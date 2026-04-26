---
name: general_date
description: 提供日期字段的格式化、筛选和计算规则，确保日期数据的正确输出与查询。
version: 1.0.2
date: 2026-02-15
---

# 通用技能：日期时间处理

## 技能描述
此技能定义了如何处理数据库中的日期和时间字段，包括在`SELECT`输出时进行格式化，以及在`WHERE`条件中进行精确或范围筛选的规则。

## 核心规则
1.  **日期格式化**: 所有日期类型字段（`date`, `datetime`）在输出时，必须使用 `DATE_FORMAT()` 函数进行格式化，以增强可读性。默认格式为 `'%Y-%m-%d'`（例如：2023-10-26）。
2.  **日期筛选**: 当用户提问涉及年份、月份或具体日期时，应使用 `year`, `month` 等函数或直接与格式化后的字符串进行比较来构建`WHERE`条件。
    -   例如：查询2023年的数据 -> `WHERE year = 2023` 或 `WHERE DATE_FORMAT(date_col, '%Y') = '2023'`。
    -   例如：查询10月份的数据 -> `WHERE month = 10` 或 `WHERE DATE_FORMAT(date_col, '%m') = '10'`。
    -   例如：查询某天之后的数据 -> `WHERE date_col > '2023-01-01'`。

## SQL示例

### 示例1：查询员工入职信息并格式化日期
```sql
SELECT
    `name` AS `姓名`,
    DATE_FORMAT(`hiredate`, '%Y-%m-%d') AS `入职日期`
FROM `employee`;
```

### 示例2：查询2024年1月之后入职的员工
```sql
SELECT
    `name` AS `姓名`,
    DATE_FORMAT(`hiredate`, '%Y-%m-%d') AS `入职日期`
FROM `employee`
WHERE `hiredate` > '2024-01-01';
```

### 示例3：查询所有在2023年5月发放的工资记录
```sql
SELECT
    e.`name` AS `员工姓名`,
    s.`fact_amount` AS `实发金额`,
    DATE_FORMAT(s.`payment_date`, '%Y-%m-%d') AS `发放日期`
FROM `salary` s
INNER JOIN `employee` e ON s.`emp_id` = e.`id`
WHERE s.`year` = 2023 AND s.`month` = 5;
```