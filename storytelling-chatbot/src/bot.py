import asyncio
import aiohttp
import logging
import os
import argparse
from typing import AsyncGenerator

from dailyai.pipeline.pipeline import Pipeline
from dailyai.pipeline.frames import EndPipeFrame, LLMMessagesFrame
from dailyai.pipeline.aggregators import (
    UserResponseAggregator,
    LLMResponseAggregator,
)
from dailyai.transports.daily_transport import DailyTransport
from dailyai.services.elevenlabs_ai_service import ElevenLabsTTSService
from dailyai.services.open_ai_services import OpenAILLMService
from dailyai.services.ai_services import FrameLogger

from services.fal import FalImageGenService
from processors import StoryProcessor, StoryImageProcessor
from prompts import LLM_BASE_PROMPT


from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format=f"[STORYBOY] %(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("dailyai")
logger.setLevel(logging.INFO)


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

        # We need aggregators to keep track of user and LLM responses

        llm_responses = LLMResponseAggregator(message_history)
        user_responses = UserResponseAggregator(message_history)

        # -------------- Processors ------------- #

        image_processor = StoryImageProcessor(fal_service)
        story_processor = StoryProcessor(message_history, story_pages)

        # -------------- Story Loop ------------- #

        logger.debug("Waiting for participant...")

        start_storytime_event = asyncio.Event()

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport):
            logger.debug("Participant joined, storytime commence!")
            start_storytime_event.set()

        # The storytime coroutine will wait for the start_storytime_event
        # to be set before starting the storytime pipeline
        async def storytime():
            await start_storytime_event.wait()

            # The intro pipeline is used to introduce start
            # the story (as per LLM_BASE_PROMPT)
            intro_pipeline = Pipeline(processors=[
                llm_service,
                story_processor,
                image_processor,
                tts_service,
                llm_responses,
            ], sink=transport.send_queue)

            await intro_pipeline.queue_frames(
                [
                    LLMMessagesFrame(message_history),
                    EndPipeFrame(),
                ]
            )

            # We start the pipeline as soon as the user joins
            await intro_pipeline.run_pipeline()

            # The main story pipeline is used to continue the
            # story based on user input
            pipeline = Pipeline(processors=[
                user_responses,
                llm_service,
                story_processor,
                image_processor,
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Daily Storyteller Bot")
    parser.add_argument("-u", type=str, help="Room URL")
    parser.add_argument("-t", type=str, help="Token")
    config = parser.parse_args()

    asyncio.run(main(config.u, config.t))
