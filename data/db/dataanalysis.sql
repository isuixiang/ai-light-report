/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : dataanalysis

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 04/04/2026 16:06:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for employee
-- ----------------------------
DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `no` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '工号',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
  `age` int(20) NULL DEFAULT NULL COMMENT '年龄',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '性别（1-男性，2-女性）',
  `married` tinyint(1) NULL DEFAULT NULL COMMENT '是否已婚（0-未婚，1-已婚）',
  `education` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '教育程度（学历），存储字典值',
  `hiredate` date NULL DEFAULT NULL COMMENT '雇佣日期',
  `firedate` date NULL DEFAULT NULL COMMENT '离职日期',
  `state` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态（0-离职，1-在职）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_employee_no`(`no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '雇员表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of employee
-- ----------------------------
INSERT INTO `employee` VALUES (1, 'A001', 'Alice', 22, 2, 0, '2', '2020-01-01', NULL, 1);
INSERT INTO `employee` VALUES (2, 'A002', 'Jason', 35, 1, 1, '3', '2020-05-01', '2025-04-30', 0);
INSERT INTO `employee` VALUES (3, 'A003', 'Tony', 46, 1, 0, '3', '2021-02-01', NULL, 1);
INSERT INTO `employee` VALUES (4, 'A004', 'Linda', 28, 2, 1, '4', '2022-03-01', NULL, 1);
INSERT INTO `employee` VALUES (5, 'A005', 'Jerry', 55, 2, 1, '5', '2023-06-01', NULL, 1);

-- ----------------------------
-- Table structure for salary
-- ----------------------------
DROP TABLE IF EXISTS `salary`;
CREATE TABLE `salary`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `emp_id` int(11) NOT NULL COMMENT '员工ID',
  `year` int(20) NULL DEFAULT NULL COMMENT '年份',
  `month` int(20) NULL DEFAULT NULL COMMENT '月份',
  `basic_amount` int(20) NULL DEFAULT NULL COMMENT '基本工资',
  `bonus_amount` int(20) NULL DEFAULT NULL COMMENT '奖金',
  `tax_amount` int(20) NULL DEFAULT NULL COMMENT '个税',
  `fact_amount` int(20) NULL DEFAULT NULL COMMENT '实际发放',
  `paydate` date NOT NULL COMMENT '发放日期',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_salary_year_month`(`year`, `month`) USING BTREE,
  INDEX `ix_salary_emp_id`(`emp_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '工资表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of salary
-- ----------------------------
INSERT INTO `salary` VALUES (1, 1, 2024, 1, 2000, 3000, 100, 4900, '2023-02-05');
INSERT INTO `salary` VALUES (2, 2, 2024, 1, 2000, 3500, 150, 5350, '2023-02-05');
INSERT INTO `salary` VALUES (3, 3, 2024, 1, 2000, 4000, 200, 5800, '2023-02-05');
INSERT INTO `salary` VALUES (4, 4, 2024, 1, 2000, 4500, 250, 6250, '2023-02-05');
INSERT INTO `salary` VALUES (5, 5, 2024, 1, 2000, 5000, 300, 6700, '2023-02-05');
INSERT INTO `salary` VALUES (6, 1, 2024, 2, 2000, 3000, 100, 4900, '2023-03-05');
INSERT INTO `salary` VALUES (7, 2, 2024, 2, 2000, 3500, 150, 5350, '2023-03-05');
INSERT INTO `salary` VALUES (8, 3, 2024, 2, 2000, 4000, 200, 5800, '2023-03-05');
INSERT INTO `salary` VALUES (9, 4, 2024, 2, 2000, 4500, 250, 6250, '2023-03-05');
INSERT INTO `salary` VALUES (10, 5, 2024, 2, 2000, 5000, 300, 6700, '2023-03-05');
INSERT INTO `salary` VALUES (11, 1, 2024, 3, 2000, 3000, 100, 4900, '2023-04-05');
INSERT INTO `salary` VALUES (12, 2, 2024, 3, 2000, 3500, 150, 5350, '2023-04-05');
INSERT INTO `salary` VALUES (13, 3, 2024, 3, 2000, 4000, 200, 5800, '2023-04-05');
INSERT INTO `salary` VALUES (14, 4, 2024, 3, 2000, 4500, 250, 6250, '2023-04-05');
INSERT INTO `salary` VALUES (15, 5, 2024, 3, 2000, 5000, 300, 6700, '2023-04-05');
INSERT INTO `salary` VALUES (16, 1, 2024, 4, 2000, 3300, 100, 5200, '2023-05-05');
INSERT INTO `salary` VALUES (17, 2, 2024, 4, 2000, 3800, 150, 5650, '2023-05-05');
INSERT INTO `salary` VALUES (18, 3, 2024, 4, 2000, 4300, 200, 6100, '2023-05-05');
INSERT INTO `salary` VALUES (19, 4, 2024, 4, 2000, 4800, 250, 6550, '2023-05-05');
INSERT INTO `salary` VALUES (20, 5, 2024, 4, 2000, 5300, 300, 7000, '2023-05-05');
INSERT INTO `salary` VALUES (21, 1, 2024, 5, 2000, 3300, 100, 5200, '2023-06-05');
INSERT INTO `salary` VALUES (22, 2, 2024, 5, 2000, 3800, 150, 5650, '2023-06-05');
INSERT INTO `salary` VALUES (23, 3, 2024, 5, 2000, 4300, 200, 6100, '2023-06-05');
INSERT INTO `salary` VALUES (24, 4, 2024, 5, 2000, 4800, 250, 6550, '2023-06-05');
INSERT INTO `salary` VALUES (25, 5, 2024, 5, 2000, 5300, 300, 7000, '2023-06-05');
INSERT INTO `salary` VALUES (26, 1, 2024, 6, 2000, 3300, 100, 5200, '2023-07-05');
INSERT INTO `salary` VALUES (27, 2, 2024, 6, 2000, 3800, 150, 5650, '2023-07-05');
INSERT INTO `salary` VALUES (28, 3, 2024, 6, 2000, 4300, 200, 6100, '2023-07-05');
INSERT INTO `salary` VALUES (29, 4, 2024, 6, 2000, 4800, 250, 6550, '2023-07-05');
INSERT INTO `salary` VALUES (30, 5, 2024, 6, 2000, 5300, 300, 7000, '2023-07-05');
INSERT INTO `salary` VALUES (31, 1, 2024, 7, 2000, 3600, 100, 5500, '2023-08-05');
INSERT INTO `salary` VALUES (32, 2, 2024, 7, 2000, 4100, 150, 5950, '2023-08-05');
INSERT INTO `salary` VALUES (33, 3, 2024, 7, 2000, 4600, 200, 6400, '2023-08-05');
INSERT INTO `salary` VALUES (34, 4, 2024, 7, 2000, 5100, 250, 6850, '2023-08-05');
INSERT INTO `salary` VALUES (35, 5, 2024, 7, 2000, 5600, 300, 7300, '2023-08-05');
INSERT INTO `salary` VALUES (36, 1, 2024, 8, 2000, 3600, 100, 5500, '2023-09-05');
INSERT INTO `salary` VALUES (37, 2, 2024, 8, 2000, 4100, 150, 5950, '2023-09-05');
INSERT INTO `salary` VALUES (38, 3, 2024, 8, 2000, 4600, 200, 6400, '2023-09-05');
INSERT INTO `salary` VALUES (39, 4, 2024, 8, 2000, 5100, 250, 6850, '2023-09-05');
INSERT INTO `salary` VALUES (40, 5, 2024, 8, 2000, 5600, 300, 7300, '2023-09-05');
INSERT INTO `salary` VALUES (41, 1, 2024, 9, 2000, 3600, 100, 5500, '2023-10-05');
INSERT INTO `salary` VALUES (42, 2, 2024, 9, 2000, 4100, 150, 5950, '2023-10-05');
INSERT INTO `salary` VALUES (43, 3, 2024, 9, 2000, 4600, 200, 6400, '2023-10-05');
INSERT INTO `salary` VALUES (44, 4, 2024, 9, 2000, 5100, 250, 6850, '2023-10-05');
INSERT INTO `salary` VALUES (45, 5, 2024, 9, 2000, 5600, 300, 7300, '2023-10-05');
INSERT INTO `salary` VALUES (46, 1, 2024, 10, 2000, 3900, 100, 5800, '2023-11-05');
INSERT INTO `salary` VALUES (47, 2, 2024, 10, 2000, 4400, 150, 6250, '2023-11-05');
INSERT INTO `salary` VALUES (48, 3, 2024, 10, 2000, 4900, 200, 6700, '2023-11-05');
INSERT INTO `salary` VALUES (49, 4, 2024, 10, 2000, 5400, 250, 7150, '2023-11-05');
INSERT INTO `salary` VALUES (50, 5, 2024, 10, 2000, 5900, 300, 7600, '2023-11-05');
INSERT INTO `salary` VALUES (51, 1, 2024, 11, 2000, 3900, 100, 5800, '2023-12-05');
INSERT INTO `salary` VALUES (52, 2, 2024, 11, 2000, 4400, 150, 6250, '2023-12-05');
INSERT INTO `salary` VALUES (53, 3, 2024, 11, 2000, 4900, 200, 6700, '2023-12-05');
INSERT INTO `salary` VALUES (54, 4, 2024, 11, 2000, 5400, 250, 7150, '2023-12-05');
INSERT INTO `salary` VALUES (55, 5, 2024, 11, 2000, 5900, 300, 7600, '2023-12-05');
INSERT INTO `salary` VALUES (56, 1, 2024, 12, 2000, 3900, 100, 5800, '2024-01-05');
INSERT INTO `salary` VALUES (57, 2, 2024, 12, 2000, 4400, 150, 6250, '2024-01-05');
INSERT INTO `salary` VALUES (58, 3, 2024, 12, 2000, 4900, 200, 6700, '2024-01-05');
INSERT INTO `salary` VALUES (59, 4, 2024, 12, 2000, 5400, 250, 7150, '2024-01-05');
INSERT INTO `salary` VALUES (60, 5, 2024, 12, 2000, 5900, 300, 7600, '2024-01-05');

-- ----------------------------
-- Table structure for sysdict
-- ----------------------------
DROP TABLE IF EXISTS `sysdict`;
CREATE TABLE `sysdict`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典代码',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典名称',
  `value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '字典值',
  `remark` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_sysdict_code`(`code`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统字典表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sysdict
-- ----------------------------
INSERT INTO `sysdict` VALUES (1, 'education', '初中', '1', '学历，教育程度');
INSERT INTO `sysdict` VALUES (2, 'education', '高中', '2', NULL);
INSERT INTO `sysdict` VALUES (3, 'education', '大专', '3', NULL);
INSERT INTO `sysdict` VALUES (4, 'education', '本科', '4', NULL);
INSERT INTO `sysdict` VALUES (5, 'education', '硕士', '5', NULL);
INSERT INTO `sysdict` VALUES (6, 'education', '博士', '6', NULL);

SET FOREIGN_KEY_CHECKS = 1;
