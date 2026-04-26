---
name: subskill_salary
description: 专门处理关于员工工资、月薪、奖金、个税等薪资相关的查询，支持按员工、按年份、按月份等多维度筛选。
version: 1.0.2
date: 2026-02-15
---

# 子技能：工资信息查询

## 技能描述
该技能专门处理关于员工工资、月薪、奖金、个税等薪资数据的查询。它能根据员工、时间（年/月）等条件进行筛选，并确保输出的金额单位为元。

## 核心规则
1.  必须隐藏主键 `id` 和逻辑外键 `emp_id`。
2.  当查询需要显示员工信息时，必须通过 `emp_id` 关联 `employee` 表以获取员工姓名等可读信息。
3.  所有金额字段（如 `basic_amount`, `bonus_amount`, `tax_amount`, `fact_amount`）默认以元为单位输出。
4.  对于 `paydate` 字段，必须应用“日期处理”规则，将其格式化为可读的字符串格式。
5.  可以按 `year` 和 `month` 字段进行时间范围的筛选。

## 表结构定义
-   **表名：salary**
-   **中文名称**：工资发放表
-   **用途描述**：用于存储企业员工每个月的工资发放记录，包括年份、月份、基本工资、奖金、个税、实际发放金额和发放日期等。
-   **主键**：`id`
-   **外键逻辑**：`emp_id`字段逻辑上关联`employee`表的`id`字段。

### 字段定义
| 字段名       | 类型          | 是否允许为空 | 默认值 | 注释                   | 示例值     |
| :----------- | :------------ | :----------- | :----- | :--------------------- | :--------- |
| id           | int           | 否           | -      | 主键ID                 | 1          |
| emp_id       | int           | 是           | NULL   | 员工ID，关联employee表 | 1          |
| year         | int           | 是           | NULL   | 年份                   | 2023       |
| month        | int           | 是           | NULL   | 月份                   | 10         |
| basic_amount | decimal(10,2) | 是           | NULL   | 基本工资               | 5000.00    |
| bonus_amount | decimal(10,2) | 是           | NULL   | 奖金                   | 1000.00    |
| tax_amount   | decimal(10,2) | 是           | NULL   | 个税                   | 150.00     |
| fact_amount  | decimal(10,2) | 是           | NULL   | 实发金额               | 5850.00    |
| paydate      | date          | 是           | NULL   | 发放日期               | 2023-10-15 |

## SQL示例

### 示例1：查询某员工在某个月的工资详情
```sql
SELECT
    e.`name` AS `员工姓名`,
    s.`year` AS `年份`,
    s.`month` AS `月份`,
    s.`basic_amount` AS `基本工资`,
    s.`bonus_amount` AS `奖金`,
    s.`tax_amount` AS `个税`,
    s.`fact_amount` AS `实发金额`,
    DATE_FORMAT(s.`payment_date`, '%Y-%m-%d') AS `发放日期`
FROM `salary` s
INNER JOIN `employee` e ON s.`emp_id` = e.`id`
WHERE e.`name` = '李四'
  AND s.`year` = 2023
  AND s.`month` = 10;
```

### 示例2：查询所有员工2023年的实发工资总额
```sql
SELECT
    e.`name` AS `员工姓名`,
    SUM(s.`fact_amount`) AS `全年实发工资总额`
FROM `salary` s
INNER JOIN `employee` e ON s.`emp_id` = e.`id`
WHERE s.`year` = 2023
GROUP BY e.`name`;
```

