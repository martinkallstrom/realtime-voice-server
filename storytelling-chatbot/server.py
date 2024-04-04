import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

import argparse


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


@app.get("/{path_name:path}", response_class=FileResponse)
async def catch_all(path_name: str):
    """
    Renders our built React UI (with dynamic routing enabled)
    """
    if path_name == "":
        return FileResponse("frontend/out/index.html")

    file_path = Path("frontend/out") / path_name

    if file_path.is_file():
        return file_path

    html_file_path = file_path.with_suffix(".html")
    if html_file_path.is_file():
        return FileResponse(html_file_path)

    raise HTTPException(status_code=450, detail="Incorrect API call")


@app.post("/start")
async def start_agent(request: Request):
    """
    Spawn an agent worker

    proc = subprocess.Popen(
    [
        f"python3 {bot_path} -u {room_url} -k {daily_api_key} {extra_args}"
    ],
    shell=True,
    bufsize=1,
    )
    """
    return JSONResponse({"success": True})


if __name__ == "__main__":
    import uvicorn

    default_host = os.getenv("HOST", "0.0.0.0")
    default_port = int(os.getenv("FAST_API_PORT", "7860"))

    parser = argparse.ArgumentParser(description="Run the app")
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
