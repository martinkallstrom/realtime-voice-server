from typing import AsyncGenerator
import re

from dailyai.pipeline.frames import TextFrame, Frame
from dailyai.services.ai_services import FrameLogger
from dailyai.pipeline.frame_processor import FrameProcessor
from dailyai.pipeline.frames import (
    Frame,
    TextFrame,
    LLMResponseEndFrame,
    LLMResponseStartFrame,
    UserStoppedSpeakingFrame,
)

from prompts import LLM_IMAGE_PROMPT, IMAGE_GEN_PROMPT

# -------------- Frame Types ------------- #


class StoryStartFrame(TextFrame):
    # Frame for when the story begins
    pass


class StoryPageFrame(TextFrame):
    # Frame for each sentence in the story before a [break]
    pass


class StoryPromptFrame(TextFrame):
    # Frame for prompting the user to continue the story
    pass


# ------------ Frame Processors ----------- #

"""
class ImagePromptLogger(FrameLogger):
    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, StoryImagePromptFrame):
            self.logger.info(f"[IMAGE PROMPT]: {frame.text}")
        yield frame
"""


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
            async for f in self._groq_service.run_llm_async([
                LLM_IMAGE_PROMPT,
                {
                    "role": "user",
                    "content": "".join(self._story)
                },
                {
                    "role": "user",
                    "content": self._story[-1]
                }
            ]):
                async for i in self._fal_service.process_frame(TextFrame(IMAGE_GEN_PROMPT % f)):
                    yield i
            yield frame
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
        # self._image_prompt = None
        self._story = story

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, UserStoppedSpeakingFrame):
            # @TODO: Hide UI elements
            pass

        elif isinstance(frame, TextFrame):
            # We want to look for sentence breaks in the text
            # but since TextFrames are streamed from the LLM
            # we need to keep a buffer of the text we've seen so far
            self._text += frame.text

            """
            # 1. Looking for < image prompts > in the LLM response
            if re.search("<", self._text):
                # Extract the prompt from the text
                if re.search(">", self._text):
                    # Extract the prompt from the text
                    self._image_prompt = re.search(
                        r'<([^>]*)>', self._text).group(1)  # type: ignore
                    # Remove the prompt from the text
                    self._text = re.sub(r'<([^>]*)>', '', self._text)
            """

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
                    # if self._image_prompt:
                    #    yield StoryImagePromptFrame(self._image_prompt)
                    yield StoryPageFrame(self._text)

                # Clear the buffer
                self._text = ""
                # self._image_prompt = None

        # End of LLM response
        elif isinstance(frame, LLMResponseEndFrame):
            print("LLM RESPONSE END")
            # @TODO: Show UI elements
            yield StoryPromptFrame(self._text)
            self._text = ""
            yield frame

        # Anything that is not a TextFrame pass through
        else:
            yield frame
