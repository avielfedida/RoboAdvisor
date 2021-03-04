import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import Copyrights from "./reusable/Copyrights";

const Footer = () => {
  return (
    <footer className="navbar fixed-bottom bg-light">
      <Container className="justify-content-end">
        <Row>
          <Col className="text-center py-3">
            <Copyrights />
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
