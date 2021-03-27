import React, { useState, useEffect } from "react";
import { Row, Col, Container, Form, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Loader from "../reusables/Loader";
import Message from "../reusables/Message";
import { login } from "../../actions/userActions";
import { validateEmail } from "../reusables/utils";
const LoginScreen = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo, error, loading } = userLogin;

  useEffect(() => {
    if (userInfo) {
      navigate("/");
    }
  }, [navigate, userInfo]);

  const submitHandler = (e) => {
    e.preventDefault();
    if (email.length === 0) {
      setMessage("חשבון המייל לא יכול להיות ריק");
    } else if (!validateEmail(email)) {
      setMessage("פורמט מייל אינו תקין");
    } else if (password.length === 0) {
      setMessage("הסיסמה לא יכולה להיות ריקה");
    } else {
      setMessage("");
      dispatch(login(email, password));
    }
  };

  return (
    <Container className="offset_nav rtl text-right" id="login_screen">
      <Row>
        <Col xs={12}>
          <h1>התחברות</h1>
          {message && <Message variant="danger" text={message} />}
          {error && <Message variant="danger" text={error} />}
          {loading && <Loader />}
          <Form onSubmit={submitHandler}>
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
            <Button block size="lg" type="submit">
              התחברות
            </Button>
            <p className="mt-4">
              אין לך משתמש? <Link to="/register">הרשם/י</Link>
            </p>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginScreen;
