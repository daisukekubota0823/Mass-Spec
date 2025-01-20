export default function MRMprobs() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-800">MRMprobs</h2>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              MRM Parameters
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Precursor m/z
                </label>
                <input
                  type="number"
                  placeholder="Enter m/z value"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Collision Energy
                </label>
                <input
                  type="number"
                  placeholder="Enter CE value"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary"
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Optimization
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Method
                </label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                  <option>Automatic</option>
                  <option>Manual</option>
                  <option>Semi-automatic</option>
                </select>
              </div>

              <button className="w-full px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90">
                Start Optimization
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
