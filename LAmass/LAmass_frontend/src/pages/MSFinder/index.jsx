import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { FiFolder, FiMinus } from "react-icons/fi";
import { getAllFiles, deleteAllFile } from "../../features/fileSlice";
import { handleFileChange, handleExport, exportRetentionTimeStructure,exportCCSLibrary,exportRetentionTimeLibrary,exportUserDefinedStructure } from "./fileHandlers";
import FileList from "./FileList";
import MolecularFormulaFinder from "../../components/MolecularFormulaFinder";
import StructuralFinder from "../../components/StructuralFinder";
import FileInformation from "../../components/FileInformation";

export default function MSFinder() {
  const dispatch = useDispatch();
  const [selectedFileData, setSelectedFileData] = useState(null);
  const allFiles = useSelector(state => state.files.allFiles);

  useEffect(() => {
    dispatch(getAllFiles());
  }, [dispatch]);

  const handleSelectFile = (fileId) => {
    const selectedFile = allFiles.find(file => file.id === fileId);
    setSelectedFileData(selectedFile);
  };

  const handleClearAll = () => {
    dispatch(deleteAllFile());
  };

  return (
    <div className="space-y-6 p-6 bg-gray-100 min-h-screen">
      <h2 className="text-3xl font-bold text-purple-600">MS-FINDER</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-medium text-purple-600 mb-4 flex items-center">
              <FiFolder className="mr-2" />
              File Navigator
            </h3>
            <div className="border-2 border-dashed border-purple-300 rounded-lg p-6 text-center">
              <p className="text-gray-600">Drop files here or click to browse</p>
              <div className="flex justify-center space-x-4 mt-2">
                <input
                  type="file"
                  accept=".xlsx, .xls"
                  onChange={(e) => handleFileChange(e, dispatch)}
                  className="hidden"
                  id="fileInput"
                />
        <label htmlFor="fileInput" className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition w-full sm:w-48">
      Choose File
    </label>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 w-full">
      <button
        onClick={handleExport}
        className="px-2 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-sm"
      >
        Export MS/MS
      </button>
      <button
        onClick={exportRetentionTimeStructure}
        className="px-2 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-sm"
      >
        Export RT Structure
      </button>
      <button
        onClick={exportCCSLibrary}
        className="px-2 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-sm"
      >
        Export CCS Library
      </button>
      <button
        onClick={exportRetentionTimeLibrary}
        className="px-2 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-sm"
      >
        Export RT Library
      </button>
      <button
        onClick={exportUserDefinedStructure}
        className="px-2 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition text-sm"
      >
        Export User Structure
      </button>
    </div>
              </div>
            </div>
            <FileList 
              files={allFiles} 
              onSelectFile={handleSelectFile} 
            />
            {allFiles.length > 0 && (
              <button
                onClick={handleClearAll}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
              >
                Remove All
              </button>
            )}
          </div>
          <MolecularFormulaFinder />
          <StructuralFinder />
        </div>
        <div className="space-y-6">
          <FileInformation fileData={selectedFileData} />
        </div>
      </div>
    </div>
  );
}
