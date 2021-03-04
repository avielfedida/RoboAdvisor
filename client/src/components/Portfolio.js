import React from "react";
import { useNavigate } from "react-router-dom";
import { Card, Row, Col, Button } from "react-bootstrap";
const Portfolio = ({ data, back }) => {
  const navigate = useNavigate();
  if (data == null) {
    return <span>Invalid routing</span>;
  }
  return (
    <Card>
      <Row>
        <Col xs={6}>
          <Card.Img variant="top" className="portfolio_image" src={data.src} />
        </Col>
        <Col xs={6}>
          <Card.Body>
            <Row>
              <Col xs={12}>
                <Card.Text className="question_text">
                  <h1>התיק המומלץ</h1>
                </Card.Text>
                <Card.Text className="question_text">
                  ראשית צריך לחלק את הכסף ע"פ התרשים האמצעי אשר מגדיר את אחוז
                  הכסף שרצוי להשקיע בכל נייר ערך
                </Card.Text>
                <Card.Text className="question_text">
                  לאחר מכן צריך לחלק את הכסף בין המניות/איגרות החוב השונות ע"פ
                  החלק מסכום ההשקעה שהוקצה לכל אחד
                </Card.Text>
                <Button variant="primary" onClick={back}>
                  שינוי תשובה
                </Button>
              </Col>
            </Row>
          </Card.Body>
        </Col>
      </Row>
    </Card>
  );
};

export default Portfolio;
