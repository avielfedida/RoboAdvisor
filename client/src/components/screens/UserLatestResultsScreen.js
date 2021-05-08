import React, { useState, useEffect } from "react";
import { Row, Col, Container, Form, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Loader from "../reusables/Loader";
import Message from "../reusables/Message";
import LatestResults from "../reusables/LatestResults";

const UserLatestResultsScreen = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    if (!userInfo) {
      navigate("/");
    }
  }, [navigate, userInfo]);

  return (
    <Container className="offset_nav rtl text-right">
      <Row>
        <Col xs={12}>
          <LatestResults byUser={userInfo.email} />
        </Col>
      </Row>
    </Container>
  );
};

export default UserLatestResultsScreen;
