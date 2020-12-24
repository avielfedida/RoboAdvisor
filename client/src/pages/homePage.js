    import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

import {makeStyles} from "@material-ui/core/styles";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
    center_page: {
        backgroundColor: '#9fa8da',
        height: 500,
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
        fontFamily: "cursive",
        textAlign: "center",
        fontSize: 30,
        direction: "rtl"
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

                </Container>
        </div>
    );
};

export default HomePage;