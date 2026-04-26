# LightReport

[中文](README.md)

LightReport is a **lightweight, intelligent** reporting tool powered by Large Language Models (LLMs). It automatically understands database semantics and generates SQL queries through natural language interaction, enabling rapid creation of interactive visual reports.

No complex configuration required. Supports Excel / database integration for **simple yet efficient** report generation.

## ✨ Key Features

- **📄 Excel Template Import**  
  Supports various report templates, from simple to complex, with perfect compatibility for complex definitions such as merged cells and formulas.

- **💬 Natural Language Interaction**  
  Automatically parses user queries to understand intent and objectives, accurately identifying key information and context. Supports complex conditions and multi-dimensional reporting logic.

- **⚡ One-Click Logic Generation**  
  Intelligently recognizes data characteristics of report templates and generates complete reporting logic with a single click, while also supporting customization and secondary editing of report logic.

- **🧠 Multi-LLM Support**  
  Integrates mainstream LLMs such as DeepSeek, Kimi, and Qwen, with flexible switching capabilities.

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher → [Download](https://www.python.org/downloads/)
- MySQL 5.7 or higher → [Download](https://downloads.mysql.com/archives/community/)

### Clone the Repository

```bash
git clone https://github.com/isuixiang/ai-light-report.git
cd ai-light-report
```

### Install Dependencies

> **Recommendation**: Create and activate a virtual environment before proceeding.

```bash
pip install -r requirements.txt
```

### Database Initialization

#### 1. Project Database

```bash
# Create a database in MySQL (choose any name)
# Then import the initialization script
mysql -u your_user -p your_project_db < data/db/ailightreport.sql
```

#### 2. Demo Database (Optional)

```bash
mysql -u your_user -p your_demo_db < data/db/dataanalysis.sql
```

### Configuration

Copy the example configuration and modify the database connection information:

```bash
cp example.env .env
```

Edit the `.env` file:

```env
# DB PARAMS
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "your_database_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
```

### Start the Service

```bash
flask run
```

After successful startup, visit:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

**Default login account**: `admin` / `123456`

## 📖 User Guide

1. **Connect Data Source**  
   Supports MySQL and SQL Server. Create a data source using the demo database as an example.

2. **Configure Skills**  
   Add skills to the created data source. Skill files are located in the `data/skills` directory under the project root.

3. **Add LLM**  
   Configure API Keys for the LLM you use (supports DeepSeek, Kimi, Qwen, etc.) in "Model Management".

4. **Add Report Template**  
   Upload or select an Excel template (templates are stored in `data/excels`).

## 🛠 Tech Stack

- **Backend**: Flask
- **Database**: MySQL
- **AI Models**: DeepSeek / Kimi / Qwen, etc.
- **Reporting**: Excel template parsing

## 🤝 Contributing

Issues and Pull Requests are welcome.  
If you have any suggestions for improvements or new feature ideas, feel free to reach out to us.

## 📬 Contact Us

- **QQ**: 1029993198
- **Email**: [zyq55917@hotmail.com](mailto:zyq55917@hotmail.com)
- **Issues**: [GitHub Issues](https://github.com/isuixiang/ai-light-report/issues)

## 📄 License

This project is open-sourced under the **Apache 2.0** license. See the [LICENSE](LICENSE) file for details.

