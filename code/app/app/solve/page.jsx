"use client";

import { Button } from "@/components/ui/button";
import { faRocketLaunch } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function Page() {
  const handleSolve = async () => {
    fetch("http://192.168.6.1:6001/api?action=solve")
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="flex h-full items-center justify-center">
      <Button onClick={handleSolve}>
        <FontAwesomeIcon icon={faRocketLaunch} /> Solve
      </Button>
    </div>
  );
}
