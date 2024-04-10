import {
  useAudioLevel,
  useAudioTrack,
  useLocalSessionId,
} from "@daily-co/daily-react";
import { useCallback, useRef } from "react";

export const AudioLevelMonitor: React.FC = () => {
  const localSessionId = useLocalSessionId();
  const audioTrack = useAudioTrack(localSessionId);

  const volRef = useRef<HTMLDivElement>(null);

  useAudioLevel(
    audioTrack?.persistentTrack,
    useCallback((volume) => {
      // this volume number will be between 0 and 1
      // give it a minimum scale of 0.15 to not completely disappear 👻
      console.log(volume);
      if (volRef.current)
        volRef.current.style.transform = `scale(${Math.max(0.15, volume)})`;
    }, [])
  );

  // Your audio track's audio volume visualized in a small circle,
  // whose size changes depending on the volume level
  return (
    <div>
      <div className="vol" ref={volRef} />
      <style jsx>{`
        .vol {
          border: 1px solid black;
          border-radius: 100%;
          height: 32px;
          transition: transform 0.1s ease;
          width: 32px;
        }
      `}</style>
    </div>
  );
};

export default AudioLevelMonitor;
