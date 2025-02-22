export default function MSDial() {
  const handleFileChange = (event) => {
    const files = event.target.files;
    // Handle the selected files as needed
    console.log(files);
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold text-gray-800">MS-DIAL</h2>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Project Settings
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Data Type
                </label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                  <option>LC/MS</option>
                  <option>GC/MS</option>
                  <option>CE/MS</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Ion Mode
                </label>
                <select className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary">
                  <option>Positive</option>
                  <option>Negative</option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-gray-800 mb-4">
              Data Files
            </h3>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <p className="text-gray-600">
                Drag and drop your data files here
              </p>
              <p className="text-sm text-gray-500 mt-1">or</p>
              <div className="mt-2">
                <input 
                  type="file" 
                  multiple 
                  onChange={handleFileChange} 
                  className="hidden" 
                  id="file-upload" 
                />
                <label htmlFor="file-upload" className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary/90 cursor-pointer">
                  Browse Files
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
