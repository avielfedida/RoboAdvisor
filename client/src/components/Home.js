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
                  id={"start_questionnaire"}
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
      <Row>
        <Col sm={12} id="disclaimer" className="rtl text-right" p={4}>
          <h4>הבהרה:</h4>
          <p>
            הפלטפורמה המוצגת לפניך היא פרי פיתוח של קבוצת סטודנטים במסגרת
            לימודים אקדמאים באוניברסיטת בן גוריון, והיא אינה מחוברת לעולם המסחר
            ואינה מהווה המלצה באופן אישי לגורם ספציפי. מטרת הפלטפורמה היא מימוש
            מודלים פיננסיים שקיבלו הכרה אקדמאית וקידום הפלטפורמה האקדמאית, על
            מנת תוכל לתת הזדמנויות לחוקרים, אנשי אקדמיה וסטודנטים, להתנסות
            במודלים הפיננסים שקיבלו הכרה אקדמאית בינלאומית ולא ממומשו עדיין
            בעולם הפיננסי.
          </p>
          <p>
            <strong>
              הפלטפורמה הינה למטרת מחקר אקדמאי בלבד. אין לראות במערכת כהמלצה או
              יעוץ.
            </strong>
          </p>
        </Col>
      </Row>
    </Container>
  );
};

export default Home;
