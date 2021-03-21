import React from "react";
import { Image } from "react-bootstrap";

const Logo = () => {
  return (
    <h4>
      Robo
      <Image
        id="logo1"
        src="/images/icon2.png"
        style={{ maxWidth: "3rem", marginTop: "-1rem" }}
      />
      Advisor
    </h4>
  );
};

export default Logo;
