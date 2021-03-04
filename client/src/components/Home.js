import React from "react";
import { Container, Row, Col, Jumbotron, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
const Home = () => {
  const navigate = useNavigate();
  return (
    <Container fluid>
      <Row>
        <Col sm={12} className="p-0">
          <Jumbotron className="jumb">
            <h1>ברוכים הבאים ל RoboAdvisor</h1>
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
          </Jumbotron>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
