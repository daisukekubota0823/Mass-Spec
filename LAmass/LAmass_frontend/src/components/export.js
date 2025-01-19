import React from 'react';
import * as XLSX from 'xlsx';

const Export = () => {
    const exportTemplate = () => {
        const headers = [
            "SMILE",
            "Spectrum Type",
            "Ion Mode",
            "Precursor Type",
            "InChIKey",
            "Ontology",
            "Collision Energy",
            "Precursor m/z",
            "Retention Time (min)",
            "Name",
            "Instrument",
            "Instrument Type",
            "Comment",
            "Sulfur Count",
            "Nitrogen Count",
            "Carbon Count"
        ];

        // Create an empty array for the data
        const templateData = [headers];

        // Convert the data to a worksheet
        const worksheet = XLSX.utils.aoa_to_sheet(templateData);

        // Apply styles to the header row
        const headerCellStyle = {
            fill: {
                fgColor: { rgb: "FFCCFF" } // Light purple background color
            },
            font: {
                bold: true,
                color: { rgb: "FFFFFF" } // White text color
            }
        };

        // Apply style to each header cell
        for (let i = 0; i < headers.length; i++) {
            const cellAddress = XLSX.utils.encode_cell({ r: 0, c: i }); // Row 0 (header)
            if (!worksheet[cellAddress]) worksheet[cellAddress] = {}; // Ensure cell exists
            worksheet[cellAddress].s = headerCellStyle; // Apply style
        }

        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Template');

        // Generate the Excel file
        XLSX.writeFile(workbook, 'Mass_Spectrometry_Template.xlsx');
    };

    return (
        <div>
            <h1 style={{ color: 'purple' }}>Excel Import/Export</h1>
            <button onClick={exportTemplate}>Export Template</button>
        </div>
    );
};

export default Export;
