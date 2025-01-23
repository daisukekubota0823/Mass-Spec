import { useState, useEffect } from "react";
import { FiFolder, FiMinus } from "react-icons/fi";
import ExcelJS from "exceljs";
import MolecularFormulaFinder from "../../components/MolecularFormulaFinder";
import StructuralFinder from "../../components/StructuralFinder";
import FileInformation from "../../components/FileInformation";
import { sendFile, getAllFiles, deleteFile, deleteAllFile } from "../../features/fileSlice"
import { useDispatch, useSelector } from 'react-redux';

export default function MSFinder() {
  const dispatch = useDispatch();
  const [importedData, setImportedData] = useState([]);
  const [files, setFiles] = useState([]);
  const [selectedFileData, setSelectedFileData] = useState(null);
  const [fileContent, setFileContent] = useState("");

  const allFiles = useSelector(state => state.files.allFiles);
  console.log(allFiles)
  const requiredFields = ["Spectrum Type", "Ion Mode", "Precursor m/z"];
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
  
    try {
      console.log("Starting file processing");
      const workbook = new ExcelJS.Workbook();
      await workbook.xlsx.load(file);
      console.log("File loaded successfully");
  
      const worksheet = workbook.worksheets[0];
      if (!worksheet) {
        throw new Error("No worksheet found in the Excel file");
      }
  
      const jsonData = [];
  
      worksheet.eachRow((row, rowNumber) => {
        if (rowNumber > 1) {
          const rowData = {};
          // let isValidRow = true;
          
          row.eachCell((cell, colNumber) => {
            const header = worksheet.getCell(1, colNumber).value;
            if (!header) {
              console.warn(`Missing header for column ${colNumber}`);
              return;
            }
            rowData[header] = cell.value;
            
            // if (requiredFields.includes(header) && !cell.value) {
            //   isValidRow = false;
            // }
          });
          
          // if (isValidRow) {
          jsonData.push(rowData);
          // }
        }
      });
  
      console.log(`Processed ${jsonData.length} rows`);
  
      // if (jsonData.length === 0) {
      //   throw new Error("No valid data found in the Excel file");
      // }
  
      const transformedData = jsonData.map(item => ({
        name: item.Name,
        SMILE: item.SMILE,
        spectrum_type: item["Spectrum Type *"],
        ion_mode: item["Ion Mode *"],
        precursor_type: item["Precursor Type"],
        inchikey: item.InChIKey,
        ontology: item.Ontology,
        collision_energy: item["Collision Energy"],
        precursor_mz: parseFloat(item["Precursor m/z *"]),
        retention_time: parseFloat(item["Retention Time (min)"]),
        instrument: item.Instrument,
        instrument_type: item["Instrument Type"],
        comment: item.Comment,
        sulfur_count: parseInt(item["Sulfur Count"]),
        nitrogen_count: parseInt(item["Nitrogen Count"]),
        carbon_count: parseInt(item["Carbon Count"]),
        peak_number_ms1: parseInt(item["Peak Number(ms1)"]),
        mstype_ms1_row1: item["MSType(ms1) Row1"],
        mstype_ms1_row2: item["MSType(ms1) Row2"],
        peak_number_ms2: parseInt(item["Peak Number(ms2)"]),
        mstype_ms2_row1: item["MSType(ms2) Row1"],
        mstype_ms2_row2: item["MSType(ms2) Row2"]
      }))[0]; // Take the first item from the array
  
      console.log("Dispatching sendFile action");
      console.log("transformedData:", JSON.stringify(transformedData));
      const result = await dispatch(sendFile( transformedData )).unwrap();
      console.log("Action result:", result);
  
    } catch (error) {
      console.error("Detailed error:", error);
    }
  };
  
  
  const handleSelectFile = async (fileId) => {
    const selectedFile = allFiles.find(file => file.id === fileId);
    setSelectedFileData(selectedFile);
  };

  const handleRemove = (fileId) => {
    dispatch(deleteFile(fileId));
  };

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


  const handleClearAll = () => {
    dispatch(deleteAllFile());
  };
  useEffect(() => {
    dispatch(getAllFiles());
  }, [dispatch]);
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
                  onChange={handleFileChange}
                  className="hidden"
                  id="fileInput"
                />
                <label htmlFor="fileInput" className="cursor-pointer bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition">
                  Choose File
                </label>
                <button
                  onClick={handleExport}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
                >
                  Export Template
                </button>
              </div>
            </div>
            <div className="mt-4 h-48 overflow-y-auto border border-gray-300 rounded-lg p-2">
              <ul className="list-disc list-inside">
                {allFiles && allFiles.map((file, index) => (
                
                  <li
                    key={file.id || index}
                    className="flex justify-between items-center text-gray-700 hover:bg-gray-100 transition-colors duration-200 cursor-pointer"
                    onClick={() => handleSelectFile(file.id)}
                  >
                    {file.name}
                    <button
                       onClick={() => handleRemove(file.id)}
                      className="ml-2 text-red-600 hover:text-red-800"
                    >
                      <FiMinus />
                    </button>
                  </li>
                ))}
              </ul>
            </div>
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
