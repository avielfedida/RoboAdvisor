import React from "react";
import {
  Navbar,
  Nav,
  NavDropdown,
  Form,
  FormControl,
  Button,
  InputGroup,
  Container,
  Row,
  Col,
} from "react-bootstrap";

import Logo from "./reusables/Logo";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../actions/userActions";
import { Link, useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const logoutHandler = () => {
    dispatch(logout());
  };

  return (
    <header>
      <Navbar id="main_navbar" className="fixed-top">
        <Link to="/">
          <Navbar.Brand>
            <Logo />
          </Navbar.Brand>
        </Link>
        <Navbar.Toggle aria-controls="basic_navbar_nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <>
            {userInfo ? (
              <>
                <span>ברוך שובך </span>
                <NavDropdown
                  title={userInfo.first_name + " " + userInfo.last_name}
                  id="username"
                >
                  <NavDropdown.Item id={"user_profile_nav"} onClick={() => navigate("profile")}>
                    פרופיל משתמש
                  </NavDropdown.Item>
                  <NavDropdown.Item id={"user_latest_results_nav"}
                    onClick={() => navigate("user_latest_results")}
                  >
                    הרצות אחרונות שלי
                  </NavDropdown.Item>
                  <NavDropdown.Item id={"user_logout"} onClick={logoutHandler}>
                    התנתק/י
                  </NavDropdown.Item>
                </NavDropdown>
              </>
            ) : (
              <>
                <Nav.Link
                  onClick={() => navigate("login")}
                  className="nav_link_custom"
                  id="nav_link_login"
                >
                  <span className="lnr lnr-enter"></span>

                  <span>התחברות</span>
                </Nav.Link>
                <Nav.Link
                  onClick={() => navigate("register")}
                  className="nav_link_custom"
                  id="nav_link_register"
                >
                  <span className="lnr lnr-user"></span>
                  <span>הרשמה</span>
                </Nav.Link>
              </>
            )}
            <Nav.Link
              onClick={() => navigate("forum")}
              className="nav_link_custom"
              id="nav_link_forum"
            >
              <span className="lnr lnr-bubble"></span>
              <span>פורום</span>
            </Nav.Link>
            <Nav.Link
              onClick={() => navigate("info_center")}
              className="nav_link_custom"
              id="nav_link_info_center"
            >
              <span className="lnr lnr-book"></span>
              <span>מרכז ידע</span>
            </Nav.Link>
            <Nav.Link
              onClick={() => navigate("/")}
              className="nav_link_custom"
              id="nav_link_forum"
            >
              <span className="lnr lnr-home"></span>
              <span>בית</span>
            </Nav.Link>
          </>
        </Navbar.Collapse>
      </Navbar>
    </header>
  );
};

export default Header;
