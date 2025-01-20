import React, { useState, useEffect } from "react";

export default function FileInformation({ fileData }) {
  // State to hold editable field values
  const [formData, setFormData] = useState({
    name: "",
    scanNo: "",
    retentionTime: "",
    precursorMz: "",
    collisionEnergy: "",
    formula: "",
    ontology: "",
    smiles: "",
    inchiKey: "",
    ms1PeakNumber: "",
    ms2PeakNumber: "",
    comment: "",
    precursorType: "[M+H]+",
    ionMode: "Positive",
    spectrumType: "MS2",
  });

  // Effect to populate form data when fileData changes
  useEffect(() => {
    if (fileData) {
      setFormData({
        name: fileData.name || "",
        scanNo: fileData.scanNo || "",
        retentionTime: fileData.retentionTime || "",
        precursorMz: fileData.precursorMz || "",
        collisionEnergy: fileData.collisionEnergy || "",
        formula: fileData.formula || "",
        ontology: fileData.ontology || "",
        smiles: fileData.smiles || "",
        inchiKey: fileData.inchiKey || "",
        ms1PeakNumber: fileData.ms1PeakNumber || "",
        ms2PeakNumber: fileData.ms2PeakNumber || "",
        comment: fileData.comment || "",
        precursorType: "[M+H]+", // Default value
        ionMode: "Positive", // Default value
        spectrumType: "MS2", // Default value
      });
    }
  }, [fileData]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <>
      {/* File Information Section */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-medium text-purple-600 mb-4">File Information</h3>

        <div className="grid grid-cols-2 gap-x-4 gap-y-6">
          {[
            { label: "Name", name: "name" },
            { label: "Scan No", name: "scanNo" },
            { label: "Retention Time (min)", name: "retentionTime" },
            { label: "Precursor m/z", name: "precursorMz" },
            { label: "Collision Energy", name: "collisionEnergy" },
            { label: "Formula", name: "formula" },
            { label: "Ontology", name: "ontology" },
            { label: "SMILES", name: "smiles" },
            { label: "InChIKey", name: "inchiKey" },
            { label: "MS1 Peak Number", name: "ms1PeakNumber" },
            { label: "MS2 Peak Number", name: "ms2PeakNumber" },
            {
              label: "Comment",
              name: "comment",
              isTextArea: true,
            },
          ].map(({ label, name, isTextArea }, index) =>
            isTextArea ? (
              <div key={index} className="col-span-full">
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <textarea
                  value={formData[name]}
                  onChange={handleChange}
                  rows={3}
                  className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200"
                />
              </div>
            ) : (
              <div key={index}>
                <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
                <input
                  type="text"
                  name={name}
                  value={formData[name]}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200"
                />
              </div>
            )
          )}

          {/* Dropdowns for Precursor Type, Ion Mode, and Spectrum Type */}
          {[
            {
              label: "Precursor Type",
              options: ["[M+H]+", "[M-H]-", "[M+Na]+"],
              valueName: "precursorType",
            },
            {
              label: "Ion Mode",
              options: ["Positive", "Negative"],
              valueName: "ionMode",
            },
            {
              label: "Spectrum Type",
              options: ["MS1", "MS2"],
              valueName: "spectrumType",
            },
          ].map(({ label, options, valueName }, index) => (
            <div key={index}>
              <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
              <select
                name={valueName}
                value={formData[valueName]}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200"
              >
                {options.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
