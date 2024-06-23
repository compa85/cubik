"use client";

import { Button } from "@/components/ui/button";

export default function Page() {
  const handleRotation = (face) => {
    fetch(`http://192.168.6.1:6001/api?action=move&movements=${face}`)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="flex h-full items-center justify-center gap-2">
      {["U", "L", "F", "R", "B", "D"].map((face) => (
        <Button key={face} variant="outline" color="secondary" onClick={() => handleRotation(face)}>
          {face}
        </Button>
      ))}
    </div>
  );
}
