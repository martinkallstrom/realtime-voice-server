"use client";

import { useEffect } from "react";
import { DailyMeetingState } from "@daily-co/daily-js";
import { useDaily, useDevices } from "@daily-co/daily-react";
import clsx from "clsx";

interface Props {
  color?: string;
  errorColor?: string;
  label?: React.ReactNode;
}

export default function DevicePicker({
  color,
  errorColor = "var(--color-orange)",
  label,
}: Props) {
  const daily = useDaily();
  const {
    currentMic,
    hasMicError,
    micState,
    microphones,
    setMicrophone,
    currentSpeaker,
    speakers,
    setSpeaker,
  } = useDevices();

  const handleMicrophoneChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
    setMicrophone(ev.target.value);
  };

  const handleSpeakerChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
    setSpeaker(ev.target.value);
  };

  useEffect(() => {
    if (microphones.length > 0 || !daily || daily.isDestroyed()) return;
    const meetingState = daily.meetingState();
    const meetingStatesBeforeJoin: DailyMeetingState[] = [
      "new",
      "loading",
      "loaded",
    ];
    if (meetingStatesBeforeJoin.includes(meetingState)) {
      daily.startCamera({ startVideoOff: true, startAudioOff: false });
    }
  }, [daily, microphones]);

  return (
    <div className="device-picker">
      {label && (
        <label className="text-md font-500" htmlFor="device-picker">
          {label}
        </label>
      )}
      <label>Microphone:</label>
      <select
        className={clsx("text-base-mono font-500")}
        id="device-picker"
        value={hasMicError ? "error" : currentMic?.device?.deviceId}
        onChange={handleMicrophoneChange}
        style={
          {
            "--color": color,
            "--error-color": errorColor,
          } as React.CSSProperties
        }
      >
        {hasMicError && (
          <option value="error" disabled>
            No microphone access.
          </option>
        )}
        {microphones.map((m) => (
          <option key={m.device.deviceId} value={m.device.deviceId}>
            {m.device.label}
          </option>
        ))}
      </select>

      <label>Speaker:</label>
      <select
        className={clsx("text-base-mono font-500")}
        id="device-picker"
        value={currentSpeaker?.device?.deviceId}
        onChange={handleSpeakerChange}
        style={
          {
            "--color": color,
            "--error-color": errorColor,
          } as React.CSSProperties
        }
      >
        {speakers.map((m) => (
          <option key={m.device.deviceId} value={m.device.deviceId}>
            {m.device.label}
          </option>
        ))}
      </select>

      {hasMicError && (
        <div className="error">
          {micState === "blocked" ? (
            <p>
              Please check your browser and system permissions. Make sure that
              this app is allowed to access your microphone.
            </p>
          ) : micState === "in-use" ? (
            <p>
              Your microphone is being used by another app. Please close any
              other apps using your microphone and restart this app.
            </p>
          ) : micState === "not-found" ? (
            <p>
              No microphone seems to be connected. Please connect a microphone.
            </p>
          ) : micState === "not-supported" ? (
            <p>
              This app is not supported on your device. Please update your
              software or use a different device.
            </p>
          ) : (
            <p>
              There seems to be an issue accessing your microphone. Try
              restarting the app or consult a system administrator.
            </p>
          )}
        </div>
      )}
      <style jsx>{`
        .device-picker {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }
        label {
          color: var(--color);
          opacity: 0.6;
        }
        select {
          background: transparent;
          border: 1px solid transparent;
          border-radius: 16px;
          color: var(--color);
          flex: 1;
          max-width: 100%;
          overflow: hidden;
          padding: 2px 6px;
          text-overflow: ellipsis;
          transition: border-color 250ms ease;
          width: 100%;
        }
        select:focus-visible,
        select:hover {
          border: 1px solid var(--color);
          cursor: pointer;
          outline: none;
        }
        .error {
          align-items: flex-start;
          color: var(--error-color);
          display: flex;
          gap: 4px;
        }
        .error :global(svg) {
          flex: none;
        }
        .error p {
          margin: 0;
        }
      `}</style>
    </div>
  );
}
