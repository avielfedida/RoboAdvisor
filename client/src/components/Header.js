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
import { Link, useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

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
            <Nav.Link
              onClick={() => navigate("login")}
              className="nav_link_custom"
              id="nav_link_login"
            >
              <span class="lnr lnr-enter"></span>

              <span>התחברות</span>
            </Nav.Link>
            <Nav.Link
              onClick={() => navigate("register")}
              className="nav_link_custom"
              id="nav_link_register"
            >
              <span class="lnr lnr-user"></span>
              <span>הרשמה</span>
            </Nav.Link>
          </>
        </Navbar.Collapse>
      </Navbar>
    </header>
  );
};

export default Header;
