---
name: general_status
description: 提供将数据库中存储的数字状态码转换为中文含义的规则，用于增强查询结果的可读性。
version: 1.0.2
date: 2026-02-15
---

# 通用技能：状态码映射

## 技能描述
当查询的字段是用于表示特定状态的数字代码时（如性别、婚姻状况、在职状态），此技能提供标准的转换规则，将代码映射为用户能直接理解的中文标签。

## 核心规则
在执行`SELECT`查询时，对于以下表中的指定字段，必须使用`CASE WHEN`语句将其转换为对应的中文含义。

### 状态映射表
| 表名     | 字段名  | 值-中文映射               | 说明     |
| :------- | :------ | :------------------------ | :------- |
| employee | gender  | 1 -> '男性'，2 -> '女性'  | 性别     |
| employee | married | 0 -> '未婚'，1 -> '已婚'  | 是否已婚 |
| employee | state   | 0 -> '离职' ，1 -> '在职' | 是否在职 |

## SQL示例

### 示例1：查询员工信息并显示所有状态的中文描述
```sql
SELECT
    `name` AS `姓名`,
    CASE `gender` WHEN 1 THEN '男性' WHEN 2 THEN '女性' END AS `性别`,
    CASE `married` WHEN 0 THEN '未婚' WHEN 1 THEN '已婚' END AS `婚姻状况`,
    CASE `state` WHEN 0 THEN '离职' WHEN 1 THEN '在职' END AS `在职状态`
FROM `employee`;
```

### 示例2：统计不同性别的员工数量
```sql
SELECT
    CASE `gender` WHEN 1 THEN '男性' WHEN 2 THEN '女性' END AS `性别`,
    COUNT(*) AS `人数`
FROM `employee`
GROUP BY `gender`;
```