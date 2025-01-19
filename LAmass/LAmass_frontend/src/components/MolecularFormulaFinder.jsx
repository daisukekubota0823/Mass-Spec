import React from 'react';

export default function MolecularFormulaFinder() {
    return (
        <>      
          {/* Molecular Formula Finder Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex">
              <h3 className="text-lg font-medium text-purple-600 mb-4 mr-5">
                Molecular Formula Finder
              </h3>
              <button
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
                    <th className="border border-gray-300 px-4 py-2">
                      Formula
                    </th>
                    <th className="border border-gray-300 px-4 py-2">
                      Error (mDa)
                    </th>
                    <th className="border border-gray-300 px-4 py-2">
                      Error (ppm)
                    </th>
                    <th className="border border-gray-300 px-4 py-2">Score</th>
                    <th className="border border-gray-300 px-4 py-2">
                      Resource
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {/* Dummy data rows */}
                  {[
                    {
                      formula: "C6H12O6",
                      error_mDa: "0.5",
                      error_ppm: "1.0",
                      score: "9.5",
                      resource: "Database A",
                    },
                    {
                      formula: "C12H22O11",
                      error_mDa: "1.0",
                      error_ppm: "1.5",
                      score: "8.7",
                      resource: "Database B",
                    },
                    {
                      formula: "C5H10O5",
                      error_mDa: "0.7",
                      error_ppm: "1.3",
                      score: "8.9",
                      resource: "Database C",
                    },
                    {
                      formula: "C3H6O3",
                      error_mDa: "0.3",
                      error_ppm: "0.8",
                      score: "9.0",
                      resource: "Database D",
                    },
                    {
                      formula: "C6H12O6",
                      error_mDa: "0.5",
                      error_ppm: "1.0",
                      score: "9.5",
                      resource: "Database A",
                    },
                    {
                      formula: "C12H22O11",
                      error_mDa: "1.0",
                      error_ppm: "1.5",
                      score: "8.7",
                      resource: "Database B",
                    },
                    {
                      formula: "C5H10O5",
                      error_mDa: "0.7",
                      error_ppm: "1.3",
                      score: "8.9",
                      resource: "Database C",
                    },
                    {
                      formula: "C3H6O3",
                      error_mDa: "0.3",
                      error_ppm: "0.8",
                      score: "9.0",
                      resource: "Database D",
                    },
                  ].map((row, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-2 text-center">
                        <input type="checkbox" />
                      </td>
                      <td className="border border-gray-300 px-4 py-2">
                        {row.formula}
                      </td>
                      <td className="border border-gray-300 px-4 py-2">
                        {row.error_mDa}
                      </td>
                      <td className="border border-gray-300 px-4 py-2">
                        {row.error_ppm}
                      </td>
                      <td className="border border-gray-300 px-4 py-2">
                        {row.score}
                      </td>
                      <td className="border border-gray-300 px-4 py-2">
                        {row.resource}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>

    );
}
