
import os
import time
import urllib
import requests

from dotenv import load_dotenv
load_dotenv()


daily_api_path = os.getenv("DAILY_API_URL")
daily_api_key = os.getenv("DAILY_API_KEY")


def create_token(room_name) -> str:
    if not room_name:
        raise Exception(
            "No Daily room specified. use the -u/--url option from the command line, or set DAILY_SAMPLE_ROOM_URL in your environment to specify a Daily room URL.")

    if not daily_api_key:
        raise Exception(
            "No Daily API key specified. set DAILY_API_KEY in your environment to specify a Daily API key, available from https://dashboard.daily.co/developers.")

    # room_name: str = urllib.parse.urlparse(url).path[1:]
    expiration: float = time.time() + 60 * 60

    res: requests.Response = requests.post(
        f"https://{daily_api_path}/meeting-tokens",
        headers={
            "Authorization": f"Bearer {daily_api_key}"},
        json={
            "properties": {
                "room_name": room_name,
                "is_owner": False,
                "exp": expiration}},
    )

    if res.status_code != 200:
        raise Exception(
            f"Failed to create meeting token: {res.status_code} {res.text}")

    token: str = res.json()["token"]

    return token
