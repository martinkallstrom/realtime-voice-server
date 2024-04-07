import asyncio
import aiohttp
import logging
import os
import argparse
from typing import AsyncGenerator

from dailyai.pipeline.pipeline import Pipeline
from dailyai.pipeline.frames import EndPipeFrame, Frame, LLMMessagesFrame
from dailyai.pipeline.aggregators import (
    UserResponseAggregator,
    LLMResponseAggregator,
)
from dailyai.transports.daily_transport import DailyTransport
from dailyai.pipeline.frame_processor import FrameProcessor
# from dailyai.services.anthropic_llm_service import AnthropicLLMService
from dailyai.services.elevenlabs_ai_service import ElevenLabsTTSService
from dailyai.services.open_ai_services import OpenAILLMService
from dailyai.services.ai_services import FrameLogger

from services.fal import FalImageGenService
from processor import StoryProcessor, StoryPageFrame
from prompts import LLM_BASE_PROMPT, LLM_INTRO_PROMPT


from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format=f"[STORYBOY] %(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("dailyai")
logger.setLevel(logging.INFO)


class StoryImageGenerator(FrameProcessor):
    def __init__(self, story, llm, fal_service):
        self._llm = llm
        self._fal_service = fal_service
        self._story = story

    async def process_frame(self, frame: Frame) -> AsyncGenerator[Frame, None]:
        if isinstance(frame, StoryPageFrame):
            print("START IMAGE FLOW")
            # prompt = frame.text
            # async for f in self._fal_service.process_frame(TextFrame(prompt)):
            #    yield f
        else:
            yield frame


async def main(room_url, token=None):
    async with aiohttp.ClientSession() as session:

        # -------------- Transport --------------- #

        transport = DailyTransport(
            room_url,
            token,
            "Storytelling Bot",
            duration_minutes=5,
            start_transcription=True,
            mic_enabled=True,
            mic_sample_rate=16000,
            vad_enabled=True,
            camera_framerate=30,
            camera_bitrate=680000,
            camera_enabled=True,
            camera_width=768,
            camera_height=768,
        )

        logger.debug("Transport created for room:" + room_url)

        # -------------- Services --------------- #

        llm_service = OpenAILLMService(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4-turbo-preview"
        )

        tts_service = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        )

        fal_service_params = FalImageGenService.InputParams(
            image_size={
                "width": 768,
                "height": 768
            },
            expand_prompt=True,
        )

        fal_service = FalImageGenService(
            aiohttp_session=session,
            model="fal-ai/fast-lightning-sdxl",
            params=fal_service_params,
            key_id=os.getenv("FAL_KEY_ID"),
            key_secret=os.getenv("FAL_KEY_SECRET"),
        )
        # --------------- Setup ----------------- #
        message_history = [LLM_BASE_PROMPT]
        story_pages = []

        image_generator = StoryImageGenerator(
            story_pages, llm_service, fal_service)
        story_processor = StoryProcessor(message_history, story_pages)

        llm_responses = LLMResponseAggregator(message_history)
        user_responses = UserResponseAggregator(message_history)

        # fl = FrameLogger("### After Image Generation")

        logger.debug("Waiting for participant...")

        # ------------- Story Loop -------------- #

        start_storytime_event = asyncio.Event()

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport):
            logger.debug("Participant joined, storytime commence!")
            start_storytime_event.set()

        async def storytime():
            await start_storytime_event.wait()

            intro_pipeline = Pipeline(processors=[
                llm_service,
                story_processor,
                tts_service,
                llm_responses,
            ], sink=transport.send_queue)

            await intro_pipeline.queue_frames(
                [
                    LLMMessagesFrame(message_history),
                    EndPipeFrame(),
                ]
            )

            await intro_pipeline.run_pipeline()

            print("BEEP")

            pipeline = Pipeline(processors=[
                user_responses,
                llm_service,
                story_processor,
                # image_generator,
                tts_service,
                llm_responses
            ])

            await transport.run_pipeline(pipeline)

        transport.transcription_settings["extra"]["endpointing"] = True
        transport.transcription_settings["extra"]["punctuate"] = True

        try:
            await asyncio.gather(transport.run(), storytime())
        except (asyncio.CancelledError, KeyboardInterrupt):
            transport.stop()

        logger.debug("Pipeline finished. Exiting.")

        """
        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport):
            print("B")
            start_story_event.set()

        async def storytime():
            await start_story_event.wait()

            llm_context = LLMAssistantContextAggregator(messages)

            story_teller_pipeline = Pipeline([
                llm_service,
                llm_context,
            ], sink=transport.send_queue)

            await story_teller_pipeline.queue_frames(
                [
                    LLMMessagesFrame(LLM_INTRO_PROMPT),
                    EndPipeFrame(),
                ]
            )

            await story_teller_pipeline.run_pipeline()

            try:
                await asyncio.gather(transport.run(), storytime())
            except (asyncio.CancelledError, KeyboardInterrupt):
                print("whoops")
                transport.stop()
        """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Daily Storyteller Bot")
    parser.add_argument("-u", type=str, help="Room URL")
    parser.add_argument("-t", type=str, help="Token")
    config = parser.parse_args()

    asyncio.run(main(config.u, config.t))
