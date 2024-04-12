from typing import AsyncGenerator
import re

from dailyai.pipeline.frames import TextFrame, Frame, AudioFrame
from dailyai.pipeline.frame_processor import FrameProcessor
from dailyai.pipeline.frames import (
    Frame,
    TextFrame,
    SendAppMessageFrame,
    LLMResponseEndFrame,
    UserStoppedSpeakingFrame,
)

from utils.helpers import load_sounds
from prompts import LLM_IMAGE_PROMPT, IMAGE_GEN_PROMPT, CUE_USER_TURN, CUE_ASSISTANT_TURN
import asyncio

sounds = load_sounds(["talking.wav", "listening.wav", "ding.wav"])

# -------------- Frame Types ------------- #


class StoryPageFrame(TextFrame):
    # Frame for each sentence in the story before a [break]
    pass


class StoryPromptFrame(TextFrame):
    # Frame for prompting the user for input
    pass


# ------------ Frame Processors ----------- #

class StoryImageProcessor(FrameProcessor):
    """
    Processor for image prompt frames that will be sent to the FAL service.

    This processor is responsible for handling frames of type `StoryImagePromptFrame`.
    It processes the frame by printing the prompt and then passing it to the FAL service
    for further processing. The processed frames are then yielded back.

    Attributes:
        _fal_service (FALService): The FAL service used for processing frames.

    """

    def __init__(self, groq_service, fal_service, story_pages):
        self._groq_service = groq_service
        self._fal_service = fal_service
        self._story = story_pages

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, StoryPageFrame):
            yield frame

            try:
                async with asyncio.timeout(5):
                    async for f in self._groq_service.run_llm_async([
                        LLM_IMAGE_PROMPT,
                        {
                            "role": "user",
                            "content": "".join(self._story)
                        }
                    ]):
                        print("AAAA")
                        try:
                            async with asyncio.timeout(5):
                                async for i in self._fal_service.process_frame(TextFrame(IMAGE_GEN_PROMPT % f)):
                                    print("BBBB")
                                    yield i
                        except TimeoutError:
                            print("TIMEOUT 2")
                            pass
            except TimeoutError:
                print("TIMEOUT 1")
                pass
        else:
            yield frame


class StoryProcessor(FrameProcessor):
    """
    A class that processes frames and builds a story based on text frames.

    Attributes:
        _messages (list): A list of llm messages.
        _text (str): A buffer to store the text from text frames.
        _story (list): A list to store the story sentences, or 'pages'.

    Methods:
        process_frame: Processes a frame and removes any [break] or [image] tokens.
    """

    def __init__(self, messages, story):
        self._messages = messages
        self._text = ""
        self._story = story

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, UserStoppedSpeakingFrame):
            # Send an app message to the UI
            yield SendAppMessageFrame(CUE_ASSISTANT_TURN, None)
            yield AudioFrame(sounds["talking"])

        elif isinstance(frame, TextFrame):
            # We want to look for sentence breaks in the text
            # but since TextFrames are streamed from the LLM
            # we need to keep a buffer of the text we've seen so far
            self._text += frame.text

            # Looking for: [break] in the LLM response
            # We prompted our LLM to add a [break] after each sentence
            # so we use regex matching to find it in the LLM response
            if re.search(r".*\[[bB]reak\].*", self._text):
                # Remove the [break] token from the text
                # so it isn't spoken out loud by the TTS
                self._text = re.sub(r'\[[bB]reak\]', '',
                                    self._text, flags=re.IGNORECASE)
                self._text = self._text.replace("\n", " ")
                if len(self._text) > 2:
                    # Append the sentence to the story
                    self._story.append(self._text)
                    yield StoryPageFrame(self._text)
                    # Assert that it's the LLMs turn, until we're finished
                    yield SendAppMessageFrame(CUE_ASSISTANT_TURN, None)
                # Clear the buffer
                self._text = ""

        # End of LLM response
        # Driven by the prompt, the LLM should have asked the user for input
        elif isinstance(frame, LLMResponseEndFrame):
            # We use a different frame type, as to avoid image generation ingest
            yield StoryPromptFrame(self._text)
            self._text = ""
            yield frame
            # Send an app message to the UI
            yield SendAppMessageFrame(CUE_USER_TURN, None)
            yield AudioFrame(sounds["listening"])

        # Anything that is not a TextFrame pass through
        else:
            yield frame
