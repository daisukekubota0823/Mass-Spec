import { useState } from "react";
import { FiFolder, FiMinus } from "react-icons/fi";
import ExcelJS from "exceljs";
import  MolecularFormulaFinder from "../../components/MolecularFormulaFinder"
import StructuralFinder from "../../components/StructuralFinder"
import FileInformation from "../../components/FileInformation";

export default function MSFinder() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = () => setIsModalOpen(!isModalOpen);
  const [importedData, setImportedData] = useState([]);
  const [files, setFiles] = useState([]);
  const [selectedFileData, setSelectedFileData] = useState(null); // State for selected file data
  const [fileContent, setFileContent] = useState(""); // New state for file content

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const workbook = new ExcelJS.Workbook();
      await workbook.xlsx.load(file); // Load the selected file

      const worksheet = workbook.worksheets[0]; // Get the first worksheet
      const jsonData = [];

      // Read data into JSON format
      worksheet.eachRow((row, rowNumber) => {
        if (rowNumber > 1) {
          // Skip header row
          const rowData = {};
          row.eachCell((cell, colNumber) => {
            rowData[worksheet.getCell(1, colNumber).value] = cell.value; // Use header as key
          });
          jsonData.push(rowData);
        }
      });

      // Validate and generate unique filenames
      const validDataWithNames = jsonData
        .map((row) => {
          if (row["Name"]) {
            // Assuming "Name" is the column to be used for filename
            return {
              ...row,
              uniqueFileName: `${row["Name"]}_${Date.now()}.xlsx`, // Create a unique filename
            };
          }
          return null; // Skip rows without a name
        })
        .filter(Boolean); // Remove null entries
      if (validDataWithNames.length > 0) {
        setImportedData((prev) => [...prev, ...validDataWithNames]); // Append valid data to state
        setFiles((prev) => [
          ...prev,
          ...validDataWithNames.map((item) => item.uniqueFileName),
        ]); // Append filenames to state
      } else {
        alert("Imported data is invalid. Please check the required fields.");
      }
    }
  };

// Function to handle selecting a file and populating its data
const handleSelectFile = async (fileIndex) => {
  const selectedFile = importedData[fileIndex]; // Get the corresponding data for the selected file
  setSelectedFileData(selectedFile); // Set the selected file data in state
  
  // Read the content of the file
  const fileName = selectedFile.uniqueFileName; // Assuming uniqueFileName is stored in importedData
  const response = await fetch(`path/to/your/files/${fileName}`); // Adjust this path as needed
  const blob = await response.blob();
  
  if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
      const workbook = new ExcelJS.Workbook();
      await workbook.xlsx.load(blob);
      const worksheet = workbook.worksheets[0];
      let content = "";
      worksheet.eachRow((row) => {
          row.eachCell((cell) => {
              content += `${cell.value}\t`; // Append cell values separated by tabs
          });
          content += "\n"; // New line after each row
      });
      setFileContent(content);
  } else if (fileName.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (e) => {
          setFileContent(e.target.result); // Set text content
      };
      reader.readAsText(blob);
  }
};

  // Function to remove a specific file
  const handleRemove = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    setFiles(newFiles);
  };
  // Function to handle file export (placeholder)
  const handleExport = async () => {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet("Mass Spectrometry Data");

    // Define headers with required fields marked with *
    const headers = [
      "Name",
      "SMILE",
      "Spectrum Type *", // Required
      "Ion Mode *", // Required
      "Precursor Type",
      "InChIKey",
      "Ontology",
      "Collision Energy",
      "Precursor m/z *", // Required
      "Retention Time (min)",
      "Instrument",
      "Instrument Type",
      "Comment",
      "Sulfur Count",
      "Nitrogen Count",
      "Carbon Count",
      "Peak Number(ms1)",
      "MSType(ms1) Row1",
      "MSType(ms1) Row2",
      "Peak Number(ms2)",
      "MSType(ms2) Row1",
      "MSType(ms2) Row2",
    ];

    // Define dropdown options for Spectrum Type and Ion Mode
    const spectrumTypes = [
      "Centroid",
      "Profile",
      "MS/MS:",
      "Full Scan",
      "SIM/SIM",
    ];
    const ionModes = [
      "Positive",
      "Negative",
      "Neutral Loss",
      "CID",
      "HCD",
      "APCI",
      "MALDI",
    ];

    // Add header row with styles
    const headerRow = worksheet.addRow(headers);

    // Apply styles to the header row
    headerRow.eachCell((cell, colNumber) => {
      cell.font = { bold: true, color: { argb: "FFFFFFFF" } }; // White text
      cell.fill = {
        type: "pattern",
        pattern: "solid",
        fgColor: { argb: "FFCC00FF" }, // Light purple background
        bgColor: { argb: "FFCC00FF" },
      };

      // Highlight required fields with red background
      if (headers[colNumber - 1].includes("*")) {
        cell.fill = {
          type: "pattern",
          pattern: "solid",
          fgColor: { argb: "FFFF0000" }, // Red for required fields
          bgColor: { argb: "FFFF0000" },
        };
      }
    });

    // Add dropdowns for Spectrum Type and Ion Mode columns (columns C and D)
    worksheet.getColumn(3).eachCell((cell, rowNumber) => {
      if (rowNumber > 1) {
        // Skip header row
        cell.dataValidation = {
          type: "list",
          allowBlank: false,
          formula1: `"${spectrumTypes.join(",")}"`, // Join options with commas
          showErrorMessage: true,
          errorTitle: "Invalid Input",
          error: "Please select a valid Spectrum Type from the dropdown.",
        };
      }
    });

    worksheet.getColumn(4).eachCell((cell, rowNumber) => {
      if (rowNumber > 1) {
        // Skip header row
        cell.dataValidation = {
          type: "list",
          allowBlank: false,
          formula1: `"${ionModes.join(",")}"`, // Join options with commas
          showErrorMessage: true,
          errorTitle: "Invalid Input",
          error: "Please select a valid Ion Mode from the dropdown.",
        };
      }
    });

    // Adjust column widths dynamically based on header length
    worksheet.columns.forEach((column, index) => {
      column.width = headers[index].length + 5; // Dynamic width based on header length
    });

    // Freeze header row
    worksheet.views = [{ state: "frozen", ySplit: 1 }];

    // Add example data (optional)
    const exampleData = [
      "Sample Name",
      "C1=CC=CC=C1",
      "MS",
      "Positive",
      "[M+H]+",
      "ABCDEFGHIJK",
      "Organic Compound",
      "30 eV",
      "100.2",
      "2.3",
      "Instrument A",
      "Type B",
      "Example comment",
      "2",
      "1",
      "6",
      "10",
      "Type 1A",
      "Type 1B",
      "20",
      "Type 2A",
      "Type 2B",
    ];
    worksheet.addRow(exampleData);

    // Export logic with error handling
    try {
      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: "application/octet-stream" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "Mass_Spectrometry_Template.xlsx";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error exporting Excel file:", error);
      alert("Failed to export the Excel file. Please try again.");
    }
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
              <p className="text-gray-600">
                Drop files here or click to browse
              </p>
              <div className="flex justify-center space-x-4 mt-2">
                <input
                  type="file"
                  accept=".xlsx, .xls"
                  onChange={handleFileChange}
                  className="h"
                  id="fileInput"
                />
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
              <div className="mt-4 h-48 overflow-y-auto border border-gray-300 rounded-lg p-2">
              <ul className="list-disc list-inside">
                        {files.map((file, index) => (
                            <li key={index} className="flex justify-between items-center text-gray-700 hover:bg-gray-100 transition-colors duration-200 cursor-pointer" onClick={() => handleSelectFile(index)}>
                                {file}
                                <button type="button" onClick={() => handleRemove(index)} className="ml-2 text-red-600 hover:text-red-800">
                                    <FiMinus />
                                </button>
                            </li>
                        ))}
                    </ul>
              </div>
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
            < MolecularFormulaFinder/>

          {/* Structural Finder Section */}
              <StructuralFinder/>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* File Information Section */}
          { <FileInformation fileData={selectedFileData} />}
        </div>
      </div>
    </div>
  );
}
