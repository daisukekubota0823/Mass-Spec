import React from "react";

const CustomModal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity duration-300">
      <div className="bg-white w-full max-w-4xl rounded-xl shadow-lg p-6 relative animate-fadeIn">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-600 hover:text-gray-900 text-xl"
          aria-label="Close Modal"
        >
          &times;
        </button>
        <div className="modal-content space-y-4">{children}</div>
      </div>
    </div>
  );
};

export default CustomModal;
