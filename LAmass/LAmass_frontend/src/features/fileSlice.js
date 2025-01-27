import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios'; // Assuming you're using axios for API calls

const API_BASE_URL = 'http://localhost:5000/api/v1'; // Replace with your actual API base URL

export const sendFile = createAsyncThunk(
  'data/sendFileContent',
  async (data, thunkAPI) => {
    try {
      console.log("DATA FINAL" + JSON.stringify(data))
      const response = await axios.post(`${API_BASE_URL}/mass_spectra`, data);
      thunkAPI.dispatch(getAllFiles());
      console.log(thunkAPI.dispatch(getAllFiles()))
      return response.data;
    } catch (error) {
      console.error("Error in sendFileContent:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

export const getAllFiles = createAsyncThunk(
  'data/getAllFiles',
  async (_, thunkAPI) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/mass_spectra`);
      console.log("ress" + JSON.stringify(response.data[0].name))
      return response.data;
    } catch (error) {
      console.error("Error in getAllFiles:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

export const getOneFile = createAsyncThunk(
  'data/getOneFile',
  async (id, thunkAPI) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/mass_spectra/${id}`);
      return response.data;
    } catch (error) {
      console.error("Error in getOneFile:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

export const updateFile = createAsyncThunk(
  'data/updateFileContent',
  async (data, thunkAPI) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/mass_spectra/${data.id}`, data);
      return response.data;
    } catch (error) {
      console.error("Error in updateFileContent:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

export const deleteFile = createAsyncThunk(
  'data/deleteFileContent',
  async (id, thunkAPI) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/mass_spectra/${id}`);
      return response.data;
    } catch (error) {
      console.error("Error in deleteFileContent:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

export const deleteAllFile = createAsyncThunk(
  'data/deleteAllFileContent',
  async (_, thunkAPI) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/mass_spectra`);
      return response.data;
    } catch (error) {
      console.error("Error in deleteAllFileContent:", error);
      return thunkAPI.rejectWithValue(error.response.data);
    }
  }
);

const fileSlice = createSlice({
  name: 'file',
  initialState: {
    loading: false,
    error: null,
    response: null,
    allFiles: [],
    currentFile: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(sendFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendFile.fulfilled, (state, action) => {
        state.loading = false;
        state.response = action.payload;
        state.error = null;
      })
      .addCase(sendFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.response = null;
      })
      .addCase(updateFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateFile.fulfilled, (state, action) => {
        state.loading = false;
        state.allFiles = state.allFiles.map(file =>
          file.id === action.payload.id ? action.payload : file
        );
        state.error = null;
      })
      .addCase(updateFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.response = null;
      })
      .addCase(deleteFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteFile.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.allFiles = state.allFiles.filter(file => file.id !== action.payload.id);
      })
      .addCase(deleteFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.response = null;
      })
      .addCase(deleteAllFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteAllFile.fulfilled, (state, action) => {
        state.loading = false;
        state.allFiles = [];
        state.error = null;
      })
      .addCase(deleteAllFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.response = null;
      })
      .addCase(getAllFiles.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getAllFiles.fulfilled, (state, action) => {
        state.loading = false;
        state.allFiles = action.payload;
        state.error = null;
      })
      .addCase(getAllFiles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.allFiles = [];
      })
      .addCase(getOneFile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getOneFile.fulfilled, (state, action) => {
        state.loading = false;
        state.currentFile = action.payload;
        state.error = null;
      })
      .addCase(getOneFile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.currentFile = null;
      });
  },
});

export default fileSlice.reducer;
