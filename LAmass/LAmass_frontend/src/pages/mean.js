import React, { useState } from "react";
import axios from "axios";

function ComputeMean() {
  const [values, setValues] = useState("");
  const [mean, setMean] = useState(null);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    setValues(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const numArray = values.split(",").map((num) => parseFloat(num.trim()));

    if (numArray.some(isNaN)) {
      setError("All values must be numeric.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/compute-mean", {
        values: numArray,
      });
      setMean(response.data.mean);
      setError("");
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
