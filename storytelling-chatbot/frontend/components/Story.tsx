import React, { useState } from "react";
import {
  useDaily,
  useParticipantIds,
  useAppMessage,
  DailyAudio,
} from "@daily-co/daily-react";
import VideoTile from "@/components/VideoTile";
import { Button } from "@/components/ui/button";
import DevicePicker from "@/components/DevicePicker";

interface StoryProps {
  handleLeave: () => void;
}

const Story: React.FC<StoryProps> = ({ handleLeave }) => {
  const daily = useDaily();
  const participantIds = useParticipantIds({ filter: "remote" });
  const [storyState, setStoryState] = useState<"user" | "assistant">(
    "assistant"
  );

  useAppMessage({
    onAppMessage: (e) => {
      if (!daily) return;

      /*if (e.fromId === "transcription") {
        console.log(e.data?.text);
      }*/

      if (!e.data?.cue) return;

      if (e.data?.cue === "user_turn") {
        daily.setLocalAudio(true);
        setStoryState("user");
      } else {
        daily.setLocalAudio(false);
        setStoryState("assistant");
      }
    },
  });

  return (
    <div>
      <h1>Story Component</h1>

      {participantIds.length ? (
        <VideoTile sessionId={participantIds[0]} />
      ) : (
        <div>Loading</div>
      )}

      <Button onClick={() => handleLeave()} />
      <DailyAudio />

      <DevicePicker />
    </div>
  );
};

export default Story;
