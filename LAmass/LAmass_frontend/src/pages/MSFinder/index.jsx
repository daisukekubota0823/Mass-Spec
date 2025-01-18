import { useState } from 'react';
import { FiFolder, FiMinus } from 'react-icons/fi';
import { Chart } from "react-chartjs-2";
import CustomModal from "../../components/CustomModal";


export default function MSFinder() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [activeFormulaNav, setActiveFormulaNav] = useState("Formula");
  const [activeStructuralNav, setActiveStructuralNav] = useState("Name");
   const [isModalOpen, setIsModalOpen] = useState(false);
  
    const toggleModal = () => setIsModalOpen(!isModalOpen);
  
    // Sample Data for Isotopic Ions Chart
    const isotopicData = {
      labels: ["C12", "C13", "O16", "O17", "O18"],
      datasets: [
        {
          label: "Isotopic Ions",
          data: [12, 3, 15, 2, 1],
          backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
        },
      ],
    };
  
    // Sample Data for MS/MS Spectrum Chart
    const msmsData = {
      labels: [50, 100, 150, 200, 250],
      datasets: [
        {
          label: "MS/MS Spectrum",
          data: [10, 20, 15, 40, 30],
          borderColor: "#FF5733",
          borderWidth: 2,
          fill: false,
        },
      ],
    };

  const formulaNavItems = [
    "Formula",
    "Error(mDa)",
    "Error(ppm)",
    "Score",
    "Resource",
    "Select",
  ];
  
  const files = [
    "Query-1415_MT_flower_Neg-1172",
    "Query-1416_MT_tree_Neg-1173",
    "Query-1417_MT_sky_Neg-1174",
    "Query-1418_MT_mountain_Neg-1175",
    "Query-1419_MT_river_Neg-1176",
    "Query-1420_MT_lake_Neg-1177",
    "Query-1421_MT_grass_Neg-1178",
    "Query-1422_MT_sunset_Neg-1179",
    "Query-1423_MT_ocean_Neg-1180",
    "Query-1424_MT_desert_Neg-1181"
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
    <div className="h-48 bg-gradient-to-r from-blue-400 to-purple-500 rounded-lg p-4 shadow-lg">
      <div className="h-full relative">
        <div className="absolute inset-0 flex items-end">
          {data.map((point, index) => (
            <div
              key={index}
              className="w-1 bg-white mx-px"
              style={{
                height: `${point.y}%`,
                transition: "height 0.3s ease",
              }}
            />
          ))}
        </div>
        <div className="absolute top-2 left-2 text-sm font-medium text-white">
          {title}
        </div>
      </div>
    </div>
  );

  // Function to remove a specific file
  const handleRemove = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
  };
  // Function to handle file export (placeholder)
  const handleExport = () => {
    alert('Exporting files...');
  };
  // Function to remove all files
  const handleClearAll = () => {
    setFiles([]);
  };
  return (
    <div className="space-y-6 p-6 bg-gray-100 min-h-screen">
      <h2 className="text-3xl font-bold text-purple-600">MS-FINDER</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-6">
          {/* File Navigator Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-medium text-purple-600 mb-4 flex items-center">
        <FiFolder className="mr-2" />
        File Navigator
      </h3>
      <div className="border-2 border-dashed border-purple-300 rounded-lg p-6 text-center">
        <p className="text-gray-600">Drop files here or click to browse</p>
        <div className="flex justify-center space-x-4 mt-2">
          <button
            type="button"
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition"
          >
            Import Files
          </button>
          <button
            type="button"
            onClick={handleExport}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Export Files
          </button>
        </div>
      </div>
      <div className="mt-4 h-48 overflow-y-auto border border-gray-300 rounded-lg p-2">
        <ul className="list-disc list-inside">
          {files.map((file, index) => (
            <li 
              key={index} 
              className="flex justify-between items-center text-gray-700 hover:bg-gray-100 transition-colors duration-200"
            >
              {file}
              <button 
                type="button" 
                onClick={() => handleRemove(index)} 
                className="ml-2 text-red-600 hover:text-red-800"
              >
                <FiMinus />
              </button>
            </li>
          ))}
        </ul>
      </div>
      {files.length > 0 && (
        <button 
          type="button" 
          onClick={handleClearAll} 
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
        >
          Remove All
        </button>
      )}
    </div>

 {/* Molecular Formula Finder Section */}
{/* Molecular Formula Finder Section */}
<div className="bg-white rounded-lg shadow-lg p-6">
  <div  className='flex'>
  <h3 className="text-lg font-medium text-purple-600 mb-4 mr-5">Molecular Formula Finder</h3>
  <button
  onClick={toggleModal}
  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 text-sm rounded-md shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300"
>
  Chart
</button>
  </div>
      
  <div className="overflow-auto max-h-64">
    <table className="min-w-full border-collapse border border-gray-300">
      <thead className="sticky top-0 bg-purple-100 text-purple-600">
        <tr>
          <th className="border border-gray-300 px-4 py-2">Select</th>
          <th className="border border-gray-300 px-4 py-2">Formula</th>
          <th className="border border-gray-300 px-4 py-2">Error (mDa)</th>
          <th className="border border-gray-300 px-4 py-2">Error (ppm)</th>
          <th className="border border-gray-300 px-4 py-2">Score</th>
          <th className="border border-gray-300 px-4 py-2">Resource</th>
        </tr>
      </thead>
      <tbody>
        {/* Dummy data rows */}
        {[
          { formula: 'C6H12O6', error_mDa: '0.5', error_ppm: '1.0', score: '9.5', resource: 'Database A' },
          { formula: 'C12H22O11', error_mDa: '1.0', error_ppm: '1.5', score: '8.7', resource: 'Database B' },
          { formula: 'C5H10O5', error_mDa: '0.7', error_ppm: '1.3', score: '8.9', resource: 'Database C' },
          { formula: 'C3H6O3', error_mDa: '0.3', error_ppm: '0.8', score: '9.0', resource: 'Database D' },
          { formula: 'C6H12O6', error_mDa: '0.5', error_ppm: '1.0', score: '9.5', resource: 'Database A' },
          { formula: 'C12H22O11', error_mDa: '1.0', error_ppm: '1.5', score: '8.7', resource: 'Database B' },
          { formula: 'C5H10O5', error_mDa: '0.7', error_ppm: '1.3', score: '8.9', resource: 'Database C' },
          { formula: 'C3H6O3', error_mDa: '0.3', error_ppm: '0.8', score: '9.0', resource: 'Database D' },
        ].map((row, index) => (
          <tr key={index} className="hover:bg-gray-50">
            <td className="border border-gray-300 px-4 py-2 text-center">
              <input type="checkbox" />
            </td>
            <td className="border border-gray-300 px-4 py-2">{row.formula}</td>
            <td className="border border-gray-300 px-4 py-2">{row.error_mDa}</td>
            <td className="border border-gray-300 px-4 py-2">{row.error_ppm}</td>
            <td className="border border-gray-300 px-4 py-2">{row.score}</td>
            <td className="border border-gray-300 px-4 py-2">{row.resource}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>


{/* Structural Finder Section */}
<div className="bg-white rounded-lg shadow-lg p-6 mt-6">
 
  <div className='flex'> 
    <h3 className="text-lg font-medium text-purple-600 mb-4">Structural Finder</h3>
  <button
  onClick={toggleModal}
  className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 text-sm rounded-md shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-300"
>
  Chart
</button>
  </div>
  <div className="overflow-auto max-h-64">
    <table className="min-w-full border-collapse border border-gray-300">
      <thead className="sticky top-0 bg-purple-100 text-purple-600">
        <tr>
          <th className="border border-gray-300 px-4 py-2">Name</th>
          <th className="border border-gray-300 px-4 py-2">Score (max=10)</th>
          <th className="border border-gray-300 px-4 py-2">Ontology</th>
          <th className="border border-gray-300 px-4 py-2">InChIKey</th>
        </tr>
      </thead>
      <tbody>
        {/* Dummy data rows */}
        {[
          { name: 'Glucose', score: '9.5', ontology: 'Carbohydrate', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Fructose', score: '8.7', ontology: 'Carbohydrate', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Sucrose', score: '8.9', ontology: 'Disaccharide', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Lactose', score: '8.0', ontology: 'Disaccharide', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Glucose', score: '9.5', ontology: 'Carbohydrate', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Fructose', score: '8.7', ontology: 'Carbohydrate', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Sucrose', score: '8.9', ontology: 'Disaccharide', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
          { name: 'Lactose', score: '8.0', ontology: 'Disaccharide', inchiKey: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
        ].map((row, index) => (
          <tr key={index} className="hover:bg-gray-50">
            <td className="border border-gray-300 px-4 py-2">{row.name}</td>
            <td className="border border-gray-300 px-4 py-2">{row.score}</td>
            <td className="border border-gray-300 px-4 py-2">{row.ontology}</td>
            <td className="border border-gray-300 px-4 py-2">{row.inchiKey}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>
</div>


        {/* Right Column */}
        <div className="space-y-6">
          {/* File Information Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-medium text-purple-600 mb-4">File Information</h3>
            
<div className="grid grid-cols-2 gap-x-4 gap-y-6">
  {[
    { label: 'Name', value: 'Sample_001' },
    { label: 'Scan No', value: '1234' },
    { label: 'Retention Time (min)', value: '5.67' },
    { label: 'Precursor m/z', value: '180.0634' },
    { label: 'Collision Energy', value: '20 eV' },
    { label: 'Formula', value: 'C6H12O6' },
    { label: 'Ontology', value: 'Carbohydrate' },
    { label: 'SMILES', value: 'C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O' },
    { label: 'InChIKey', value: 'WQZGKKKJIJFFOK-GASJEMHNSA-N' },
    { label: 'MS1 Peak Number', value: '45' },
    { label: 'MS2 Peak Number', value: '32' },
    { label: 'Comment', value: 'Sample analysis of glucose standard', isTextArea: true }
  ].map(({ label, value, isTextArea }, index) => (
    isTextArea ? (
      <div key={index} className="col-span-full">
        <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
        <textarea defaultValue={value} rows={3} readOnly 
          className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200" />
      </div>
    ) : (
      <div key={index}>
        <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
        <input type="text" defaultValue={value} readOnly 
          className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200" />
      </div>
    )
  ))}
  
  {/* Dropdowns for Precursor Type, Ion Mode, and Spectrum Type */}
  {[
    {
      label: 'Precursor Type',
      options: ['[M+H]+', '[M-H]-', '[M+Na]+'],
      defaultValue: '[M+H]+'
    },
    {
      label: 'Ion Mode',
      options: ['Positive', 'Negative'],
      defaultValue: 'Positive'
    },
    {
      label: 'Spectrum Type',
      options: ['MS1', 'MS2'],
      defaultValue: 'MS2'
    }
  ].map(({ label, options, defaultValue }, index) => (
    <div key={index}>
      <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>
      <select defaultValue={defaultValue} 
        className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm focus:ring focus:ring-purple-500 focus:border-purple-500 transition duration-200" readOnly>
        {options.map(option => (
          <option key={option} value={option}>{option}</option>
        ))}
      </select>
    </div>
  ))}
</div>
          </div>

          {/* Mass Chromatogram Section */}
          <div className="bg-white rounded-lg shadow-lg p6">
            <h3 className="text-lg font-medium text-purple600 mb4">Mass Chromatogram</h3>
            <div className="space-y4">
              {renderGraph(ms1Data, "MS1 Spectrum")}
              {renderGraph(ms2Data, "MS2 Spectrum")}
            </div>
          </div>
        </div> 
      </div> 
    </div> 
  ); 
}
