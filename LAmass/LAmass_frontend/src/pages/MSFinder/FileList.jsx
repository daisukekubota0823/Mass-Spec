import React from 'react';
import { FiMinus } from "react-icons/fi";

const FileList = ({ files, onSelectFile, onRemoveFile }) => {
  return (
    <div className="mt-4 h-48 overflow-y-auto border border-gray-300 rounded-lg p-2">
      <ul className="list-disc list-inside">
        {files && files.map((file, index) => (
          <li
            key={file.id || index}
            className="flex justify-between items-center text-gray-700 hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
            onClick={() => onSelectFile(file.id)}
          >
            {file.name}
            <button
              onClick={() => onRemoveFile(file.id)}
              className="ml-2 text-red-600 hover:text-red-800"
            >
              <FiMinus />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FileList;
