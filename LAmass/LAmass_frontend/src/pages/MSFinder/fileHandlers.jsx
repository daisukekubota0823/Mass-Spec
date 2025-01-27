import ExcelJS from "exceljs";
import { sendFile } from "../../features/fileSlice";

export const handleFileChange = async (event, dispatch) => {
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
        row.eachCell((cell, colNumber) => {
          const header = worksheet.getCell(1, colNumber).value;
          if (!header) {
            console.warn(`Missing header for column ${colNumber}`);
            return;
          }
          rowData[header] = cell.value;
        });
        jsonData.push(rowData);
      }
    });

    console.log(`Processed ${jsonData.length} rows`);

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
    }))[0];

    console.log("Dispatching sendFile action");
    console.log("transformedData:", JSON.stringify(transformedData));
    const result = await dispatch(sendFile(transformedData)).unwrap();
    console.log("Action result:", result);

  } catch (error) {
    console.error("Detailed error:", error);
  }
};

export const handleExport = async () => {
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


// Helper function to export Excel file
const exportExcel = async (worksheetData, fileName) => {
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet(worksheetData.name);
  
    // Add headers
    worksheet.addRow(worksheetData.columns.map(col => col.header));
  
    // Set column keys
    worksheetData.columns.forEach((col, index) => {
      worksheet.getColumn(index + 1).key = col.key;
    });
  
    try {
      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: "application/octet-stream" });
      const url = window.URL.createObjectURL(blob);
  
      const a = document.createElement("a");
      a.href = url;
      a.download = fileName;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(`Error exporting ${fileName}:`, error);
      alert(`Failed to export ${fileName}. Please try again.`);
    }
  };

// Export functions for each file type
export const exportMSP = async () => {
  const worksheet = {
    name: "MSP Format",
    columns: [
      { header: "NAME", key: "name" },
      { header: "PRECURSORMZ", key: "precursorMz" },
      { header: "PRECURSORTYPE", key: "precursorType" },
      { header: "FORMULA", key: "formula" },
      { header: "ONTOLOGY", key: "ontology" },
      { header: "INCHIKEY", key: "inchikey" },
      { header: "SMILES", key: "smiles" },
      { header: "RETENTIONTIME", key: "retentionTime" },
      { header: "IONMODE", key: "ionMode" },
      { header: "COLLISIONENERGY", key: "collisionEnergy" },
      { header: "COMMENT", key: "comment" },
      { header: "Num Peaks", key: "numPeaks" },
      { header: "m/z", key: "mz" },
      { header: "intensity", key: "intensity" }
    ]
  };
  await exportExcel(worksheet, "MSP_Format_Template.xlsx");
};

export const exportMAT = async () => {
  const worksheet = {
    name: "MAT Format",
    columns: [
      { header: "Name", key: "name" },
      { header: "PrecursorMz", key: "precursorMz" },
      { header: "Formula", key: "formula" },
      { header: "InChIKey", key: "inchikey" },
      { header: "SMILES", key: "smiles" },
      { header: "RetentionTime", key: "retentionTime" },
      { header: "IonMode", key: "ionMode" },
      { header: "CollisionEnergy", key: "collisionEnergy" },
      { header: "FragmentMz", key: "fragmentMz" },
      { header: "FragmentIntensity", key: "fragmentIntensity" }
    ]
  };
  await exportExcel(worksheet, "MAT_Format_Template.xlsx");
};

export const exportMATElementsFix = async () => {
  const worksheet = {
    name: "MAT Elements-Fix",
    columns: [
      { header: "Name", key: "name" },
      { header: "PrecursorMz", key: "precursorMz" },
      { header: "Formula", key: "formula" },
      { header: "InChIKey", key: "inchikey" },
      { header: "SMILES", key: "smiles" },
      { header: "RetentionTime", key: "retentionTime" },
      { header: "IonMode", key: "ionMode" },
      { header: "CollisionEnergy", key: "collisionEnergy" },
      { header: "FragmentMz", key: "fragmentMz" },
      { header: "FragmentIntensity", key: "fragmentIntensity" },
      { header: "ElementsFix", key: "elementsFix" }
    ]
  };
  await exportExcel(worksheet, "MAT_Elements_Fix_Template.xlsx");
};

export const exportUserDefinedStructure = async () => {
  const worksheet = {
    name: "User Defined Structure",
    columns: [
      { header: "Title", key: "title" },
      { header: "InChIKey", key: "inchikey" },
      { header: "ShortInChIKey", key: "shortInchikey" },
      { header: "PubChemCID", key: "pubchemCid" },
      { header: "ExactMass", key: "exactMass" },
      { header: "Formula", key: "formula" },
      { header: "SMILES", key: "smiles" },
      { header: "DatabaseID", key: "databaseId" }
    ]
  };
  await exportExcel(worksheet, "User_Defined_Structure_Template.xlsx");
};

export const exportRetentionTimeLibrary = async () => {
  const worksheet = {
    name: "Retention Time Library",
    columns: [
      { header: "CompoundName", key: "compoundName" },
      { header: "InChIKey", key: "inchikey" },
      { header: "RetentionTime", key: "retentionTime" }
    ]
  };
  await exportExcel(worksheet, "Retention_Time_Library_Template.xlsx");
};

export const exportCCSLibrary = async () => {
  const worksheet = {
    name: "CCS Library",
    columns: [
      { header: "CompoundName", key: "compoundName" },
      { header: "InChIKey", key: "inchikey" },
      { header: "Adduct", key: "adduct" },
      { header: "CCS", key: "ccs" }
    ]
  };
  await exportExcel(worksheet, "CCS_Library_Template.xlsx");
};

export const exportRetentionTimeStructure = async () => {
  const worksheet = {
    name: "RT Structure Prediction",
    columns: [
      { header: "MetaboliteName", key: "metaboliteName" },
      { header: "RetentionTime", key: "retentionTime" },
      { header: "SMILES", key: "smiles" }
    ]
  };
  await exportExcel(worksheet, "RT_Structure_Prediction_Template.xlsx");
};
