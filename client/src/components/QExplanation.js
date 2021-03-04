import React from "react";
import { Jumbotron, Button, Card } from "react-bootstrap";

const QExplanation = ({ update_question }) => {
  return (
    <Card>
      <Jumbotron className="jumb">
        <h1>אופן מענה</h1>
        <p>
          השאלון הבא מורכב משאלות שמטרתן לזהות את התיק המותאם ביותר עבורך, ועוד
          הסברים פה...
        </p>
        <p>
          <Button variant="primary" onClick={() => update_question(1)}>
            התחל!
          </Button>
        </p>
      </Jumbotron>
    </Card>
  );
};

export default QExplanation;
