import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import {makeStyles} from "@material-ui/core/styles";
import { Link as RouterLink } from 'react-router-dom';

const drawerWidth = 240;



const useStyles = makeStyles((theme) => ({
    center_page: {
        backgroundColor: '#9fa8da',
        height: 545,
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.32,
        shadowRadius: 5.46,
        elevation: 9,
    },
    main_title: {
        fontFamily: "cursive",
        textAlign: "center",
        fontSize: 100,
    },
    secende_title:{
        fontFamily: 'Suez One',
        textAlign: "center",
        fontSize: 30,
        direction: "rtl"
    },
     button_list: {
        display: 'flex',
        justifyContent:'center',
        alignItems:'center',
        left: 50 ,
         '& > *': {
             margin: theme.spacing(5),
             padding: 20,
             fontSize: 25,
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
    button_1: {
        backgroundColor: '#9575cd',
        '&:hover': {
          backgroundColor: '#673ab7',
        },
    },
    button_2: {
        backgroundColor: '#5c6bc0',
        '&:hover': {
          backgroundColor: '#3f51b5',
        },
    },
    button_3: {
        backgroundColor: '#42a5f5',
        '&:hover': {
          backgroundColor: '#2196f3',
        },
    },
}));

const HomePage = () =>  {
    const classes = useStyles();
    return (
        <div >
            <CssBaseline />
            <Container fixed  className={classes.center_page}>
                <Typography className={classes.main_title}  >
                    OMAN
                </Typography>
                <Typography className={classes.secende_title}  >
                    ROBO ADV- הפתח שלך לעולם חדש
                </Typography>
                <div className={classes.button_list}>
                    <Button className={classes.button_1} >
                        אני רוצה לדעת יותר
                    </Button>
                    <Button className={classes.button_2} >
                      בניית תיק השקעות
                    </Button>
                    <Button className={classes.button_3}  component={RouterLink} to="/forum">
                      בואו לדבר על זה
                    </Button>
                </div>

            </Container>
        </div>
    );
};

export default HomePage;