import React from "react";

import styles from "./UserInputIndicator.module.css";
import { IconMicrophone } from "@tabler/icons-react";

interface Props {
  active: boolean;
}

export default function UserInputIndicator({ active }: Props) {
  return (
    <div className={`${styles.panel} ${active ? styles.active : ""}`}>
      <div className="relative z-20 flex flex-col">
        <div
          className={`${styles.micIcon} ${active ? styles.micIconActive : ""}`}
        >
          <IconMicrophone size={42} />
          {active && <div className={styles.bubble}></div>}
        </div>
        <footer className={styles.transcript}>...</footer>
      </div>
    </div>
  );
}
