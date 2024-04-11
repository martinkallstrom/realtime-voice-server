[![PyPI](https://img.shields.io/pypi/v/dailyai)](https://pypi.org/project/dailyai)
[![PyPI](https://img.shields.io/badge/docs-docusaurus)](https://daily-co.github.io/dailyai-docs/docs/intro)

# Daily AI Examples

Collection of self-contained real-time voice and video AI demo applications built with [dailyai](https://github.com/daily-co/dailyai/).

## Quickstart

Each project has a set of dependencies and configuration variables. This repo intentionally avoids shared code across projects &mdash; you can grab whichever demo folder you want to work with as a starting point.

We recommend you start with a virtual environment:

```shell
python -m venv venv

# Mac / Linux:
source venv/bin/activate

# Windows:
source venv/Scripts/Activate

cd simple-chatbot

pip install -r requirements.txt
```

Next, follow the steps in the README for each demo.

Note: make sure you `pip install -r requirements.txt` for each demo project, so you can be sure to have the necessary service dependencies that extend the functionality of Daily AI. You can read more about the framework architecture [here](https://github.com/daily-co/dailyai?tab=readme-ov-file#getting-started).

## Projects:

| Project                                      | Description                                                                                                                                | Services                                              |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| [Simple Chatbot](simple-chatbot)             | Basic voice-driven conversational bot. A good starting point for learning the flow of the framework.                                       | Deepgram, OpenAI, Daily Prebuilt UI                   |
| [Storytelling Chatbot](storytelling-chatbot) | Stitches together multiple third-party services to create a collaborative storytime experience.                                            | Deepgram, ElevenLabs, Anthropic, Groq, Fal, Custom UI |
| [Translation Chatbot](translation-chatbot)   | Listens for user speech, then translates that speech to Spanish and speaks the translation back. Demonstrates multi-participant use-cases. | Deepgram, Azure, OpenAI, Daily Prebuilt               |
| [Moondream Chatbot](moondream-chatbot)       | Demonstrates how to add vision capabilities to GPT4. **Note: works best with a GPU**                                                       | Deepgram,OpenAI, Moondream, Daily Prebuilt            |

> [!IMPORTANT]
> Daily Prebuilt is a hosted video calling UI.
> Any real-time session powered by Daily can be joined using Daily Prebuilt
> It provides a quick way to test your ideas, without building any frontend code

## Other demos:

The Daily AI repo has a wide array of feature demos [found here](https://github.com/daily-co/dailyai/tree/main/examples)

---

## FAQ

### Deployment

For each of these demos we've included a `Dockerfile`. Out of the box, this should provide everything needed to get the respective demo running on a VM.

```shell
docker build username/app:tag .

docker run -p 7860:7860 --env-file ./.env username/app:tag
```

### SSL

If you're working with a custom UI (such as with the Storytelling Chatbot), it's important to ensure your platform supports HTTPS, as accessing user devices such as mics and webcams requires it.

### Are these examples production ready?

Yes, and unfortunately no.

These demos attempt to keep things simple and are unopinionated regarding scalability. We're using FastAPI to spawn a subprocess for the bots / agents &mdash; useful for small tests, but not so great for production grade apps with many concurrent users.

Creating virualized worker pools and on-demand instances is out of scope for these examples, but we have shared various implementation ideas here.

### What is VAD?

Voice Activity Detection &mdash; very important for knowing when a user has finished speaking to your bot.

Daily AI makes use of WebRTC VAD by default when using the Daily transport layer. Optionally, you can use Silero VAD for improved accuracy at the cost of higher CPU usage. You can enable Silero like so:

```shell
pip install dailyai[silero]
```

```py
transport = DailyTransport(
    room_url,
    token,
    "Bot Name",
    ...
    vad_enabled=True #Note: True by default
)
```

The first time your run your bot with Silero enabled things may take a while to get started as it downloads and caches the model.

## Getting help

➡️ [Join our Discord](https://discord.gg/dailyai)

➡️ [Reach us on Twitter](https://x.com/trydaily)
