# Daily AI examples

Collection of self-contained real-time AI demo applications built with [dailyai](https://github.com/daily-co/dailyai/)

(... intro text here)

---

## Quickstart

Each demo is a standalone project with its own set of dependencies and configuration variables. This repo intentionally avoids shared code across projects &mdash; you can grab whichever demo folder you want to work with as a starting point.

We recommend you start with a virtual environment:

```
python -m venv venv

# Mac / Linux:
source venv/bin/activate

# Windows:
source venv/Scripts/Activate
```

Next, follow the steps in the README for each demo.

Note: make sure you `pip install -r requirements.txt` for each demo project, so you can be sure to have the necessary service dependencies that extend the functionality of Daily AI. You can read more about the framework architecture [here](https://github.com/daily-co/dailyai?tab=readme-ov-file#getting-started).

---

## Demos:

### Simple Chat Bot (CPU)

[ image ]

Your basic voice-driven conversational bot

- Text-to-Speech: DeepGram
- Speech-to-Text: DeepGram
- LLM: OpenAI
- UI: Daily Prebuilt

### Translation Bot (CPU)

[ image ]

Real-time language translation with an emphasis on latency.

- Text-to-Speech: DeepGram
- Speech-to-Text: Azure
- LLM: Groq (Mixtral)
- UI: Custom

### Storytelling Bot (CPU)

[ image ]

Stitches together multiple third-party services to create a fun and collaborative storytime experience.

- Text-to-Speech: DeepGram
- Speech-to-Text: Eleven Labs
- LLM: Claude3 (Anthropic)
- Image Generation: Fal.ai
- UI: Custom

### Tool-calling Bot (CPU)

[ image ]

Process-driven workflow that demonstrates how to trigger various tools throughout the conversation (a great starting point for customer service bots!)

- Text-to-Speech: DeepGram
- Speech-to-Text: Eleven Labs
- LLM: Fireworks
- UI: Daily Prebuilt

## Other demos:

#### Chat Bot with Silero VAD (GPU)

[ image ]

By default the Daily AI framework uses a CPU-bound version of VAD (voice activity detection.) If your agent targets hardware-capable machines with CUDA support, it's possible to infer from trained models for greater accuracy.

#### Moondream Vision Bot (GPU)

[ image ]

...

---

## What is Daily, do I need it to run my bots?

...

### What is Daily Prebuilt?

To get up and running with your bots quickly, you can make use of Daily's hosted user interface for real-time video and audio calls. Daily Prebuilt will allow you to join any room on your domain via a URL, for example: `https://[your-domains].daily.co/[room_name]`.

Daily Prebuilt has been designed as a fully-featured video calling experience, and whilst it may not fit every bot use-case, it can definitely serve as a helpful debugging tool or method for avoiding building your own frontend.

---

## Deployment

`docker run -p 7860:7860 --env-file ./.env user/app:tag`

For each of these demos we've included a `Dockerfile`. Out of the box, this should provide everything needed to get the respective demo running on a VM.

There is a typical pattern that we've found works best for managing and spawning Daily AI agents:

[ diagram of agent spawning flow ]

Of course, these demos attempt to keep things simple and are unopinionated regarding scalability. When a Daily AI agent is summoned into a session, all we do is run a new subprocess on the same machine instance &mdash; useful for small tests, but not so great for production grade apps with many concurrent users.

Creating virualized worker pools and on-demand instances is out of scope for these examples, but we have shared various implementation ideas here.

#### SSL

`docker build --build-arg USE_LETSENCRYPT=1 username/app:tag .`
...

---

## Getting help

...
