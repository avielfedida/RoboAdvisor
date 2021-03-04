import React, { useEffect } from "react";

import QuestionAnswers from "./questionAnswers";
import formSubmit from "../api/formSubmit";
import Questions_Answers from "./questions_answers";
import Image from "./AnalysisImage";
import AnalysisImage from "./AnalysisImage";
import Portfolio from "./Portfolio";

const steps = Questions_Answers;

const MainForm = () => {
  const [activeStep, setActiveStep] = React.useState(0); // 7
  const [answers, setAnswers] = React.useState({});

  const [allAns, setAllAns] = React.useState(false); // true
  const [load, setLoad] = React.useState(false);
  const [showModal, setShowModal] = React.useState(false);
  const [explanationQuestion, setExplanationQuestion] = React.useState(true); // false
  const getChooseAns = (step, index) => {
    setAnswers({ ...answers, [step]: parseInt(index) });
  };
  const [getPortfolio, setGetPortfolio] = React.useState(null);

  const load_form_submit = async () => {
    try {
      setLoad(true);
      const res = await formSubmit.post("/", answers);
      setGetPortfolio(res.data.src);
      setLoad(false);
    } catch (e) {
      console.log(e);
    }
  };

  // useEffect(() => {
  //     load_form_submit()
  // }, [])

  const handleEnd = () => {
    if (Object.keys(answers).length === steps.length) {
      // setAllAns(true);
      // console.log(answers)
      load_form_submit();
    } else {
      setShowModal(true);
    }
  };
  const handleNext = () => {
    setActiveStep(activeStep + 1);
  };
  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };
  const handleClose = () => {
    setShowModal(false);
    setActiveStep(0);
  };
  const handleStart = () => {
    setExplanationQuestion(false);
  };
  return (
    <main className={classes.layout}>
      <Paper className={classes.paper}>
        {showModal ? (
          <Modal
            className={classes.modal}
            open={showModal}
            onClose={handleClose}
          >
            <div className={classes.modal_body}>
              <h2>כדי שנוכל להתאים לך את התיק המתאים</h2>
              <h2>יש לענות על כל השאלות</h2>
            </div>
          </Modal>
        ) : null}
        {load ? <LinearProgress className={classes.linear_progress} /> : null}
        {activeStep !== steps.length &&
          !load &&
          !explanationQuestion &&
          getPortfolio == null && (
            <div>
              <QuestionAnswers
                answers={answers}
                step={activeStep}
                question={steps[activeStep].question}
                using_image_question={steps[activeStep].using_image_question}
                image_url_question={steps[activeStep].image_url_question}
                example={steps[activeStep].example}
                list_ans={steps[activeStep].list_ans}
                using_image_ans={steps[activeStep].using_image_ans}
                getchooseans={getChooseAns}
                className={classes.question_answers}
              />

              <div className={classes.buttons}>
                {activeStep !== steps.length - 1 && (
                  <Button onClick={handleNext} className={classes.button_next}>
                    הבא
                  </Button>
                )}

                {activeStep === steps.length - 1 && (
                  <Button onClick={handleEnd} className={classes.button_next}>
                    סיום
                  </Button>
                )}

                {activeStep !== 0 && (
                  <Button onClick={handleBack} className={classes.button_back}>
                    חזור
                  </Button>
                )}
              </div>
            </div>
          )}
        {explanationQuestion && !load ? (
          <div>
            <p className={classes.title}>
              8 שאלות קצרות ויש לך תיק השקעות מותאם אישית
            </p>

            <p className={classes.body}>
              כדי לתכנן את תיק ההשקעות המתאים ביותר עבורך נשאל כמה שאלות לגבי
              ההעדפות שלך
            </p>
            <p className={classes.body}>
              תענה לפי מה שמשקף בצורה הטובה ביותר אותך
            </p>

            <p className={classes.end}>בהצלחה!</p>

            <Button onClick={handleStart} className={classes.button_next}>
              קדימה בואו נתחיל
            </Button>
          </div>
        ) : null}
        {getPortfolio !== null ? (
          <Portfolio src={getPortfolio} />
        ) : // <AnalysisImage src={getPortfolio}/>
        null}
      </Paper>
    </main>
  );
};

export default MainForm;
