import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./components/Home";
import QWrapper from "./components/screens/questionnaire/QWrapper";
import LoginScreen from "./components/screens/LoginScreen";
import ForumScreen from "./components/screens/forum/ForumScreen";
import RegisterScreen from "./components/screens/RegisterScreen";

function App() {
  return (
    <Router>
      <Header />
      <main>
        <Routes>
          <Route path="login" element={<LoginScreen />} />
          <Route path="register" element={<RegisterScreen />} />
          <Route path="forum/*" element={<ForumScreen />} />
          <Route path="questionnaire/*" element={<QWrapper />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
