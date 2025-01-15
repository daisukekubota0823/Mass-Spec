import React, { useState } from "react";
import axios from "axios";

function ComputeMean() {
  const [values, setValues] = useState("");
  const [mean, setMean] = useState(null);
  const [error, setError] = useState("");

  // Handle input change
  const handleChange = (event) => {
    setValues(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    // Convert input string into an array of numbers
    const numArray = values
      .split(",") // Split by commas
      .map((num) => parseFloat(num.trim())); // Trim and convert each value to a float

    // Validate that input is an array of numbers
    if (numArray.some(isNaN)) {
      setError("All values must be numeric.");
      return;
    }

    try {
      // Make POST request to compute the mean
      const response = await axios.post("http://127.0.0.1:8000/compute-mean", {
        values: numArray,
      });
      setMean(response.data.mean);
      setError(""); // Clear any previous errors
    } catch (err) {
      setError("Error computing mean: " + err.response.data.detail);
    }
  };

  return (
    <div>
      <h1>Compute Mean</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Enter numbers (comma-separated):
          <input
            type="text"
            value={values}
            onChange={handleChange}
            placeholder="e.g. 1, 2, 3, 4, 5"
          />
        </label>
        <button type="submit">Compute Mean</button>
      </form>

      {mean !== null && (
        <div>
          <h2>Mean: {mean}</h2>
        </div>
      )}

      {error && <div style={{ color: "red" }}>{error}</div>}
    </div>
  );
}

export default ComputeMean;
