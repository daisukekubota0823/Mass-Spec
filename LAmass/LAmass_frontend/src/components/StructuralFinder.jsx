import React from "react";

export default function StructuralFinder() {
  return (
    <>
      <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
        <div className="flex">
          <h3 className="text-lg font-medium text-purple-600 mb-4">
            Structural Finder
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
                <th className="border border-gray-300 px-4 py-2">Name</th>
                <th className="border border-gray-300 px-4 py-2">
                  Score (max=10)
                </th>
                <th className="border border-gray-300 px-4 py-2">Ontology</th>
                <th className="border border-gray-300 px-4 py-2">InChIKey</th>
              </tr>
            </thead>
            <tbody>
              {/* Dummy data rows */}
              {[
                {
                  name: "Glucose",
                  score: "9.5",
                  ontology: "Carbohydrate",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Fructose",
                  score: "8.7",
                  ontology: "Carbohydrate",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Sucrose",
                  score: "8.9",
                  ontology: "Disaccharide",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Lactose",
                  score: "8.0",
                  ontology: "Disaccharide",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Glucose",
                  score: "9.5",
                  ontology: "Carbohydrate",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Fructose",
                  score: "8.7",
                  ontology: "Carbohydrate",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Sucrose",
                  score: "8.9",
                  ontology: "Disaccharide",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
                {
                  name: "Lactose",
                  score: "8.0",
                  ontology: "Disaccharide",
                  inchiKey: "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                },
              ].map((row, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="border border-gray-300 px-4 py-2">
                    {row.name}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {row.score}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {row.ontology}
                  </td>
                  <td className="border border-gray-300 px-4 py-2">
                    {row.inchiKey}
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
