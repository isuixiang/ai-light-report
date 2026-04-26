/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : ailightreport

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 10/02/2026 14:22:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chatmessage
-- ----------------------------
DROP TABLE IF EXISTS `chatmessage`;
CREATE TABLE `chatmessage`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `ds_id` int(11) NOT NULL COMMENT '数据源ID',
  `role` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称（user-用户，ai-大模型）',
  `type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '数据类型（text/sql/table）',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '对话内容（JSON格式，包括type和value两个键，type区分text/sql/table，value存储对话内容）',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_chatmessage_template_id`(`ds_id`) USING BTREE,
  INDEX `ix_chatmessage_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '聊天消息' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for datasource
-- ----------------------------
DROP TABLE IF EXISTS `datasource`;
CREATE TABLE `datasource`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据源名称',
  `db_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据库类型',
  `db_host` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '数据库主机',
  `db_port` int(11) NULL DEFAULT NULL COMMENT '数据库端口',
  `db_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '数据库名称',
  `db_user` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '数据库用户',
  `db_password` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '数据库密码（加密）',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_datasource_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '数据源配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for dbtype
-- ----------------------------
DROP TABLE IF EXISTS `dbtype`;
CREATE TABLE `dbtype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据库类型',
  `port` int(11) NOT NULL COMMENT '默认端口',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '支持的数据库系统' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of dbtype
-- ----------------------------
INSERT INTO `dbtype` VALUES (1, 'MySQL', 3306);
INSERT INTO `dbtype` VALUES (2, 'SQLServer', 1433);

-- ----------------------------
-- Table structure for exceloutput
-- ----------------------------
DROP TABLE IF EXISTS `exceloutput`;
CREATE TABLE `exceloutput`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `template_id` int(11) NOT NULL COMMENT '模板ID',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '报表数据（JSON格式，包括row,col,value三个键值）',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'excel文件',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_exceloutput_template_id`(`template_id`) USING BTREE,
  INDEX `ix_exceloutput_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Excel报表输出' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for exceltemplate
-- ----------------------------
DROP TABLE IF EXISTS `exceltemplate`;
CREATE TABLE `exceltemplate`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `ds_id` int(11) NOT NULL COMMENT '数据源ID',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'excel文件',
  `pattern` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '模板内容',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '模板定义（JSON格式，包括row,col,type,value四个键值）',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_exceltemplate_ds_id`(`ds_id`) USING BTREE,
  INDEX `ix_exceltemplate_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Excel模板文件' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for llm
-- ----------------------------
DROP TABLE IF EXISTS `llm`;
CREATE TABLE `llm`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '大模型名称',
  `url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '接口调用URL',
  `apikey` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '大模型APIKEY',
  `used` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否默认（0-否，1-是）',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_llm_name`(`name`) USING BTREE,
  INDEX `ix_llm_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '大模型配置表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of llm
-- ----------------------------
INSERT INTO `llm` VALUES (1, 'deepseek', NULL, '1234567890', 0, '2025-11-10 19:42:37');
INSERT INTO `llm` VALUES (2, 'kimi', NULL, '1234567890', 0, '2025-11-14 11:27:37');
INSERT INTO `llm` VALUES (3, '千问', NULL, '1234567890', 1, '2025-11-14 11:30:21');

-- ----------------------------
-- Table structure for llmtype
-- ----------------------------
DROP TABLE IF EXISTS `llmtype`;
CREATE TABLE `llmtype`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'LLM类型',
  `remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '支持的大模型名称' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of llmtype
-- ----------------------------
INSERT INTO `llmtype` VALUES (1, 'deepseek', '模型 deepseek-chat');
INSERT INTO `llmtype` VALUES (2, 'kimi', '模型 kimi-k2-turbo-preview');
INSERT INTO `llmtype` VALUES (3, '千问', '模型 qwen3-max');

-- ----------------------------
-- Table structure for skills
-- ----------------------------
DROP TABLE IF EXISTS `skills`;
CREATE TABLE `skills`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `ds_id` int(11) NOT NULL COMMENT '数据源ID',
  `type` tinyint(1) NOT NULL COMMENT '类型（1-主技能，2-子技能，3-通用技能）',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '技能名称',
  `desc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `filename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文件名URL',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '文件内容',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_skills_unique`(`ds_id`, `name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '数据源技能文档' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序号',
  `no` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '账号',
  `pwd` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `create_time` datetime(0) NOT NULL COMMENT '创建时间',
  `state` tinyint(1) NOT NULL DEFAULT 1 COMMENT '状态（0-禁用，1-正常）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_user_no`(`no`) USING BTREE,
  INDEX `ix_user_create_time`(`create_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', 'Z0FBQUFBQnAzanRnTVFraS1HMEFxZ0Nhb0V6VHVGZ2d3cDhvajE5T2xTSHJweXNaUFJHQTQ3QmFtd2dfRno4YU0tUmNUeGhlcEk0Sm1mMnZESER5amhwQlNyQ1RwZmFWNkE9PQ==', 'Admin', '2025-12-28 10:56:58', 1);

SET FOREIGN_KEY_CHECKS = 1;
