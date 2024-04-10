import React from "react";
import { Button } from "@/components/ui/button";
import DevicePicker from "@/components/DevicePicker";
import { IconEar, IconLoader2 } from "@tabler/icons-react";

type SetupProps = {
  handleStart: () => void;
};

const buttonLabel = {
  intro: "Next",
  setup: "Let's begin!",
  loading: "Joining...",
};
export const Setup: React.FC<SetupProps> = ({ handleStart }) => {
  const [state, setState] = React.useState<"intro" | "setup" | "loading">(
    "intro"
  );

  return (
    <div className="flex-1 bg-white rounded-3xl cardAnim cardShadow p-9 max-w-screen-sm mx-auto outline outline-[5px] outline-gray-600/10">
      <div className="flex flex-col gap-6">
        <h1 className="text-4xl font-bold text-pretty tracking-tighter mb-4">
          Welcome to <span className="text-sky-500">Storytime</span>
        </h1>
        {state === "intro" ? (
          <>
            <p className="text-gray-600 leading-relaxed text-pretty">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut
              congue, quam id malesuada consectetur, elit mauris blandit augue,
              facilisis facilisis metus nunc eget leo. Sed vitae ligula in
              ligula semper fringilla nec ac dolor.
            </p>
            <p className="flex flex-row gap-2 text-gray-600 font-medium">
              <IconEar size={24} /> For best results, try in a quiet
              environment!
            </p>
          </>
        ) : (
          <>
            <p className="text-gray-600 leading-relaxed text-pretty">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut
              congue, quam id malesuada consectetur.
            </p>
            <DevicePicker />
          </>
        )}

        <hr className="border-gray-150 my-2" />

        <Button
          size="lg"
          disabled={state === "loading"}
          onClick={() => {
            if (state === "intro") {
              setState("setup");
            } else {
              setState("loading");
              handleStart();
            }
          }}
        >
          {state === "loading" && (
            <IconLoader2
              size={21}
              stroke={2}
              className="mr-2 h-4 w-4 animate-spin"
            />
          )}
          {buttonLabel[state]}
        </Button>
      </div>
    </div>
  );
};

export default Setup;
