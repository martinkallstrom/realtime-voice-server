import asyncio
import aiohttp
import logging
import os
import argparse

from dailyai.pipeline.pipeline import Pipeline
from dailyai.pipeline.frames import TextFrame, LLMMessagesFrame
from dailyai.transports.daily_transport import DailyTransport
from dailyai.services.anthropic_llm_service import AnthropicLLMService

from agent.debug_service import FalImageGenService
# from dailyai.services.elevenlabs_ai_service import ElevenLabsTTSService

from dotenv import load_dotenv
load_dotenv(override=True)

logging.basicConfig(format=f"%(levelno)s %(asctime)s %(message)s")
logger = logging.getLogger("dailyai")
logger.setLevel(logging.DEBUG)


async def main(room_url, token=None):
    async with aiohttp.ClientSession() as session:
        transport = DailyTransport(
            room_url,
            token,
            "Storyteller Bot",
            mic_enabled=True,
            camera_enabled=True,
            camera_width=768,
            camera_height=768,
        )

        """
        tts = ElevenLabsTTSService(
            aiohttp_session=session,
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        )
        """

        llm = AnthropicLLMService(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        fal_params = FalImageGenService.InputParams(
            image_size={
                "width": 768,
                "height": 768
            },
            expand_prompt=True,
        )

        imagegen = FalImageGenService(
            aiohttp_session=session,
            model="fal-ai/fast-lightning-sdxl",
            params=fal_params,
            key_id=os.getenv("FAL_KEY_ID"),
            key_secret=os.getenv("FAL_KEY_SECRET"),
        )

        pipeline = Pipeline(processors=[llm, imagegen])

        @transport.event_handler("on_first_other_participant_joined")
        async def on_first_other_participant_joined(transport):
            # Note that we do not put an EndFrame() item in the pipeline for this demo.
            # This means that the bot will stay in the channel until it times out.
            # An EndFrame() in the pipeline would cause the transport to shut
            # down.
            await pipeline.queue_frames(
                [
                    LLMMessagesFrame(messages=[
                        {
                            "role": "system",
                            "content": f"Describe a nature photograph suitable for use in a calendar, for the month of {month}. Include only the image description with no preamble. Limit the description to one sentence, please.",
                        }
                    ]),
                    TextFrame("a doggo"),
                    TextFrame("some chocolate"),
                    TextFrame("a tiny frog"),
                    TextFrame("a cat in the style of picasso")
                ]
            )

        await transport.run(pipeline)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Daily Storyteller Bot")
    parser.add_argument("-u", type=str, help="Room URL")
    parser.add_argument("-t", type=str, help="Token")
    config = parser.parse_args()

    asyncio.run(main(config.u, config.t))
