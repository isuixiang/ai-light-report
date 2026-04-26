LightReport 是一个轻量级的智能报表工具。无需复杂配置，快速接入数据源，自动生成交互式可视化报表。支持Excel/数据库对接，实现简单且高效的报表制作。

系统基于人工智能大语言模型实现，通过自然语言交互，智能理解数据库语义并构建SQL查询语句，支持一键生成报表逻辑与自定义报表逻辑。

## 核心功能

- **Excel模板导入**：Excel模板导入功能，支持从简单到复杂的各类报表模板，支持单元格合并和计算公式等复杂定义。
- **自然语言交互**：自动解析用户提问的语义与目标，准确识别关键信息与上下文关系。支持复杂条件与多维度报表逻辑。
- **一键生成逻辑**：智能识别报表模板的数据特征，一键生成完整的报表逻辑，同时支持报表逻辑的自定义功能。

## 安装指南

### 前置条件

- Python 3.9+版本，点击 [下载](https://www.python.org/downloads/)
- MySQL 5.7+版本，点击 [下载](https://downloads.mysql.com/archives/community/)

### 克隆仓库

```
git clone https://github.com/isuixiang/ai-light-report.git
cd ai-light-report
```

### 安装依赖包

在项目根目录下，执行以下命令安装依赖包：

```
pip install -r requirements.txt
```

**注**：建议创建虚拟环境，在虚拟环境中安装依赖包。

### 创建数据库

#### 项目数据库

创建项目数据库的步骤如下：

1. 在 MySQL 中创建一个数据库
2. 进入项目的 `data/db` 目录
3. 在新创建的项目数据库中导入 `ailightreport.sql` 初始化数据库

#### 演示数据库

用于演示的数据库，创建步骤如下：

1. 在 MySQL 中创建一个数据库
2. 进入项目的 `data/db` 目录
3. 在新创建的演示数据库中导入 `dataanalysis.sql` 初始化数据库

### 修改配置文件

将项目根目录下的 `example.env` 复制到 `.env`，修改 `.env` 中的数据库参数：

```
# DB PARAMS
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "your_database_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
```

## 使用指南

### 启动项目

打开一个终端控制台窗口，使用以下命令启动服务：

```
flask run
```

启动成功后，在浏览器中输入网址 `http://127.0.0.1:5000` 访问。

登录用户：admin，初始登录密码：123456

### 连接数据源

支持 MySQL 和 SQLServer 两类关系数据库。

创建一个数据源，数据使用我们前面已经创建的演示数据库。

### 配置技能

在已创建的数据源中添加技能（Skills）。技能文件在项目根目录下的 `data/skills` 目录中。

### 添加大模型

支持 DeepSeek、Kimi、Qwen 等大语言模型。

在模型管理中添加 LLMs 的 API Key。

### 添加报表模板

添加并配置报表模板，报表模板在项目根目录下的 `data/excels` 目录中。

## 联系我们

如你有更多问题，请提交 Issues，你也可以加入我们的技术交流群与我们交流。

QQ：1029993198

E-mail：zyq55917@hotmail.com
