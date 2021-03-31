import React, { useState } from "react";
import { Row, Col, Container, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Loader from "../reusables/Loader";
import Message from "../reusables/Message";
import { register } from "../../actions/userActions";
import { validateEmail } from "../reusables/utils";

const RegisterScreen = () => {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");

  const [message, setMessage] = useState("");

  const dispatch = useDispatch();

  const userRegister = useSelector((state) => state.userRegister);
  const { success, error, loading } = userRegister;

  const submitHandler = (e) => {
    e.preventDefault();
    if (email.length === 0) {
      setMessage("חשבון המייל לא יכול להיות ריק");
    } else if (!validateEmail(email)) {
      setMessage("פורמט מייל אינו תקין");
    } else if (name.length === 0) {
      setMessage("השם לא יכול להיות ריק");
    } else if (surname.length === 0) {
      setMessage("שם המשפחה לא יכול להיות ריק");
    } else if (password.length === 0) {
      setMessage("הסיסמה לא יכולה להיות ריקה");
    } else if (password !== passwordConfirm) {
      setMessage("הסיסמאות אינן תואמות");
    } else {
      setMessage("");
      dispatch(register(name, surname, email, password, dateOfBirth));
    }
  };

  return (
    <Container className="offset_nav rtl text-right" id="login_screen">
      <Row>
        <Col xs={12}>
          <h1>הרשמה</h1>
          {success && <Message variant="success" text={success} />}
          {message && <Message variant="danger" text={message} />}
          {error && <Message variant="danger" text={error} />}
          {loading && <Loader />}
          <Form onSubmit={submitHandler}>
            <Form.Group controlId="email">
              <Form.Label>
                מייל<span className="red">*</span>
              </Form.Label>
              <Form.Control
                autoFocus
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="name">
              <Form.Label>
                שם<span className="red">*</span>
              </Form.Label>
              <Form.Control
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="surname">
              <Form.Label>
                שם משפחה<span className="red">*</span>
              </Form.Label>
              <Form.Control
                type="text"
                value={surname}
                onChange={(e) => setSurname(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="password">
              <Form.Label>
                סיסמה<span className="red">*</span>
              </Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="password_confirm">
              <Form.Label>
                סיסמה שנית<span className="red">*</span>
              </Form.Label>
              <Form.Control
                type="password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="date_of_birth">
              <Form.Label>תאריך לידה</Form.Label>
              <Form.Control
                type="date"
                value={dateOfBirth}
                onChange={(e) => setDateOfBirth(e.target.value)}
              />
            </Form.Group>
            <Button block size="lg" type="submit">
              הרשמה
            </Button>
            <p className="mt-4">
              יש לך משתמש? <Link to="/login">התחבר/י</Link>
            </p>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default RegisterScreen;
