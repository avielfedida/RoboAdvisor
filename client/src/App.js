import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./components/Home";
import QWrapper from "./components/screens/questionnaire/QWrapper";
import LoginScreen from "./components/screens/LoginScreen";
import ForumScreen from "./components/screens/forum/ForumScreen";
import RegisterScreen from "./components/screens/RegisterScreen";
import ProfileScreen from "./components/screens/ProfileScreen";
import ChangePasswordScreen from "./components/screens/ChangePasswordScreen";
import PortfolioScreen from "./components/screens/PortfolioScreen";
import ForgotPasswordScreen from "./components/screens/ForgotPasswordScreen";
import ResetPasswordScreen from "./components/screens/ResetPasswordScreen";

function App() {
  return (
    <Router>
      <Header />
      <main>
        <Routes>
          <Route path="login" element={<LoginScreen />} />
          <Route path="register" element={<RegisterScreen />} />
          <Route path="profile" element={<ProfileScreen />} />
          <Route path="change_password" element={<ChangePasswordScreen />} />
          <Route path="forgot_password" element={<ForgotPasswordScreen />} />
          <Route
            path="reset_password/:reset_code"
            element={<ResetPasswordScreen />}
          />
          <Route path="forum/*" element={<ForumScreen />} />
          <Route path="questionnaire/*" element={<QWrapper />} />
          <Route path="portfolio/:link" element={<PortfolioScreen />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
