import React, { useState, useRef } from 'react';

const SelectionBox = () => {
  const [isSelecting, setIsSelecting] = useState(false);
  const [selectionBox, setSelectionBox] = useState(null);
  const containerRef = useRef(null);

  const handleMouseDown = (event) => {
    const rect = containerRef.current.getBoundingClientRect();
    setSelectionBox({
      startX: event.clientX - rect.left,
      startY: event.clientY - rect.top,
      endX: event.clientX - rect.left,
      endY: event.clientY - rect.top,
    });
    setIsSelecting(true);
  };

  const handleMouseMove = (event) => {
    if (!isSelecting) return;

    const rect = containerRef.current.getBoundingClientRect();
    setSelectionBox((prev) => ({
      ...prev,
      endX: event.clientX - rect.left,
      endY: event.clientY - rect.top,
    }));
  };

  const handleMouseUp = () => {
    setIsSelecting(false);
  };

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '500px',
        border: '1px solid black',
        position: 'relative',
        overflow: 'hidden',
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
    >
      {selectionBox && (
        <div
          style={{
            position: 'absolute',
            left: Math.min(selectionBox.startX, selectionBox.endX),
            top: Math.min(selectionBox.startY, selectionBox.endY),
            width: Math.abs(selectionBox.endX - selectionBox.startX),
            height: Math.abs(selectionBox.endY - selectionBox.startY),
            backgroundColor: 'rgba(0, 0, 255, 0.3)',
            border: '1px solid blue',
          }}
        ></div>
      )}
    </div>
  );
};

export default SelectionBox;
