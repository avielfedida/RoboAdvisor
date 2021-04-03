import React, { useState, useEffect, useMemo } from "react";
import { Container, Row, Col } from "react-bootstrap";
import queryString from "query-string";
import {
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

// const COLORS1 = ["#2b2e4a", "#e84545", "#903749", "#53354a"];
// const COLORS1  = ["#f39189", "#bb8082", "#6e7582", "#046582"];
// const COLORS1 = ["#440a67", "#93329e", "#b4aee8", "#ffe3fe"];
const COLORS1 = ["#693c72", "#c15050", "#d97642", "#d49d42"];

// const assets_mapper = (x) => {name: x.stock_price_ticker, value: x}

const Portfolio = ({ data }) => {
  const parsedData = data.map((x) => {
    return {
      asset_type: x.asset_type,
      name: x.stock_price_ticker,
      value: parseFloat(x.weight),
    };
  });
  const filteredData = parsedData.filter((x) => x.value > 0.0005);
  const stocksBonds = filteredData.reduce(
    (accumulator, currentValue) => {
      if (currentValue.asset_type === "stock") {
        accumulator[0].value += currentValue.value;
      } else {
        accumulator[1].value += currentValue.value;
      }
      accumulator[2].value -= currentValue.value;
      return accumulator;
    },
    [
      { name: "Stocks", value: 0 },
      { name: "Bonds", value: 0 },
      { name: "Not allocated", value: 1.0 },
    ]
  );

  const stocksAllocation = filteredData.filter((x) => x.asset_type === "stock");
  const bondsAllocation = filteredData.filter((x) => x.asset_type === "bond");

  return (
    <Container>
      <Row>
        <Col xs={4} style={{ textAlign: "center" }}>
          <h2>מניות</h2>
        </Col>
        <Col xs={4} style={{ textAlign: "center" }}>
          <h2>חלוקה</h2>
        </Col>
        <Col xs={4} style={{ textAlign: "center" }}>
          <h2>איגרות חוב</h2>
        </Col>
      </Row>
      <Row>
        <Col xs={4} className="pie_chart_container_col">
          <ResponsiveContainer height="100%" width="100%">
            <PieChart>
              <Pie data={stocksAllocation} dataKey="value" nameKey="name">
                {stocksAllocation.map((item, index) => (
                  <Cell
                    key={index}
                    strokeWidth={0}
                    fill={COLORS1[index % COLORS1.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Col>
        <Col xs={4} className="pie_chart_container_col">
          <ResponsiveContainer height="100%" width="100%">
            <PieChart>
              <Pie data={stocksBonds} dataKey="value" nameKey="name">
                {stocksBonds.map((item, index) => (
                  <Cell
                    key={index}
                    strokeWidth={0}
                    fill={COLORS1[index % COLORS1.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Col>
        <Col xs={4} className="pie_chart_container_col">
          <ResponsiveContainer height="100%" width="100%">
            <PieChart>
              <Pie data={bondsAllocation} dataKey="value" nameKey="name">
                {bondsAllocation.map((item, index) => (
                  <Cell
                    key={index}
                    strokeWidth={0}
                    fill={COLORS1[index % COLORS1.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </Col>
      </Row>
    </Container>
  );
};

export default Portfolio;
