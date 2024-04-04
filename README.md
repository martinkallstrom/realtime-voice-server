# Daily AI example apps

Collection of self-contained real-time AI demo applications built with [dailyai](https://github.com/daily-co/dailyai/)

(... intro text here)

---

## Quickstart

Each demo is standalone, with its own set of project files, dependencies and configuration variables. This repo intentionally avoids shared code across projects, so you can grab whichever folder / demo you want to work with as a starting point.

We recommend you start with a virtual environment:

```
python -m venv venv

# Mac / Linux:
source venv/bin/active 

# Windows:
source venv/Scripts/Active
```

From there, follow the getting started steps in the README for each demo.


---

## Demos:

Please be sure to check the corresponding README and env.example for guidance for how to get it running.

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

### Other demos:

#### Chat Bot with Silero VAD (GPU)

[ image ]

By default the Daily AI framework uses a CPU-bound version of VAD (voice activity detection.) If working with hardware acceleration capabilities, such as CUDA, it's possible leverag trained models for greater accuracy.

---

## Local development
...

---

## Deployment

For each of these demos we've included a `Dockerfile`. Out of the box, this should provide everything needed to get the respective demo running on a VM.

There is a typical pattern that we've found works best for managing and spawning Daily AI agents:

[ diagram of agent spawning flow ]

Of course, these demos attempt to keep things simple and are unopinionated regarding at scale use-cases. When a Daily AI agent is summoned into a session, all we do is run a new subprocess on the same machine instance &mdash; useful for small tests, but not so great for production grade apps with many concurrent users.

Creating virualized worker pools and on-demand instances is out of scope for these examples, but we have shared various implementation ideas here.

---

## Getting help