import React from "react";
import styles from "./VideoTile.module.css";
import { DailyVideo } from "@daily-co/daily-react";

const VideoTile = ({ sessionId }) => {
  return (
    <div className={styles.videoTile}>
      <DailyVideo
        sessionId={sessionId}
        type={"video"}
        className="aspect-square"
      />
    </div>
  );
};

export default VideoTile;
