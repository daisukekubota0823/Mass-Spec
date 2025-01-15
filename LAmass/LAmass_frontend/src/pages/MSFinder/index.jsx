import { useState } from "react";
import { FiFolder, FiSearch } from "react-icons/fi";

export default function MSFinder() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeFormulaNav, setActiveFormulaNav] = useState("Formula");
  const [activeStructuralNav, setActiveStructuralNav] = useState("Name");

  const formulaNavItems = [
    "Formula",
    "Error(mDa)",
    "Error(ppm)",
    "Score",
    "Resource",
    "Select",
  ];
  const structuralNavItems = ["Name", "Score (max=10)", "Ontology", "InChIKey"];

  // Dummy data for graphs
  const ms1Data = Array.from({ length: 50 }, (_, i) => ({
    x: i * 10,
    y: Math.sin(i * 0.2) * 50 + Math.random() * 20 + 50,
  }));

  const ms2Data = Array.from({ length: 50 }, (_, i) => ({
    x: i * 10,
    y: Math.cos(i * 0.2) * 40 + Math.random() * 15 + 40,
  }));

  const renderGraph = (data, title) => (
    <div className="h-48 bg-gray-100 rounded-lg p-4">
      <div className="h-full relative">
        <div className="absolute inset-0 flex items-end">
          {data.map((point, index) => (
            <div
              key={index}
              className="w-1 bg-primary mx-px"
              style={{
                height: `${point.y}%`,
                transition: "height 0.3s ease",
              }}
            />
          ))}
        </div>
        <div className="absolute top-2 left-2 text-sm font-medium text-gray-600">
          {title}
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-800">MS-FINDER</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-6">
          {/* File Navigator Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-medium text-gray-800 mb-4 flex items-center">
              <FiFolder className="mr-2" />
              File Navigator
            </h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <p className="text-gray-600">
                Drop files here or click to browse
              </p>
              <button
                type="button"
                className="mt-2 px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90"
              >
                Browse Files
              </button>
            </div>
          </div>

          {/* Molecular Formula Finder Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Molecular Formula Finder
            </h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {formulaNavItems.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setActiveFormulaNav(item)}
                  className={`px-4 py-2 rounded-md transition-colors ${
                    activeFormulaNav === item
                      ? "bg-primary text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
            <div className="mt-4 bg-white rounded-lg">
              <div className="p-4">
                <p className="text-gray-600">
                  Selected view: {activeFormulaNav}
                </p>
              </div>
            </div>
          </div>

          {/* Structural Finder Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Structural Finder
            </h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {structuralNavItems.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setActiveStructuralNav(item)}
                  className={`px-4 py-2 rounded-md transition-colors ${
                    activeStructuralNav === item
                      ? "bg-primary text-white"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
            <div className="mt-4 bg-white rounded-lg">
              <div className="p-4">
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                    <span>Glucose</span>
                    <span className="text-gray-600">9.5</span>
                  </div>
                  <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                    <span>Fructose</span>
                    <span className="text-gray-600">8.7</span>
                  </div>
                  <div className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                    <span>Sucrose</span>
                    <span className="text-gray-600">8.2</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* File Information Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              File Information
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Name
                </label>
                <input
                  type="text"
                  defaultValue="Sample_001"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Scan No
                </label>
                <input
                  type="text"
                  defaultValue="1234"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Retention Time (min)
                </label>
                <input
                  type="text"
                  defaultValue="5.67"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Precursor m/z
                </label>
                <input
                  type="text"
                  defaultValue="180.0634"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Precursor Type
                </label>
                <input
                  type="text"
                  defaultValue="[M+H]+"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Ion Mode
                </label>
                <input
                  type="text"
                  defaultValue="Positive"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Spectrum Type
                </label>
                <input
                  type="text"
                  defaultValue="MS2"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Collision Energy
                </label>
                <input
                  type="text"
                  defaultValue="20 eV"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">
                  Formula
                </label>
                <input
                  type="text"
                  defaultValue="C6H12O6"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">
                  Ontology
                </label>
                <input
                  type="text"
                  defaultValue="Carbohydrate"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">
                  SMILES
                </label>
                <input
                  type="text"
                  defaultValue="C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">
                  InChIKey
                </label>
                <input
                  type="text"
                  defaultValue="WQZGKKKJIJFFOK-GASJEMHNSA-N"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  MS1 Peak Number
                </label>
                <input
                  type="text"
                  defaultValue="45"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  MS2 Peak Number
                </label>
                <input
                  type="text"
                  defaultValue="32"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  readOnly
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">
                  Comment
                </label>
                <textarea
                  defaultValue="Sample analysis of glucose standard"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  rows="3"
                  readOnly
                />
              </div>
            </div>
          </div>

          {/* Mass Chromatogram Section */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Mass Chromatogram
            </h3>
            <div className="space-y-4">
              {renderGraph(ms1Data, "MS1 Spectrum")}
              {renderGraph(ms2Data, "MS2 Spectrum")}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
