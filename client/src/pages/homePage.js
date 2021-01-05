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
         marginTop:100,
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
             backgroundColor: '#000',
            color :'white',

            '&:hover': {
                backgroundColor: 'white',
                color :'#000',
                borderColor: '#000',
                border: '2px solid'
            },
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
                    MONA
                </Typography>
                <Typography className={classes.secende_title}  >
                    ROBO ADV- הפתח שלך לעולם חדש
                </Typography>
                <div className={classes.button_list}>
                    <Button  >
                        אני רוצה לדעת יותר
                    </Button>
                    <Button  component={RouterLink} to="/mainForm" >
                      בניית תיק השקעות
                    </Button>
                    <Button >
                      בואו לדבר על זה
                    </Button>
                </div>

            </Container>
        </div>
    );
};

export default HomePage;