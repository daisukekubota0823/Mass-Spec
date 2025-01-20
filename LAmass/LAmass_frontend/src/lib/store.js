import { configureStore } from "@reduxjs/toolkit";
import fileReducer from "../features/fileSlice";

const store = configureStore({
  reducer: {
    files: fileReducer,
  },
});

export default store;
