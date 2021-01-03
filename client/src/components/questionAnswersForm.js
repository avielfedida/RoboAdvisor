import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import QuestionAnswers from './questionAnswers';
import Questions_Answers from './questions_answers';


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
        backgroundColor: '#9fa8da',
    },
    buttons:{
      display: "flex",
        '& > *': {
          height: 40 ,
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
         },
    },
    button_next: {
        backgroundColor: '#42a5f5',
        '&:hover': {
          backgroundColor: '#2196f3',
        },
        marginTop: theme.spacing(2),
        marginRight: 'auto'
    },
    button_back: {
        backgroundColor: '#9575cd',
        '&:hover': {
          backgroundColor: '#673ab7',
        },
        marginTop: theme.spacing(2),
        marginLeft: 'auto',
    },
}));
const steps= Questions_Answers


const MainForm = () => {
    const classes = useStyles();
    const [activeStep, setActiveStep] = React.useState(0);
    const [answers, setAnswers ]= React.useState({});

    const getChooseAns = (step,index) => {
        setAnswers({...answers, [step]: parseInt(index)});
    };


    const handleNext = () => {
        setActiveStep(activeStep + 1);
    };

    const handleBack = () => {
        setActiveStep(activeStep - 1);
    };

    return (
        <React.Fragment>
            <main className={classes.layout}>
                <Paper className={classes.paper}>
                    <React.Fragment>
                        {/* Here we need to send the answers to the server */}
                        {activeStep === steps.length ? (
                            <React.Fragment>
                                <Typography variant="h5" gutterBottom>
                                    Thank you for your order.
                                </Typography>
                                <Typography variant="subtitle1">
                                    Your order number is #2001539. We have emailed your order confirmation, and will
                                    send you an update when your order has shipped.
                                </Typography>
                            </React.Fragment>
                        ) : (
                            <React.Fragment>
                                <QuestionAnswers
                                    answers={answers}
                                    step={activeStep}
                            question={steps[activeStep].question}
                            using_image_question={steps[activeStep].using_image_question}
                            image_url_question={steps[activeStep].image_url_question}
                            list_ans={steps[activeStep].list_ans}
                            using_image_ans={steps[activeStep].using_image_ans}
                            getchooseans={getChooseAns}
                            />
                                <div className={classes.buttons}>
                                    <Button

                                        onClick={handleNext}
                                        className={classes.button_next}
                                    >
                                        {activeStep === steps.length - 1 ? 'סיום' : 'הבא'}
                                    </Button>
                                    {activeStep !== 0 && (
                                        <Button onClick={handleBack} className={classes.button_back}>
                                            חזור
                                        </Button>
                                    )}
                                </div>
                            </React.Fragment>
                        )}
                    </React.Fragment>
                </Paper>
            </main>
        </React.Fragment>
    );
}

export default MainForm;
