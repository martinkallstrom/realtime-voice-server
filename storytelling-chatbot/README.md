# Storytelling Chat Bot

[video]

This example shows how to build a voice-driven interactive storytelling experience. 
It periodically prompts the user for input for a 'choose your own adventure' style experience.
We add a bit of visual flair to our story by generating images at lightning speed.

It uses the following AI services:

**Deepgram - Speech-to-Text**

Transcribes inbound participant voice media to text.

**Anthropic (Claude 3) - LLM**

Our creative writer LLM. You can see the context used to prompt it here: ...

**Eleven - Labs Text-to-Speech**

Streams the LLM response to audio

**Fal.ai - Image Generation**

Adds pictures to our story (really fast!) Prompting is quite key for style consistency, see here: ...


---


## Setup

**Install requirements**
```
pip install -r requirements.txt
```

**Create environment file and set variables:**
```
mv env.example .env
```

**Build the frontend:**

This project uses a custom frontend, which needs to built. Note: this is done automatically as part of the Docker deployment.

```
cd frontend/
npm install / yarn
npm run build
```


The build UI files can be found in `frontend/out`


## Running it locally

Start the API / bot manager:

`python server.py`

If you'd like to run a custom domain or port:

`python server.py --host somehost --p 7777`


➡️ Open the host URL in your browser


---


## How does it work?

...


---


## Deploying

...