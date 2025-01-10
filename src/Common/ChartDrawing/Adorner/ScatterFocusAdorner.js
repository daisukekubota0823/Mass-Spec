import React, { useState, useRef } from "react";

const ScatterFocusAdorner = ({
  scatterPoints = [],
  targetPoint = null,
  outerScale = 2,
  innerScale = 1,
  radius = 10,
}) => {
  const containerRef = useRef(null);

  const calculateGeometry = (point) => {
    const largeRadius = radius * outerScale;
    const smallRadius = radius * innerScale;

    return {
      large: {
        left: point.x - largeRadius,
        top: point.y - largeRadius,
        width: largeRadius * 2,
        height: largeRadius * 2,
      },
      small: {
        left: point.x - smallRadius,
        top: point.y - smallRadius,
        width: smallRadius * 2,
        height: smallRadius * 2,
      },
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
    >
      {/* Render scatter points */}
      {scatterPoints.map((point, index) => (
        <div
          key={index}
          style={{
            position: "absolute",
            left: `${point.x - radius}px`,
            top: `${point.y - radius}px`,
            width: `${radius * 2}px`,
            height: `${radius * 2}px`,
            borderRadius: "50%",
            backgroundColor: "blue",
          }}
        ></div>
      ))}

      {/* Render focus area */}
      {targetPoint && (
        <div>
          {/* Outer circle */}
          <div
            style={{
              position: "absolute",
              left: `${targetPoint.x - radius * outerScale}px`,
              top: `${targetPoint.y - radius * outerScale}px`,
              width: `${radius * outerScale * 2}px`,
              height: `${radius * outerScale * 2}px`,
              borderRadius: "50%",
              backgroundColor: "rgba(0, 0, 255, 0.2)",
            }}
          ></div>

          {/* Inner circle */}
          <div
            style={{
              position: "absolute",
              left: `${targetPoint.x - radius * innerScale}px`,
              top: `${targetPoint.y - radius * innerScale}px`,
              width: `${radius * innerScale * 2}px`,
              height: `${radius * innerScale * 2}px`,
              borderRadius: "50%",
              backgroundColor: "rgba(255, 255, 255, 0.5)",
            }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default ScatterFocusAdorner;
