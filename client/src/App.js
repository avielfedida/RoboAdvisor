import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./components/Home";
import QWrapper from "./components/QWrapper";
function App() {
  return (
    <div>
      <Header />
      <main>
        <BrowserRouter>
          <Routes>
            <Route path="questionnaire/*" element={<QWrapper />} />
            <Route path="/" element={<Home />} />
          </Routes>
        </BrowserRouter>
      </main>
      <Footer />
    </div>
  );
}

export default App;
