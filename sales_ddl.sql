
--DDL for Sales table

DROP TABLE IF EXISTS `clever-tooling-352705.sales.sales`;
CREATE TABLE `clever-tooling-352705.sales.sales`
(
  Region STRING,
  Country STRING,
  Item_Type STRING,
  Sales_Channel STRING,
  Order_Priority STRING,
  Order_Date STRING,
  Order_ID STRING,
  Ship_Date STRING,
  Units_Sold FLOAT64,
  Units_Price FLOAT64,
  Units_Cost FLOAT64,
  Total_Revenue FLOAT64,
  Total_Cost FLOAT64,
  TOtal_Profit FLOAT64
);