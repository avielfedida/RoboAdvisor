import React, { useState } from "react";
import { Row, Col, Container, Form, Button } from "react-bootstrap";

const RegisterScreen = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  function validateForm() {
    return (
      email.length > 0 && password.length > 0 && password == passwordConfirm
    );
  }

  function handleSubmit(event) {
    event.preventDefault();
  }

  return (
    <Container className="offset_nav rtl text-right" id="login_screen">
      <Row>
        <Col xs={12}>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="email">
              <Form.Label>מייל</Form.Label>
              <Form.Control
                autoFocus
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="password">
              <Form.Label>סיסמה</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="password">
              <Form.Label>סיסמה שנית</Form.Label>
              <Form.Control
                type="password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
              />
            </Form.Group>
            <Button block size="lg" type="submit" disabled={!validateForm()}>
              הרשמה
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default RegisterScreen;
