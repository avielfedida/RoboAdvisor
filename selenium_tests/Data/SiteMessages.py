from dataclasses import dataclass


@dataclass
class SiteMessages:
    INVALID_LOGIN_CREDENTIALS = "שם משתמש/סיסמה לא נמצאו"
    REGISTER_SUCCESSFULLY = "המשתמש נרשם בהצלחה למערכת"
    REGISTER_ALREADY_USER_EXISTS = "כבר קיים משתמש רשום למערכת עם מייל זה"
    PASSWORD_CHANGED_SUCCESSFULLY = "הסיסמה עודכנה בהצלחה"
    PROFILE_UPDATED_SUCCESSFULLY = "הפרופיל עודכן בהצלחה"
    FIRST_NAME_CANT_BE_EMPTY = "השם לא יכול להיות ריק"
    LAST_NAME_CANT_BE_EMPTY = "שם המשפחה לא יכול להיות ריק"
    ENTER_OLD_PASSWORD = "אנא הקלד/י את סיסמתך הישנה"
    PASSWORD_CANNOT_BE_EMPTY = "הסיסמה לא יכולה להיות ריקה"
    PASSWORD_DO_NOT_MATCH = "הסיסמאות אינן תואמות"