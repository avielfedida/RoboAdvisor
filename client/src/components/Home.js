import React from "react";
import { Container, Row, Col, Image, Button } from "react-bootstrap";
import Logo from "./reusables/Logo";
import { useNavigate } from "react-router-dom";
import LatestResults from "./reusables/LatestResults";

const Home = () => {
  const navigate = useNavigate();
  return (
    <Container fluid>
      <Row>
        <Col sm={12} id="top_banner">
          <Row>
            <Col sm={12}>
              <Logo />
              <p>
                מטרת האתר היא לאפשר לכל מי שמעוניין להיכנס לעולם ההשקעות ואו
                להשתמש ב RoboAdvisors לשם השקעה לעשות זאת באופן קל ונוח
              </p>
              <p>
                באתר זה תוכלו למצוא פורום משתמשים בו תוכלו לחלוק רעיונות ותוצאות
                של ה RoboAdvisor ולעזור אחד לשני
              </p>
              <p>
                <Button
                  variant="primary"
                  onClick={() => navigate("questionnaire/explanation")}
                >
                  בניית תיק השקעות
                </Button>
              </p>
            </Col>
          </Row>
        </Col>
      </Row>
      <Row>
        <Col sm={12}>
          <LatestResults />
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
