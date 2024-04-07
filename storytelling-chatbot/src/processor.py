from typing import AsyncGenerator
import re

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
    def __init__(self, messages, story):
        self._messages = messages
        self._text = ""
        self._story = story

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, UserStoppedSpeakingFrame):
            print("USER FINISHED SPEAKING")
            pass
        elif isinstance(frame, TextFrame):
            yield frame
        elif isinstance(frame, LLMResponseStartFrame):
            print("LLM RESPONSE START")
            yield StoryPromptFrame("painting of a frog")
            yield frame
        elif isinstance(frame, LLMResponseEndFrame):
            print("LLM RESPONSE END")
            yield StoryPromptFrame("painting of a cat")
            yield frame
        else:
            yield frame
