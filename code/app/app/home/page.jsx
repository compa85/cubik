"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

export default function Page() {
  const [movements, setMovements] = useState([]);
  const [timer, setTimer] = useState(null);

  const sendMovements = () => {
    const stringMovements = movements.join("");
    fetch(`http://192.168.6.1:6001/api?action=move&movements=${stringMovements}`)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  };

  const handleRotation = (face) => {
    setMovements((prevMovements) => [...prevMovements, face]);
    if (timer) {
      clearTimeout(timer);
    }
  };

  useEffect(() => {
    if (movements.length > 0) {
      const timeout = setTimeout(() => {
        sendMovements();
        setMovements([]);
      }, 500);
      setTimer(timeout);
    }

    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [movements]);

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
