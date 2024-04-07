import React, { useState } from "react";

import { useDaily } from "@daily-co/daily-react";
import { DailyVideo, useParticipantIds } from "@daily-co/daily-react";

type State =
  | "idle"
  | "connecting"
  | "connected"
  | "started"
  | "finished"
  | "error";

export default function Call() {
  const daily = useDaily();
  const participantIds = useParticipantIds({ filter: "remote" });

  const [state, setState] = useState<State>("idle");
  const [room, setRoom] = useState<string | null>(null);
  const [botId, setBotId] = useState<string | null>(null);

  async function start() {
    setState("connecting");

    try {
      const response = await fetch("/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          room_url: process.env.NEXT_PUBLIC_ROOM_URL || null,
        }),
      });

      const { room_url, token } = await response.json();

      setRoom(room_url);

      await daily?.join({ url: room_url, token, videoSource: false });

      setState("connected");

      const resp = await fetch("/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          room_url,
        }),
      });

      const { bot_id } = await resp.json();
      setBotId(bot_id);

      setState("started");
    } catch (error) {
      setState("error");
    }
  }

  async function leave() {
    await daily?.leave();
    setState("finished");
  }

  if (state === "error") {
    return <div>An Error occured</div>;
  }

  if (state === "started") {
    return (
      <div className="text-center mx-auto">
        Experience the wonder BotID: {botId}
        Room: {room}
        {participantIds.length ? (
          <DailyVideo
            sessionId={participantIds[0]}
            type={"video"}
            className="aspect-square"
          />
        ) : (
          <div>Loading</div>
        )}
        <button onClick={() => leave()}>Leave</button>
      </div>
    );
  }

  return (
    <div>
      {state} - {room}
      <video className="aspect-square flex flex-1" />
      <button onClick={() => start()}>Start</button>
    </div>
  );
}
