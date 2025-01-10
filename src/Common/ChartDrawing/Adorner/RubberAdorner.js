import React, { useState, useRef } from "react";

const RubberAdorner = () => {
  const [startPoint, setStartPoint] = useState(null);
  const [currentPoint, setCurrentPoint] = useState(null);
  const [shape, setShape] = useState("rectangle"); // "rectangle", "horizontal", "vertical"
  const [invert, setInvert] = useState(false);
  const containerRef = useRef(null);

  const handleMouseDown = (e) => {
    const rect = containerRef.current.getBoundingClientRect();
    setStartPoint({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
    setCurrentPoint(null);
  };

  const handleMouseMove = (e) => {
    if (!startPoint) return;
    const rect = containerRef.current.getBoundingClientRect();
    setCurrentPoint({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleMouseUp = () => {
    setStartPoint(null);
    setCurrentPoint(null);
  };

  const calculateArea = () => {
    if (!startPoint || !currentPoint) return null;

    const x1 = startPoint.x;
    const y1 = startPoint.y;
    const x2 = currentPoint.x;
    const y2 = currentPoint.y;

    switch (shape) {
      case "rectangle":
        return {
          left: Math.min(x1, x2),
          top: Math.min(y1, y2),
          width: Math.abs(x2 - x1),
          height: Math.abs(y2 - y1),
        };
      case "horizontal":
        return {
          left: Math.min(x1, x2),
          top: 0,
          width: Math.abs(x2 - x1),
          height: containerRef.current.offsetHeight,
        };
      case "vertical":
        return {
          left: 0,
          top: Math.min(y1, y2),
          width: containerRef.current.offsetWidth,
          height: Math.abs(y2 - y1),
        };
      default:
        return null;
    }
  };

  const areaStyle = () => {
    const area = calculateArea();
    if (!area) return {};

    if (invert) {
      // Inverted style (optional, for visual effect)
      return {
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        background: `radial-gradient(circle, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.5) 100%)`,
        clipPath: `polygon(${area.left}px ${area.top}px, ${area.left + area.width}px ${area.top}px, ${area.left + area.width}px ${area.top + area.height}px, ${area.left}px ${area.top + area.height}px)`,
      };
    }

    return {
      position: "absolute",
      left: `${area.left}px`,
      top: `${area.top}px`,
      width: `${area.width}px`,
      height: `${area.height}px`,
      backgroundColor: "rgba(128, 128, 128, 0.5)",
      border: "1px solid darkgray",
    };
  };

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: "400px",
        position: "relative",
        backgroundColor: "#f0f0f0",
        border: "1px solid #ccc",
        overflow: "hidden",
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      {startPoint && currentPoint && <div style={areaStyle()}></div>}
      <div style={{ position: "absolute", top: 10, left: 10 }}>
        <button onClick={() => setShape("rectangle")}>Rectangle</button>
        <button onClick={() => setShape("horizontal")}>Horizontal</button>
        <button onClick={() => setShape("vertical")}>Vertical</button>
        <button onClick={() => setInvert(!invert)}>Toggle Invert</button>
      </div>
    </div>
  );
};

export default RubberAdorner;
