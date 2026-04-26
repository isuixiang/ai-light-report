---
name: subskill_employee
description: 专门处理关于员工个人档案、基本信息、在职状态等方面的查询，能够准确翻译性别、婚姻、在职状态等编码。
version: 1.0.2
date: 2026-02-15
---

# 子技能：员工信息查询

## 技能描述
该技能专门处理关于员工个人档案、基本信息（如姓名、工号、年龄）、在职状态等方面的查询。它能够准确地将数据库中的数字状态码翻译成用户可读的中文信息。

## 核心规则
1.  必须隐藏 `id` 主键字段。
2.  对于 `gender`, `married`, `state` 字段，必须应用“状态映射”规则，将数字码转换为中文描述。
3.  对于 `education` 字段，必须应用“字典翻译”规则，通过关联 `sysdict` 表获取对应的学历中文名称。
4.  对于 `hiredate` 和 `firedate` 字段，必须应用“日期处理”规则，将其格式化为可读的字符串格式。

## 表结构定义
-   **表名：employee**
-   **中文名称**：员工信息表
-   **用途描述**：用于存储企业员工（雇员）的基本信息，包括工号、姓名、年龄、性别、婚姻状况、教育程度、雇佣日期和离职日期等。
-   **主键**：`id`
-   **外键逻辑**：无

### 字段定义
| 字段名    | 类型        | 是否允许为空 | 默认值 | 注释                         | 示例值       |
| :-------- | :---------- | :----------- | :----- | :--------------------------- | :----------- |
| id        | int         | 否           | -      | 主键ID                       | 1            |
| no        | varchar(10) | 是           | NULL   | 工号，唯一索引               | 'E00001'     |
| name      | varchar(20) | 是           | NULL   | 姓名                         | '张三'       |
| age       | int         | 是           | NULL   | 年龄                         | 30           |
| gender    | tinyint(1)  | 是           | NULL   | 性别（1-男性，2-女性）       | 1            |
| married   | tinyint(1)  | 是           | NULL   | 是否已婚（0-未婚，1-已婚）   | 1            |
| education | varchar(10) | 是           | NULL   | 教育程度（学历），存储字典值 | '1'          |
| hiredate  | date        | 是           | NULL   | 雇佣日期（入职日期）         | '2020-01-01' |
| firedate  | date        | 是           | NULL   | 离职日期（解雇日期）         | NULL         |
| state     | tinyint(1)  | 否           | 1      | 在职状态（0-离职，1-在职）   | 1            |

## SQL示例

### 示例1：查询所有在职员工

```
SELECT
	emp.`no` AS 工号,
    emp.`name` AS `姓名`,
    emp.`age` AS 年龄,
    CASE emp.`gender`
        WHEN 1 THEN '男'
        WHEN 2 THEN '女'
        ELSE '未知'
    END AS `性别`,
    CASE emp.`married`
        WHEN 0 THEN '未婚'
        WHEN 1 THEN '已婚'
        ELSE '未知'
    END AS `是否已婚`,
    dict.name AS 教育程度,
    emp.`hiredate` AS 入职日期
FROM `employee` emp
LEFT JOIN `sysdict` dict ON emp.`education` = dict.`value` AND dict.`code` = 'education'
WHERE emp.`state` = 1;
```

### 示例2：查询所有女性员工的姓名和婚姻状况
```sql
SELECT
    `name` AS `姓名`,
    CASE `married`
        WHEN 0 THEN '未婚'
        WHEN 1 THEN '已婚'
        ELSE '未知'
    END AS `婚姻状况`
FROM `employee`
WHERE `gender` = 2;
```

### 示例3：查询所有在职员工的工号和入职日期
```sql
SELECT
    `no` AS `工号`,
    DATE_FORMAT(`hiredate`, '%Y-%m-%d') AS `入职日期`
FROM `employee`
WHERE `state` = 1;
```