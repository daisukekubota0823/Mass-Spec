const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { Pool } = require("pg");
const path = require("path");
const fs = require("fs");
const ExcelJS = require("exceljs");

const app = express();
const PORT = process.env.PORT || 5000;

// Enable CORS
app.use(cors());

// Configure PostgreSQL connection
const pool = new Pool({
  user: "postgres",
  host: "localhost",
  database: "lamass",
  password: "morah",
  port: 5432,
});

// Function to check database connection
const checkDatabaseConnection = async () => {
  try {
    const res = await pool.query("SELECT NOW()"); // Simple query to check connection
    console.log("Database connected successfully:", res.rows[0]);
  } catch (error) {
    console.error("Database connection error:", error);
  }
};

// Ensure assets directory exists
const assetsDir = path.join(__dirname, "assets");
if (!fs.existsSync(assetsDir)) {
  fs.mkdirSync(assetsDir); // Create the assets directory if it doesn't exist
}

// Set up storage for uploaded files
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, assetsDir); // Specify the directory to save files
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname)); // Append timestamp to the filename
  },
});

const upload = multer({ storage });

// Endpoint to upload files
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    // Save metadata to PostgreSQL
    await pool.query("INSERT INTO files (filename) VALUES ($1)", [
      req.file.filename,
    ]);

    console.log(`File uploaded successfully: ${req.file.filename}`);
    return res.json({
      message: "File uploaded successfully!",
      filename: req.file.filename,
    });
  } catch (error) {
    console.error("Error uploading file:", error);
    return res.status(500).json({ error: "Failed to upload the file." });
  }
});

// Endpoint to get list of uploaded files
app.get("/files", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM files");
    console.log(`Fetched ${result.rowCount} files successfully.`);
    res.json(result.rows);
  } catch (error) {
    console.error("Error fetching files:", error);
    res.status(500).json({ error: "Failed to fetch files." });
  }
});

// Endpoint to delete a file
app.delete("/files/:id", async (req, res) => {
  const { id } = req.params;

  try {
    const result = await pool.query(
      "DELETE FROM files WHERE id = $1 RETURNING *",
      [id]
    );

    if (result.rowCount === 0) {
      console.warn(`File not found for deletion with ID: ${id}`);
      return res.status(404).json({ error: "File not found." });
    }

    // Optionally delete the physical file as well
    const filename = result.rows[0].filename;
    const filePath = path.join(assetsDir, filename);

    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath); // Delete the file from the server
      console.log(`Deleted physical file: ${filename}`);
    }

    console.log(`File deleted successfully with ID: ${id}`);
    res.json({ message: "File deleted successfully!" });
  } catch (error) {
    console.error("Error deleting file:", error);
    res.status(500).json({ error: "Failed to delete the file." });
  }
});

// Endpoint to get content of an Excel file for editing
app.get("/files/content/:filename", async (req, res) => {
  const { filename } = req.params;

  try {
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.readFile(path.join(assetsDir, filename));

    const worksheet = workbook.worksheets[0];
    const jsonData = [];

    worksheet.eachRow((row, rowNumber) => {
      if (rowNumber > 1) { // Skip header row
        const rowData = {};
        row.eachCell((cell, colNumber) => {
          rowData[worksheet.getCell(1, colNumber).value] = cell.value; // Use header as key
        });
        jsonData.push(rowData);
      }
    });

    console.log(`Content retrieved successfully for file: ${filename}`);
    res.json(jsonData);
  } catch (error) {
    console.error("Error reading file content:", error);
    res.status(500).json({ error: "Failed to read the file content." });
  }
});

// Call the function to check the database connection
checkDatabaseConnection();

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
