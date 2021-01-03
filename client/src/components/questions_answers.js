import MainForm from "./questionAnswersForm";
const ans_O1 = ['בעוד שנה או פחות', 'בעוד שנה לשנתיים', 'בעוד 3 שנים ל-4 שנים','בעוד 5 שנים ל-7 שנים', 'בעוד 8 שנים ל-10 שנים', 'בעוד יותר מ-11 שנים']
const ans_O2 = ['כשנה או פחות', 'בין שנה ל-4 שנים', 'בין 5 ל-7 שנים', 'בין 8 ל-10 שנים', 'יותר מ-11 שנים']
const ans_O3 = ['מסכים לחלוטין', 'מסכים', 'לא מסכים', 'בשום פנים ואופן לא ']
const ans_O4 = ['q4_ans1.PNG','q4_ans3.PNG','q4_ans3.PNG']//images
const ans_O5 = ['q5_ans1.PNG','q5_ans3.PNG','q5_ans3.PNG']//images
const ans_O6 = ['1','2','3','4','5']
const ans_O7 = ['1','2','3','4','5']
const ans_O8 = ['שנתיים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 2%',
                '4 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 5%',
                '5 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 6%',
                '6 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 8%',
                '7 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 9%']
const Questions_Answers = [
    {question: 'מתי אתה מתכנן להתחיל למשוך חלק מהכסף?', using_image_question: false, image_url_question: null,list_ans: ans_O1, using_image_ans: false},
    {question: 'למשך כמה זמן אתה מתכנן להשקיע את הכסף?', using_image_question: false, image_url_question: null,list_ans: ans_O2, using_image_ans: false},
    {question: 'אני מוכן לקחת סיכון ולחוות ירידות גדולות לעיתים קרובות בתיק ההשקעות שלי במידה וזה יביא לי תשואות גבוהות בטווח הרחוק.', using_image_question: false, image_url_question:null,list_ans: ans_O3, using_image_ans: false },
    {question: 'בתמונות הבאות נתונים הסיכונים אפשריים והרווחים אפשריים, לאיזה מהתמונות אתה הכי מתחבר?', using_image_question: false, image_url_question: null, list_ans: ans_O4, using_image_ans: true },
    {question: 'בתמונות הבאות נתונים הסיכונים אפשריים והרווחים אפשריים, לאיזה מהתמונות אתה הכי מתחבר?', using_image_question: false, image_url_question: null, list_ans: ans_O5, using_image_ans: true },
    {question: 'לפי התמונה הבאה, איזה תיק תבחר?', using_image_question: true, image_url_question: 'q6.PNG', list_ans: ans_O6, using_image_ans: false},
    {question: 'במידה ותרצה להשקיע 100,000 למשך שנה איזה מבין האפשרויות הבאות היית בוחר:', using_image_question: true, image_url_question: 'q7.PNG', list_ans: ans_O7, using_image_ans: false},
    {question: 'איזה מהאופציות הבאות היית מעדיף?', using_image_question: false, image_url_question: null, list_ans: ans_O8, using_image_ans: false},
];

export default Questions_Answers;
