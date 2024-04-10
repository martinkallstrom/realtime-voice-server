import {
  useAudioLevel,
  useAudioTrack,
  useLocalSessionId,
} from "@daily-co/daily-react";
import { useCallback, useRef } from "react";

export const AudioIndicator: React.FC = () => {
  const localSessionId = useLocalSessionId();
  const audioTrack = useAudioTrack(localSessionId);

  const volRef = useRef<HTMLDivElement>(null);

  useAudioLevel(
    audioTrack?.persistentTrack,
    useCallback((volume) => {
      // this volume number will be between 0 and 1
      // give it a minimum scale of 0.15 to not completely disappear 👻
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

export const AudioIndicatorBar: React.FC = () => {
  const localSessionId = useLocalSessionId();
  const audioTrack = useAudioTrack(localSessionId);

  const volRef = useRef<HTMLDivElement>(null);

  useAudioLevel(
    audioTrack?.persistentTrack,
    useCallback((volume) => {
      if (volRef.current)
        volRef.current.style.width = Math.max(2, volume * 100) + "%";
    }, [])
  );

  return (
    <div className="flex-1 bg-gray-200 h-[8px] rounded-full overflow-hidden">
      <div
        className="bg-green-500 h-[8px] w-full rounded-full transition-all duration-100 ease"
        ref={volRef}
      />
    </div>
  );
};

export default AudioIndicator;
