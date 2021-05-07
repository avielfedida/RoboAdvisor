import React from "react";

const Copyrights = () => {
  return (
    <div>
      <span>
        .הפלטפורמה הינה למטרת מחקר אקדמאי בלבד. אין לראות במערכת כהמלצה או יעוץ
      </span>
      &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
      <span>
        <a href="#">RoboAdvisor כל הזכויות שמורות ל</a> &copy;{" "}
        {new Date().getFullYear()}
      </span>
    </div>
  );
};

export default Copyrights;
