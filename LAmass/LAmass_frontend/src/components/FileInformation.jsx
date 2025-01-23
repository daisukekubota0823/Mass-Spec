import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { updateFile } from "../features/fileSlice";

export default function FileInformation({ fileData }) {
  const dispatch = useDispatch();

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

  useEffect(() => {
    if (fileData) {
      setFormData({
        name: fileData.name || "",
        scanNo: fileData.scanNo || "",
        retentionTime: fileData.retention_time || "",
        precursorMz: fileData.precursor_mz || "",
        collisionEnergy: fileData.collision_energy || "",
        formula: fileData.formula || "",
        ontology: fileData.ontology || "",
        smiles: fileData.SMILE || "",
        inchiKey: fileData.inchikey || "",
        ms1PeakNumber: fileData.peak_number_ms1 || "",
        ms2PeakNumber: fileData.peak_number_ms2 || "",
        comment: fileData.comment || "",
        precursorType: fileData.precursor_type || "[M+H]+",
        ionMode: fileData.ion_mode || "Positive",
        spectrumType: fileData.spectrum_type || "MS2",
      });
    }
  }, [fileData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (fileData && fileData.id) {
      const transformedData = {
        id: fileData.id,
        name: formData.name,
        SMILE: formData.smiles,
        spectrum_type: formData.spectrumType,
        ion_mode: formData.ionMode,
        precursor_type: formData.precursorType,
        inchikey: formData.inchiKey,
        ontology: formData.ontology,
        collision_energy: formData.collisionEnergy,
        precursor_mz: parseFloat(formData.precursorMz),
        retention_time: parseFloat(formData.retentionTime),
        instrument: formData.instrument,
        instrument_type: formData.instrumentType,
        comment: formData.comment,
        sulfur_count: parseInt(formData.sulfurCount),
        nitrogen_count: parseInt(formData.nitrogenCount),
        carbon_count: parseInt(formData.carbonCount),
        peak_number_ms1: parseInt(formData.ms1PeakNumber),
        mstype_ms1_row1: formData.mstype_ms1_row1,
        mstype_ms1_row2: formData.mstype_ms1_row2,
        peak_number_ms2: parseInt(formData.ms2PeakNumber),
        mstype_ms2_row1: formData.mstype_ms2_row1,
        mstype_ms2_row2: formData.mstype_ms2_row2
      };
  
      dispatch(updateFile(transformedData));
    }
  };
  

  return (
    <form onSubmit={handleSubmit}>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-medium text-purple-600 mb-4">File Information</h3>
        <div className="grid grid-cols-2 gap-x-4 gap-y-6">
          {/* Render input fields */}
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
          {/* Dropdowns */}
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
                {options.map(option => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
          ))}
        </div>
        <button
          type="submit"
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
        >
          Save Changes
        </button>
      </div>
    </form>
  );
}
