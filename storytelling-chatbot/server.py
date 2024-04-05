import os
import argparse
import subprocess

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from utils.daily_helpers import create_room as _create_room, get_token

# Bot sub-process dict for status reporting
bot_procs = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="frontend/out",
          html=True), name="static")


@app.get("/", response_class=FileResponse)
async def catch_all(path_name: str) -> FileResponse:
    return FileResponse("frontend/out/index.html")


@app.post("/create")
async def create_room(request: Request) -> JSONResponse:
    room_url, room_name = _create_room()

    return JSONResponse({"room_url": room_url, "room_name": room_name})


@app.post("/start")
async def start_agent(request: Request) -> JSONResponse:
    data = await request.json()

    # Is this a webhook creation request?
    if "test" in data:
        return JSONResponse({"test": True})

    # Ensure the room property is present
    room_url = data.get('room_url')
    if not room_url:
        raise HTTPException(
            status_code=500, detail="Missing 'room' property in request data. Cannot start agent without a target room!")

    token = get_token(room_url)

    if not token:
        raise HTTPException(
            status_code=500, detail=f"Failed to get token for room: {room_url}")

    # Spawn a new agent, and join the user session
    # Note: this is mostly for demonstration purposes (refer to 'deployment' in README)
    try:
        proc = subprocess.Popen(
            [
                f"python3 -m agent.bot -u {room_url} -t {token}"
            ],
            shell=True,
            bufsize=1,
        )
        bot_procs[proc.pid] = proc
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start subprocess: {e}")

    return JSONResponse({"bot_id": proc.pid, "room_url": room_url})


@app.get("/status/{pid}")
def get_status(pid: int):
    # Look up the subprocess
    proc = bot_procs.get(pid)

    # If the subprocess doesn't exist, return an error
    if not proc:
        raise HTTPException(
            status_code=404, detail=f"Bot with process id: {pid} not found")

    # Check the status of the subprocess
    if proc.poll() is None:
        status = "running"
    else:
        status = "finished"

    return JSONResponse({"bot_id": pid, "status": status})


if __name__ == "__main__":
    import uvicorn

    default_host = os.getenv("HOST", "0.0.0.0")
    default_port = int(os.getenv("FAST_API_PORT", "7860"))

    parser = argparse.ArgumentParser(
        description="Daily Storyteller FastAPI server")
    parser.add_argument("--host", type=str,
                        default=default_host, help="Host address")
    parser.add_argument("--port", type=int,
                        default=default_port, help="Port number")
    parser.add_argument("--reload", action="store_true",
                        help="Reload code on change")

    config = parser.parse_args()

    uvicorn.run(
        "server:app",
        host=config.host,
        port=config.port,
        reload=config.reload,
    )
