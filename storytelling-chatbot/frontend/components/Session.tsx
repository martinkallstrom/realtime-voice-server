"use client";

import React, { useState, useCallback, useEffect } from "react";

import { useDaily } from "@daily-co/daily-react";
import {
  useParticipantIds,
  useAppMessage,
  DailyAudio,
} from "@daily-co/daily-react";
import VideoTile from "./VideoTile";
import DeviceManager from "./DevicePicker";
import AudioLevelMonitor from "./AudioLevelMonitor";
import { MicToggle } from "./MicToggle";

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

  useAppMessage({
    onAppMessage: (e) => {
      if (!daily) return;

      if (e.fromId === "transcription") {
        console.log(e.data?.text);
      }

      if (!e.data?.cue) return;

      if (e.data?.cue === "user_turn") {
        daily.setLocalAudio(true);
      } else {
        daily.setLocalAudio(false);
      }
    },
  });

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
        <MicToggle />
        <AudioLevelMonitor />
        <button onClick={() => leave()}>Leave</button>
      </div>
    );
  }

  return (
    <div>
      {state} - {room}
      <p>For best results: use a quiet environment</p>
      <button onClick={() => start()}>Start</button>
    </div>
  );
}
