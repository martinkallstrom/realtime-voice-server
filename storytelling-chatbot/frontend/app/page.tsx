"use client";

import React from "react";
import { DailyProvider, useCallObject } from "@daily-co/daily-react";

import Session from "../components/Session";

export default function Home() {
  const callObject = useCallObject({});

  return (
    <DailyProvider callObject={callObject}>
      <Session />
    </DailyProvider>
  );
}
