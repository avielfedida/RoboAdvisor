import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";

const QExplanation = ({ update_question }) => {
  return (
    <Container className="offset_nav rtl">
      <Row>
        <Col xs={12}>
          <h1>אופן מענה</h1>
          <p>
            השאלון הבא מורכב מאוסף שאלות אשר מטרתן היא לזהות מהוא פרופיל הסיכון
            המתאים לך. לאחר מכן יופעלו אחד מהאלגוריתמים בהתאם לאחד שתבחר/י
            ויתקבל תיק השקעות מומלץ ע"פ האלגוריתם
          </p>
          <p>
            <Button id={"qt_explanation_start_btn"} variant="primary" onClick={() => update_question(1)}>
              התחלה!
            </Button>
          </p>
        </Col>
      </Row>
    </Container>
  );
};

export default QExplanation;
