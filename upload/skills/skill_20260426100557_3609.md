---
name: general_formula
description: 提供工作年限、年龄、收入区间等复杂业务指标的计算公式和实现方法。
---

# 通用技能：业务指标计算

## 技能描述
此技能封装了数据库中不直接存储，但需要通过现有字段计算得出的业务指标（如工作年限、年龄、收入区间等），为统计分析提供支持。

## 核心规则
1.  **工作年限**: 计算员工的工作年限时，使用公式 `TIMESTAMPDIFF(YEAR, hiredate, COALESCE(firedate, CURDATE()))`。如果员工在职（`firedate`为NULL），则计算到当前日期。
2.  **工资区间统计**: 用于统计员工的年收入水平。年收入的计算方式为 `SUM(salary.fact_amount)` 并按年分组。然后根据预定义的区间进行分类。
    -   区间定义: `'<=50000'`, `'50000~60000'`, `'60000~70000'`, `'>=70000'`

## SQL示例

### 示例1：计算每个员工的工作年限
```sql
SELECT
    `name` AS `员工姓名`,
    TIMESTAMPDIFF(YEAR, `hiredate`, COALESCE(`firedate`, CURDATE())) AS `工作年限`
FROM `employee`;
```

### 示例2：按年收入区间统计员工人数
```sql
SELECT
    CASE
        WHEN annual_income <= 50000 THEN '<=50000'
        WHEN annual_income > 50000 AND annual_income <= 60000 THEN '50000~60000'
        WHEN annual_income > 60000 AND annual_income <= 70000 THEN '60000~70000'
        WHEN annual_income > 70000 THEN '>=70000'
    END AS `工资区间`,
    COUNT(*) AS `员工人数`
FROM (
    SELECT
        e.`id`,
        SUM(s.`fact_amount`) AS `annual_income`
    FROM `employee` e
    LEFT JOIN `salary` s ON e.`id` = s.`emp_id`
    WHERE s.`year` = 2023
    GROUP BY e.`id`
) AS `emp_annual_income`
GROUP BY `工资区间`;
```