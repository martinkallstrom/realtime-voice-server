import React, { useState } from "react";
import {
  useDaily,
  useParticipantIds,
  useAppMessage,
  DailyAudio,
} from "@daily-co/daily-react";
import VideoTile from "@/components/VideoTile";
import { Button } from "@/components/ui/button";
import UserInputIndicator from "@/components/UserInputIndicator";

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
    <div className="w-full flex flex-col flex-1 self-stretch">
      <div className="absolute inset-0 bg-gray-900 bg-opacity-80 z-10 fade-in"></div>

      <div className="relative z-20 flex-1">
        {participantIds.length ? (
          <VideoTile sessionId={participantIds[0]} />
        ) : (
          <div>Loading</div>
        )}

        <Button onClick={() => handleLeave()}>Finish story</Button>

        <DailyAudio />
      </div>
      <UserInputIndicator active={storyState === "user"} />
    </div>
  );
};

export default Story;
