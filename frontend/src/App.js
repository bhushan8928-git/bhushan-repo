import React, { useEffect, useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import Home from "./pages/Home";
import CountryDetail from "./pages/CountryDetail";
import PlaceDetail from "./pages/PlaceDetail";
import { Toaster } from "sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export const axiosInstance = axios.create({
  baseURL: API,
});

function App() {
  useEffect(() => {
    const seedData = async () => {
      try {
        await axiosInstance.post('/seed');
      } catch (e) {
        console.error('Seed error:', e);
      }
    };
    seedData();
  }, []);

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/country/:countryId" element={<CountryDetail />} />
          <Route path="/place/:placeId" element={<PlaceDetail />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" richColors />
    </div>
  );
}

export default App;