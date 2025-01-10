import React, { useState, useEffect, useRef } from "react";

const RangeSelectAdorner = ({
  initialRange = { min: 0, max: 100 },
  color = "rgba(0, 0, 255, 0.5)",
  isSelected = false,
  onRangeChange,
}) => {
  const [range, setRange] = useState(initialRange);
  const [isDragging, setIsDragging] = useState(false);
  const [isCurrentlySelected, setIsCurrentlySelected] = useState(isSelected);
  const containerRef = useRef(null);

  const handleMouseDown = (e) => {
    const rect = containerRef.current.getBoundingClientRect();
    const startX = e.clientX - rect.left;
    setRange({ min: startX, max: startX });
    setIsDragging(true);
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    const rect = containerRef.current.getBoundingClientRect();
    const currentX = e.clientX - rect.left;
    setRange((prevRange) => ({
      min: Math.min(prevRange.min, currentX),
      max: Math.max(prevRange.min, currentX),
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
    if (onRangeChange) {
      onRangeChange(range);
    }
  };

  const toggleSelection = () => {
    setIsCurrentlySelected((prev) => !prev);
  };

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height: "200px",
        position: "relative",
        backgroundColor: "#f0f0f0",
        border: "1px solid #ccc",
        userSelect: "none",
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onDoubleClick={toggleSelection} // Double-click to toggle selection
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          left: `${range.min}px`,
          width: `${range.max - range.min}px`,
          height: "100%",
          backgroundColor: isCurrentlySelected ? color : "rgba(128, 128, 128, 0.5)",
          border: isCurrentlySelected ? "2px solid #000" : "2px solid #aaa",
        }}
      ></div>
    </div>
  );
};

export default RangeSelectAdorner;
