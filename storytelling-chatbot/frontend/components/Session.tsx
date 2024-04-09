"use client";

import React, { useState, useCallback } from "react";

import { useDaily } from "@daily-co/daily-react";
import {
  useParticipantIds,
  useAppMessage,
  DailyAudio,
} from "@daily-co/daily-react";
import VideoTile from "./VideoTile";
import DeviceManager from "./DevicePicker";

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
  const sendAppMessage = useAppMessage({
    onAppMessage: (e) => console.log(e),
  });

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

      await daily?.join({
        url: room_url,
        token,
        videoSource: false,
        startAudioOff: true,
      });

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
        <DeviceManager />
        Experience the wonder BotID: {botId}
        Room: {room}
        {participantIds.length ? (
          <VideoTile sessionId={participantIds[0]} />
        ) : (
          <div>Loading</div>
        )}
        <DailyAudio />
        <button onClick={() => leave()}>Leave</button>
      </div>
    );
  }

  return (
    <div>
      {state} - {room}
      <button onClick={() => start()}>Start</button>
    </div>
  );
}
