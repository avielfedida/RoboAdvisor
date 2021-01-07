import React, {useEffect} from 'react';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Radio from '@material-ui/core/Radio';

const QuestionAnswers=({step,answers, question, using_image_question,image_url_question,example, list_ans, using_image_ans, getchooseans})=>{

  const [value, setValue] = React.useState(0);


  useEffect(() => {
      if (answers.hasOwnProperty(step)) {
          setValue(answers[step]);
      }
      else {
          setValue(0);
      }
  }, [step]);

  const AsImgQ = using_image_question;
  const handleChange=(event)=>{
      let step_index = parseInt( event.target.value)
      setValue(step_index)
      getchooseans(step, step_index )
  };

  let classes = {
      center_page: {
          minHeight : 450,
          shadowColor: "#303f9f",
          shadowOffset: {
              width: 0,
              height: 3,
          },
          shadowOpacity: 0.32,
          shadowRadius: 5.47,
          elevation: 9,
      },
      question: {
          color: '#000',
          fontFamily: 'Suez One',
          textAlign: "center",
          fontSize: 25,
          direction: "rtl",
      },
      img_question:{

          display: 'block',
          margin: 'auto',
      },
          form_control_label:{
              color: '#000',
              fontFamily: 'Suez One',
              textAlign: "center",
              fontSize: 14,
              direction: "rtl",

          },
          example :{
                    color: '#000',
          fontFamily: 'Suez One',
          textAlign: "center",
          fontSize: 16,
          direction: "rtl",
          }
  };
  // console.log(image_url_question);
   return (
      <div style={classes.center_page} >
          <h1 style={classes.question}>שאלה {step+1}:</h1 >
          <h1 style={classes.question}>{question}</h1>
          {AsImgQ ? (
            <img style={classes.img_question} src={require('../Images/'+image_url_question)}/>
            ) : null
          }
          {example.length>0 ?(<h1 style={classes.example}>{example}</h1>): null}
              <RadioGroup  name={step+"_q"} value={value} onChange={handleChange}>
                  {list_ans.map((text, index) => {
                      return (<FormControlLabel style={classes.form_control_label} key={index+1} value={index+1} control={<Radio color="primary" />} label={text}/>);
                  })}
              </RadioGroup>
      </div>
   );
}
export default QuestionAnswers;