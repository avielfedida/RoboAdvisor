import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";

const QExplanation = ({ update_question }) => {
  return (
    <Container className="offset_nav rtl">
      <Row>
        <Col xs={12}>
          <h1>אופן מענה</h1>
          <p>
            השאלון הבא מורכב משאלות שמטרתן לזהות את התיק המותאם ביותר עבורך,
            ועוד הסברים פה...
          </p>
          <p>
            <Button variant="primary" onClick={() => update_question(1)}>
              התחל!
            </Button>
          </p>
        </Col>
      </Row>
    </Container>
  );
};

export default QExplanation;
