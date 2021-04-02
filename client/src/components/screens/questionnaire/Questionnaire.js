import React, { useState } from "react";
import { useParams } from "react-router-dom";
import {
  Card,
  Button,
  ButtonGroup,
  Form,
  Row,
  Col,
  FormCheck,
} from "react-bootstrap";

const Questionnaire = ({
  data,
  max_q_n,
  update_question,
  answers_state,
  update_answer,
}) => {
  const { q_num } = useParams();
  const q_number = parseInt(q_num);
  const [disabledBtns, setDisabledBtns] = useState(false);
  return (
    <Card border="0">
      <Row>
        <Col xs={6}>
          {data.using_image_question ? (
            <Card.Img
              variant="top"
              src={"/images/" + data.image_url_question}
            />
          ) : null}
        </Col>
        <Col xs={6}>
          <Card.Body>
            <Row style={{ minHeight: "20vh" }}>
              <Col xs={12}>
                <Card.Text className="question_text">
                  <h1>שאלה מספר {q_number}</h1>
                </Card.Text>
                <Card.Text className="question_text">
                  <h4>{data.question}</h4>
                </Card.Text>
              </Col>
            </Row>
            <hr />
            <Form.Group as={Row} style={{ position: "relative" }}>
              <ButtonGroup
                style={{ position: "absolute", top: "-35px", right: 0 }}
              >
                <Button
                  disabled={disabledBtns}
                  variant="primary"
                  onClick={() => {
                    if (q_number === max_q_n) {
                      setDisabledBtns(true);
                    }
                    update_question(q_number + 1);
                  }}
                >
                  {q_number === max_q_n ? "הרכבת תיק" : "שאלה הבאה"}
                </Button>
                <Button
                  disabled={disabledBtns}
                  onClick={() => update_question(q_number - 1)}
                  // disabled={q_number === 1}
                  variant="secondary"
                >
                  {q_number === 1 ? "חזרה להסבר" : "שאלה קודמת"}
                </Button>
              </ButtonGroup>
              <Col xs={12}>
                <Form.Label as="legend" column>
                  <h3>תשובות אפשריות</h3>
                </Form.Label>
                {data.list_ans.map((ans, i) => {
                  return (
                    <Form.Check key={i}>
                      <Form.Check.Label
                        className="rtl"
                        onClick={() => update_answer(q_number - 1, i)}
                      >
                        <Form.Check.Input
                          checked={answers_state[q_number - 1] === i}
                          name={data.question}
                          type={"radio"}
                        />
                        <span className="mr-5">{ans}</span>
                      </Form.Check.Label>
                    </Form.Check>
                  );
                })}
              </Col>
            </Form.Group>
          </Card.Body>
        </Col>
      </Row>
    </Card>
  );
};

export default Questionnaire;
