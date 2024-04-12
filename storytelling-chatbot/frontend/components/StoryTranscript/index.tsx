"use client";

import React, { useEffect, useRef, useState } from "react";

import { useAppMessage } from "@daily-co/daily-react";
import { DailyEventObjectAppMessage } from "@daily-co/daily-js";

import styles from "./StoryTranscript.module.css";

export default function StoryTranscript() {
  const [partialText, setPartialText] = useState<string>("");
  const [sentences, setSentences] = useState<string[]>([]);
  const intervalRef = useRef<any | null>(null);

  useEffect(() => {
    clearInterval(intervalRef.current);

    intervalRef.current = setInterval(() => {
      if (sentences.length > 2) {
        setSentences((s) => s.slice(1));
      }
    }, 2500);

    return () => clearInterval(intervalRef.current);
  }, [sentences]);

  useAppMessage({
    onAppMessage: (e: DailyEventObjectAppMessage<any>) => {
      if (e.fromId && e.fromId === "transcription") {
        // Check for LLM transcripts only
        if (e.data.user_id !== "") {
          setPartialText(e.data.text);
          if (e.data.is_final) {
            setPartialText("");
            setSentences((s) => [...s, e.data.text]);
          }
        }
      }
    },
  });

  return (
    <div className="absolute text-white top-0 z-50 text-center max-w-sm mx-auto flex flex-col justify-end content-end h-[300px]">
      {sentences.map((sentence, index) => (
        <p key={index} className={`${styles.transcript} ${styles.sentence}`}>
          {sentence}
        </p>
      ))}
      {partialText && <p className={`${styles.transcript}`}>{partialText}</p>}
    </div>
  );
}
