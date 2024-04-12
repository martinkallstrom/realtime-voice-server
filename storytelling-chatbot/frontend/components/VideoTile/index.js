import React from "react";
import styles from "./VideoTile.module.css";
import { DailyVideo } from "@daily-co/daily-react";
import StoryTranscript from "@/components/StoryTranscript";

const VideoTile = ({ sessionId }) => {
  return (
    <div className="relative">
      <StoryTranscript />

      <div className={styles.videoTile}>
        <DailyVideo
          sessionId={sessionId}
          type={"video"}
          className="aspect-square"
        />
      </div>
    </div>
  );
};

export default VideoTile;
