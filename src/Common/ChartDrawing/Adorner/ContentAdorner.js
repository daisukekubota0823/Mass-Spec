import React, { useState, useEffect, useRef } from "react";

const ContentAdorner = ({
  adornedElementId,
  content,
  alignment = "top-center",
  targetPoint = null,
  targetRadius = 0,
}) => {
  const [isAttached, setIsAttached] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const contentRef = useRef(null);

  useEffect(() => {
    if (adornedElementId && targetPoint) {
      const adornedElement = document.getElementById(adornedElementId);
      if (adornedElement) {
        const updatePosition = () => {
          const rect = adornedElement.getBoundingClientRect();
          const contentSize = contentRef.current.getBoundingClientRect();
          const { top, left } = calculatePosition(
            rect,
            contentSize,
            targetPoint,
            alignment,
            targetRadius
          );
          setPosition({ top, left });
        };

        updatePosition();
        setIsAttached(true);

        // Update position on window resize
        window.addEventListener("resize", updatePosition);
        return () => {
          window.removeEventListener("resize", updatePosition);
        };
      }
    }
  }, [adornedElementId, targetPoint, alignment, targetRadius]);

  const calculatePosition = (rect, contentSize, targetPoint, alignment, radius) => {
    const centerX = rect.left + targetPoint.x;
    const centerY = rect.top + targetPoint.y;
    const width = contentSize.width;
    const height = contentSize.height;

    let top = 0;
    let left = 0;

    switch (alignment) {
      case "top-left":
        top = centerY - height - radius;
        left = centerX - width - radius;
        break;
      case "top-center":
        top = centerY - height - radius;
        left = centerX - width / 2;
        break;
      case "top-right":
        top = centerY - height - radius;
        left = centerX + radius;
        break;
      case "middle-left":
        top = centerY - height / 2;
        left = centerX - width - radius;
        break;
      case "middle-center":
        top = centerY - height / 2;
        left = centerX - width / 2;
        break;
      case "middle-right":
        top = centerY - height / 2;
        left = centerX + radius;
        break;
      case "bottom-left":
        top = centerY + radius;
        left = centerX - width - radius;
        break;
      case "bottom-center":
        top = centerY + radius;
        left = centerX - width / 2;
        break;
      case "bottom-right":
        top = centerY + radius;
        left = centerX + radius;
        break;
      default:
        top = centerY;
        left = centerX;
    }

    return { top, left };
  };

  if (!isAttached) {
    return null;
  }

  return (
    <div
      ref={contentRef}
      style={{
        position: "absolute",
        top: `${position.top}px`,
        left: `${position.left}px`,
        pointerEvents: "none", // Disable interaction
        backgroundColor: "rgba(255, 255, 255, 0.8)", // Example styling
        padding: "5px",
        border: "1px solid black",
      }}
    >
      {content}
    </div>
  );
};

export default ContentAdorner;
