import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  files: [], // List of uploaded files
  selectedFileContent: null, // Content of the selected file for editing
};

const fileSlice = createSlice({
  name: "files",
  initialState,
  reducers: {
    addFiles(state, action) {
      state.files.push(action.payload);
    },
    removeFile(state, action) {
      state.files = state.files.filter((_, index) => index !== action.payload);
    },
    clearFiles(state) {
      state.files = [];
    },
    setSelectedFileContent(state, action) {
      state.selectedFileContent = action.payload;
    },
  },
});

export const { addFiles, removeFile, clearFiles, setSelectedFileContent } =
  fileSlice.actions;

export default fileSlice.reducer;
