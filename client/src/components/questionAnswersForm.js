import React  from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Modal from '@material-ui/core/Modal';
import LinearProgress from '@material-ui/core/LinearProgress';

import QuestionAnswers from './questionAnswers';
import formSubmit from '../api/formSubmit';
import Questions_Answers from './questions_answers';
import Image from './AnalysisImage';
import AnalysisImage from "./AnalysisImage";


const useStyles = makeStyles((theme) => ({
    layout: {
        width: 'auto',
        [theme.breakpoints.up(5 + theme.spacing(2) )]: {
            width: 1000,
            marginLeft: 'auto',
            marginRight: 'auto',
        },

    },
    paper: {
        [theme.breakpoints.up(5 + theme.spacing(2) )]: {
            padding: theme.spacing(1),
        },

    },
    modal: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    modal_body:{
        height : 150,
        width: 400,
        backgroundColor: '#000',
        direction: "rtl",
        color :'white',
        padding: theme.spacing(2),
        textAlign :'center',
    },
    title:{
        direction: "rtl",
        fontSize: 35,
        fontFamily: 'Suez One',
        padding: theme.spacing(1),
        textAlign :'center',

    },
    body:{

        direction: "rtl",
        fontSize: 25,
        fontFamily: 'Suez One',
        padding: theme.spacing(1),
        textAlign :'center',
    },
    end:{

        direction: "rtl",
        fontSize: 30,
        fontFamily: 'Suez One',
        padding: theme.spacing(1),
        textAlign :'center',
    },
    buttons:{
      display: "flex",
        '& > *': {
            height: 40,
            width: 80,
            fontSize: 20,
            fontFamily: 'Suez One',
            variant:"contained",
            shadowColor: "#000",
            shadowOffset: {
                width: 0,
                height: 12,
            },
            shadowOpacity: 0.58,
            shadowRadius: 16.00,
            elevation: 24,
            backgroundColor: '#000',
            color :'white',
            marginTop: theme.spacing(3),
            '&:hover': {
                backgroundColor: 'white',
                color :'#000',
                borderColor: '#000',
                border: '2px solid'
            },
         },
    },
    button_next: {
        height: 40,
        fontSize: 20,
        fontFamily: 'Suez One',
        variant:"contained",
        backgroundColor: '#000',
        color :'white',
        marginTop: theme.spacing(3),
        '&:hover': {
            backgroundColor: 'white',
            color :'#000',
            borderColor: '#000',
            border: '2px solid'
        },
        marginRight: 'auto'
    },
    button_back: {
        marginLeft: 'auto',
    },
    linear_progress:{
        width: '100%',
        '& > * + *': {
            marginTop: theme.spacing(2),
        },

        background: '#2196f3',
        display: 'flex',
        justifyContent: 'center',
    },
    question_answers:{
    },
}));
const steps= Questions_Answers


const MainForm = () => {
    const classes = useStyles();
    const [activeStep, setActiveStep] = React.useState(0);
    const [answers, setAnswers ]= React.useState({});
    const [allAns, setAllAns] = React.useState(false);
    const [load, setLoad] = React.useState(false);
    const [showModal, setShowModal] = React.useState(false);
    const [explanationQuestion, setExplanationQuestion] = React.useState(true);
    const getChooseAns = (step,index) => {
        setAnswers({...answers, [step]: parseInt(index)});
    };
    const [getPortfolio, setGetPortfolio] = React.useState(null);

    const load_form_submit = async () => {
        try {
            setLoad(true);
            const res = await formSubmit.post( "/", answers );
            setGetPortfolio(res.data.src);
            setLoad(false);
        } catch (e) {
            console.log(e);
        }
    };

    const handleEnd = () =>{
        if(Object.keys(answers).length ===  steps.length ) {
            // setAllAns(true);
            // console.log(answers)
            load_form_submit()
        }
        else {
            setShowModal(true);
        }
    }
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
                ): null}
                {load ? (<LinearProgress className={classes.linear_progress}/>) : null}
                {activeStep !== steps.length && !load && !explanationQuestion && getPortfolio ==null &&
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
                                <Button onClick={handleNext} className={classes.button_next}>הבא</Button>
                            )}

                            {activeStep === steps.length -1 && (
                                <Button onClick={handleEnd} className={classes.button_next}>סיום</Button>
                            )}

                            {activeStep !== 0 && (
                                <Button onClick={handleBack} className={classes.button_back}>חזור</Button>
                            )}
                        </div>
                    </div>
                }
                {explanationQuestion && !load ? (
                    <div >
                        <p className={classes.title}>8 שאלות קצרות ויש לך תיק השקעות מותאם אישית</p>

                        <p className={classes.body}>
                            כדי לתכנן את תיק ההשקעות המתאים ביותר עבורך נשאל כמה שאלות לגבי ההעדפות שלך
                        </p>
                        <p className={classes.body}>
                            תענה לפי מה שמשקף בצורה הטובה ביותר אותך
                        </p>

                        <p className={classes.end}>בהצלחה!</p>

                        <Button onClick={handleStart} className={classes.button_next}>קדימה בואו נתחיל</Button>
                    </div>
                ):null}
                {getPortfolio !== null ? (<AnalysisImage src={getPortfolio}/>): null}
            </Paper>
        </main>
    );
}

export default MainForm;
