from typing import AsyncGenerator
import re

from click import prompt
from dailyai.pipeline.frames import TextFrame, Frame
from dailyai.pipeline.frame_processor import FrameProcessor
from dailyai.pipeline.frames import (
    Frame,
    TextFrame,
    LLMResponseEndFrame,
    LLMResponseStartFrame,
    AudioFrame,
    ImageFrame,
    UserStoppedSpeakingFrame,
)


class StoryStartFrame(TextFrame):
    pass


class StoryPageFrame(TextFrame):
    pass


class StoryPromptFrame(TextFrame):
    pass


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
            # @TODO: Hide UI elements
            pass

        elif isinstance(frame, TextFrame):
            # We want to look for sentence breaks in the text
            # but since TextFrames are streamed from the LLM
            # we need to keep a buffer of the text we've seen so far
            self._text += frame.text

            # Looking for: [break] in the LLM response
            # We prompted our LLM to add a [break] after each sentence
            # so we use regex matching to find it in the LLM response
            if re.findall(r".*\[[bB]reak\].*", self._text):
                # Remove the [break] token from the text
                # so it isn't spoken out loud by the TTS
                self._text = re.sub(r'\[[bB]reak\]', '',
                                    self._text, flags=re.IGNORECASE)
                self._text = self._text.replace("\n", " ")
                if len(self._text) > 2:
                    # Append the sentence to the story
                    self._story.append(self._text)
                    yield StoryPageFrame(self._text)
                # Clear the buffer
                self._text = ""

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
