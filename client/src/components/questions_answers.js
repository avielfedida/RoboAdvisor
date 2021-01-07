// import MainForm from "./questionAnswersForm";
// const ans_O1 = ['בעוד שנה או פחות', 'בעוד שנה לשנתיים', 'בעוד 3 שנים ל-4 שנים','בעוד 5 שנים ל-7 שנים', 'בעוד 8 שנים ל-10 שנים', 'בעוד יותר מ-11 שנים']
// const ans_O2 = ['כשנה או פחות', 'בין שנה ל-4 שנים', 'בין 5 ל-7 שנים', 'בין 8 ל-10 שנים', 'יותר מ-11 שנים']
// const ans_O3 = ['מסכים לחלוטין', 'מסכים', 'לא מסכים', 'בשום פנים ואופן לא ']
// const ans_O4 = ['q4_ans1.PNG','q4_ans3.PNG','q4_ans3.PNG']//images
// const ans_O5 = ['q5_ans1.PNG','q5_ans3.PNG','q5_ans3.PNG']//images
// const ans_O6 = ['1','2','3','4','5']
// const ans_O7 = ['1','2','3','4','5']
// const ans_O8 = ['שנתיים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 2%',
//                 '4 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 5%',
//                 '5 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 6%',
//                 '6 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 8%',
//                 '7 שנים בתוך תקופה של 20 שנים היו בהפסד אך בסוף היית ברווח של 9%']
// const Questions_Answers = [
//     {question: 'מתי אתה מתכנן להתחיל למשוך חלק מהכסף?', using_image_question: false, image_url_question: null,list_ans: ans_O1, using_image_ans: false},
//     {question: 'למשך כמה זמן אתה מתכנן להשקיע את הכסף?', using_image_question: false, image_url_question: null,list_ans: ans_O2, using_image_ans: false},
//     {question: 'אני מוכן לקחת סיכון ולחוות ירידות גדולות לעיתים קרובות בתיק ההשקעות שלי במידה וזה יביא לי תשואות גבוהות בטווח הרחוק.', using_image_question: false, image_url_question:null,list_ans: ans_O3, using_image_ans: false },
//     {question: 'בתמונות הבאות נתונים הסיכונים אפשריים והרווחים אפשריים, לאיזה מהתמונות אתה הכי מתחבר?', using_image_question: false, image_url_question: null, list_ans: ans_O4, using_image_ans: true },
//     {question: 'בתמונות הבאות נתונים הסיכונים אפשריים והרווחים אפשריים, לאיזה מהתמונות אתה הכי מתחבר?', using_image_question: false, image_url_question: null, list_ans: ans_O5, using_image_ans: true },
//     {question: 'לפי התמונה הבאה, איזה תיק תבחר?', using_image_question: true, image_url_question: 'q6.PNG', list_ans: ans_O6, using_image_ans: false},
//     {question: 'במידה ותרצה להשקיע 100,000 למשך שנה איזה מבין האפשרויות הבאות היית בוחר:', using_image_question: true, image_url_question: 'q7.PNG', list_ans: ans_O7, using_image_ans: false},
//     {question: 'איזה מהאופציות הבאות היית מעדיף?', using_image_question: false, image_url_question: null, list_ans: ans_O8, using_image_ans: false},
// ];
//
// export default Questions_Answers;
//



import MainForm from "./questionAnswersForm";
const ans_O1 = ['פחות משנה', 'בין שנה לשנתיים', 'בין 3 שנים ל-4 שנים','בין 5 שנים ל-7 שנים', 'בין 8 שנים ל-10 שנים', '11 שנים או יותר']
const ans_O2 = ['מסכים לחלוטין', 'מסכים', 'לא מסכים', 'בשום פנים ואופן לא ']
const ans_O3 = ['A','B','C']
const ans_O4 = ['אני מוכן לקבל רווחים נמוכים ביותר בתמורה לכך שערך התיק יהיה עם השינויים הנמוכים ביותר ובתדירות הנמוכה ביותר',
                'אני מוכן לקבל רווחים בינוניים, בתמורה לכך שערך התיק יספוג שינויים נמוכים בתדירות נמוכה',
                'אני מוכן לקבל רווחים הכי גבוהים בלבד. אני מבין שערך התיק יחווה שינויים גדולים באופן תדיר.']
const ans_O5 = ['תיק 1','תיק 2','תיק 3','תיק 4','תיק 5']
const ans_O6 = ['תיק 1','תיק 2','תיק 3','תיק 4','תיק 5']
const ans_O7 = ['רווח ממוצע של 3% מערך התיק, בהסתברות של שנתיים מתוכם בהפסד',
                'רווח ממוצע של 5% מערך התיק, בהסתברות של 4 שנים מתוכם בהפסד',
                'רווח ממוצע של 6% מערך התיק, בהסתברות של 5 שנים מתוכם בהפסד',
                'רווח ממוצע של 8% מערך התיק, בהסתברות של 6 שנים מתוכם בהפסד',
                'רווח ממוצע של 9% מערך התיק, בהסתברות של 7 שנים מתוכם בהפסד']
const ans_O8 = ['אני לא אשנה את תיק ההשקעות שלי',
                'הייתי ממתין לפחות שנה לפני שאעבור לאופציות שהן יותר שמרניות',
                'הייתי ממתין לפחות שלושה חודשים לפני שאעבור לאופציות שהן יותר שמרניות',
                'הייתי מייד משנה לאופציות שמרניות יותר']


const Questions_Answers = [
    {question: 'לכמה זמן אתה רוצה להשקיע את הכסף?', using_image_question: false, image_url_question: null,example:'',list_ans: ans_O1, using_image_ans: false},
    {question: 'כידוע, רווחים גדולים דורשים סיכון גדול, האם היית מסכים לקחת סיכון גדול בו יתכן ותפסיד חלק גדול מההשקעה, עבור הסיכוי לקבל רווח גדול', using_image_question: false, image_url_question:null,example:'',list_ans: ans_O2, using_image_ans: false },
    {question: 'כל שורה בטבלה מטה מייצגת תיק השקעות המורכב מהסתברויות לסיכונים ורווחים, אילו מבין התיקים מייצג באופן הטוב ביותר את גישתך?', using_image_question: true, image_url_question: 'q3.jpeg', example:'', list_ans: ans_O3, using_image_ans: false },
    {question: ' כמה רווחים אתה מוכן לוותר על מנת להרגיש יותר בנוח מבחינת סיכון?', using_image_question: false, image_url_question: null ,example:'', list_ans: ans_O4, using_image_ans: false },
    {question: 'לפי הגרף הבא, המתאר טווחי רווח והפסד בתקופה של שנה, באיזה תיק תבחר להשקיע?' , using_image_question: true, image_url_question: 'q5.jpeg',example:'לדוגמה: בתיק 1 התשואה המוערכת בסוף השנה היא בין הפסד של 5.9% לבין רווח של 12.7%', list_ans: ans_O5, using_image_ans: false},
    {question: 'נניח שאתה רוצה להשקיע 100,000 ₪ למשך שנה. איזה מבין האפשרויות הבאות היית בוחר (הגרף באלפים), תוך התחשבות במצבים השונים:', using_image_question: true, image_url_question: 'q6.jpeg',
     example:'דוגמה : בתיק 1  שערכו ההתחלתי היה 100,000 ₪, ערך התיק המוערך בסוף השנה הוא:' +
            ' במקרה הטוב ביותר 113,000 ₪' +
            ', במקרה הממוצע 103,000 ₪' +
            ', במקרה הגרוע ביותר 94,000 ₪', list_ans: ans_O6, using_image_ans: false},
    {question: 'בהנחה שמדובר בתקופה של 20 שנים, איזה מהאופציות הבאות היית מעדיף?', using_image_question: false, image_url_question: null, example:'', list_ans: ans_O7, using_image_ans: false},
    {question: 'נניח שהשקעת 50,000 ₪ לפני 6 שנים. ברבעון האחרון, התיק הפסיד חצי מרווחיו הקודמים, כמתואר בגרף הבא. איזה מהפעולות הבאות היית נוקט?', using_image_question: true, image_url_question: 'q8.jpeg', example:'', list_ans: ans_O8, using_image_ans: false},

];

export default Questions_Answers;
