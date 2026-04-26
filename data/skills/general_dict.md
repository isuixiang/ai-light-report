---
name: general_dict
description: 提供通过系统字典表（sysdict）将业务表中的字典值翻译为中文名称的规则。
version: 1.0.2
date: 2026-02-15
---

# 通用技能：字典项翻译

## 技能描述
当查询的字段存储的是字典值（如教育程度的代码）时，此技能提供通过关联`sysdict`系统字典表，将这些代码转换为对应的、可读的中文名称的方法。

## 核心规则
1.  查询包含需要翻译的字典字段（如`employee.education`）时，必须左连接`sysdict`表。
2.  连接条件为：`业务表.字典字段 = sysdict.value` 且 `sysdict.code = '字典编码'`。
3.  输出时，用`sysdict.name`字段替代或补充业务表中的原始字典值字段。
4.  目前系统中，字典编码`code`为`'education'`的表项用于翻译`employee`表的`education`字段。

### 字典项对照表
| 表名     | 字段名    | 字典编码(code) | 获取中文名称的字段 |
| :------- | :-------- | :------------- | :----------------- |
| employee | education | 'education'    | sysdict.name       |

## SQL示例

### 示例1：查询员工姓名及其可读的学历信息
```sql
SELECT
    e.`name` AS `姓名`,
    d.`name` AS `学历`
FROM `employee` e
LEFT JOIN `sysdict` d ON e.`education` = d.`value` AND d.`code` = 'education';
```

### 示例2：查询所有硕士学历的员工名单
```sql
SELECT
    e.`name` AS `姓名`
FROM `employee` e
INNER JOIN `sysdict` d ON e.`education` = d.`value` AND d.`code` = 'education'
WHERE d.`name` = '硕士';
```

