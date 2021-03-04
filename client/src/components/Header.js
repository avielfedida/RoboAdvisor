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

const Header = () => {
  return (
    <header>
      {/* <Container id="stripe_over_navbar">
        <Row>
          <Col>בקרו אותנו בפייסבוק</Col>
        </Row>
      </Container> */}
      <Navbar id="main-navbar" bg="light" expand="xl">
        <Navbar.Brand href="/">
          <h1>RoboAdvisor</h1>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic_navbar_nav" />
        <Navbar.Collapse className="justify-content-end" id="basic-navbar-nav">
          <Form inline>
            <InputGroup>
              <InputGroup.Prepend>
                <Button>
                  <i className="fa fa-search"></i>
                </Button>
              </InputGroup.Prepend>
              <FormControl
                id="search_box"
                type="text"
                placeholder="חפש מאמר"
                className="p-4"
              />
            </InputGroup>
          </Form>

          <Nav className="ml-5">
            <Nav.Link href="/forum" className="nav_link_custom">
              <i className="fas fa-comment-dollar fa-2x"></i>
              <p>פורום</p>
            </Nav.Link>
            <Nav.Link href="/login" className="nav_link_custom">
              <i className="fas fa-user fa-2x"></i>
              <p>התחברות</p>
            </Nav.Link>
            <Nav.Link href="/" className="nav_link_custom">
              <i className="fas fa-home fa-2x"></i>
              <p>עמוד הבית</p>
            </Nav.Link>
            {/* <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                        <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                        <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                    </NavDropdown> */}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </header>
  );
};

export default Header;
