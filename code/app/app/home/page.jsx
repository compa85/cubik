"use client";

import { Button } from "@/components/ui/button";
import { faPlugCircleBolt, faPlugCircleXmark } from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function Page() {
  const handleRotationClick = (face) => {
    fetch(`http://192.168.6.1:6001/api?action=move&movements=${face}`)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  const enableMotors = () => {
    fetch("http://192.168.6.1:6001/api?action=enableMotors")
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  const disableMotors = () => {
    fetch("http://192.168.6.1:6001/api?action=disableMotors")
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="flex h-full flex-col items-center justify-center gap-10">
      <div className="flex items-center justify-center gap-2">
        {["U", "L", "F", "R", "B", "D"].map((face) => (
          <Button key={face} variant="outline" isIconOnly color="secondary" onClick={() => handleRotationClick(face)}>
            {face}
          </Button>
        ))}
      </div>
      <div className="flex items-center justify-center gap-2">
        <Button variant="outline" color="secondary" onClick={() => enableMotors()}>
          <FontAwesomeIcon icon={faPlugCircleBolt} size="lg" /> Enable motors
        </Button>
        <Button variant="outline" color="secondary" onClick={() => disableMotors()}>
          <FontAwesomeIcon icon={faPlugCircleXmark} size="lg" /> Disable motors
        </Button>
      </div>
    </div>
  );
}
