# 07 - MySQL Database Guide

This guide covers the MySQL database integration for the Resume Builder application, including setup, schema design, CRUD operations, and the candidate management system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Schema Design](#schema-design)
4. [Configuration](#configuration)
5. [API Endpoints](#api-endpoints)
6. [Searching & Sorting](#searching--sorting)
7. [How It Works (Code Walkthrough)](#how-it-works)
8. [Common Operations](#common-operations)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **MySQL Server 8.0+** installed and running
- **Python 3.8+** with pip
- The following Python packages (included in `requirements.txt`):
  - `Flask-SQLAlchemy==3.1.1` — ORM for Flask
  - `PyMySQL==1.1.0` — Pure-Python MySQL client

### Installing MySQL

**Windows:**
Download from https://dev.mysql.com/downloads/installer/ and run the installer. Choose "Developer Default" setup type.

**macOS (Homebrew):**
```bash
brew install mysql
brew services start mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

---

## Database Setup

### Step 1: Configure Credentials

Edit `config.py` in the project root:

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''        # Set your MySQL root password here
MYSQL_DB = 'resume_builder'
MYSQL_PORT = 3306
```

You can also use environment variables:

```bash
set MYSQL_HOST=localhost
set MYSQL_USER=root
set MYSQL_PASSWORD=yourpassword
set MYSQL_DB=resume_builder
```

### Step 2: Create the Database

**Option A — Automatic (recommended):**

```bash
python init_db.py
```

This script will:
1. Connect to MySQL and create the `resume_builder` database
2. Create all required tables using SQLAlchemy

**Option B — Manual:**

```sql
CREATE DATABASE IF NOT EXISTS resume_builder
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Then start the app — tables are auto-created on first run:

```bash
python app.py
```

### Step 3: Verify

Visit `http://localhost:5000/health` — you should see:

```json
{
  "status": "ok",
  "message": "Server is running",
  "database": "connected"
}
```

---

## Schema Design

### `candidates` Table

| Column           | Type          | Constraints                | Description                        |
|------------------|---------------|----------------------------|------------------------------------|
| `id`             | INT           | PRIMARY KEY, AUTO_INCREMENT| Unique candidate ID                |
| `full_name`      | VARCHAR(255)  | NOT NULL, INDEX            | Candidate's full name              |
| `email`          | VARCHAR(255)  | NOT NULL, UNIQUE, INDEX    | Email address (used as identifier) |
| `phone`          | VARCHAR(50)   | NULLABLE                   | Phone number                       |
| `location`       | VARCHAR(255)  | NULLABLE                   | City/Country                       |
| `linkedin`       | VARCHAR(500)  | NULLABLE                   | LinkedIn profile URL               |
| `summary`        | TEXT          | NULLABLE                   | Professional summary               |
| `photo_filename` | VARCHAR(255)  | NULLABLE                   | Uploaded photo filename            |
| `template`       | VARCHAR(50)   | DEFAULT 'modern'           | Resume template name               |
| `education`      | JSON          | NULLABLE                   | Array of education entries         |
| `experience`     | JSON          | NULLABLE                   | Array of experience entries        |
| `skills`         | JSON          | NULLABLE                   | Array of skill strings             |
| `projects`       | JSON          | NULLABLE                   | Array of project entries           |
| `created_at`     | DATETIME      | DEFAULT NOW()              | Record creation timestamp          |
| `updated_at`     | DATETIME      | DEFAULT NOW(), ON UPDATE   | Last update timestamp              |

### Why JSON Columns?

Education, experience, skills, and projects are stored as JSON arrays. This keeps the schema simple (single table) while allowing flexible, nested data. MySQL 8.0+ has native JSON support with indexing capabilities.

**Example `education` JSON:**
```json
[
  {
    "degree": "B.Sc Computer Science",
    "institution": "MIT",
    "location": "Cambridge, MA",
    "duration": "2020 - 2024",
    "description": "GPA: 3.8/4.0"
  }
]
```

---

## Configuration

All database settings live in `config.py`:

```python
class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'resume_builder')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

The connection string format is: `mysql+pymysql://user:password@host:port/database`

---

## API Endpoints

### List Candidates

```
GET /api/candidates
```

**Query Parameters:**

| Parameter    | Type   | Default      | Description                              |
|-------------|--------|--------------|------------------------------------------|
| `search`    | string | (empty)      | Search across name, email, phone, location |
| `sort_by`   | string | `created_at` | Column to sort by                        |
| `sort_order`| string | `desc`       | `asc` or `desc`                          |
| `skill`     | string | (empty)      | Filter by skill name                     |
| `location`  | string | (empty)      | Filter by location                       |
| `page`      | int    | 1            | Page number                              |
| `per_page`  | int    | 20           | Results per page                         |

**Response:**
```json
{
  "candidates": [...],
  "total": 42,
  "pages": 3,
  "current_page": 1,
  "per_page": 20
}
```

### Create Candidate

```
POST /api/candidates
Content-Type: application/json
```

**Body:**
```json
{
  "data": {
    "personal": {
      "fullName": "John Doe",
      "email": "john@example.com",
      "phone": "+1 234 567 8900",
      "location": "New York, USA",
      "linkedin": "linkedin.com/in/johndoe",
      "summary": "Experienced developer...",
      "photo_filename": "abc123.jpg"
    },
    "education": [...],
    "experience": [...],
    "skills": ["Python", "JavaScript"],
    "projects": [...]
  },
  "template": "modern"
}
```

**Response (201):**
```json
{
  "success": true,
  "candidate": { ... }
}
```

### Get Single Candidate

```
GET /api/candidates/<id>
```

### Update Candidate

```
PUT /api/candidates/<id>
Content-Type: application/json
```

Same body format as Create.

### Delete Candidate

```
DELETE /api/candidates/<id>
```

### Candidate Statistics

```
GET /api/candidates/stats
```

**Response:**
```json
{
  "total_candidates": 42,
  "locations": [
    {"location": "New York", "count": 15},
    {"location": "San Francisco", "count": 8}
  ]
}
```

---

## Searching & Sorting

### Search

The search feature uses `ILIKE` (case-insensitive) matching across multiple columns simultaneously:

```python
query = query.filter(
    db.or_(
        Candidate.full_name.ilike(f"%{search}%"),
        Candidate.email.ilike(f"%{search}%"),
        Candidate.phone.ilike(f"%{search}%"),
        Candidate.location.ilike(f"%{search}%")
    )
)
```

### Sort

Sortable columns: `full_name`, `email`, `location`, `created_at`, `updated_at`

### Filter by Skill

Skills are stored as JSON arrays. The filter uses a `LIKE` query on the JSON column:

```python
query = query.filter(Candidate.skills.like(f'%"{skill_filter}"%'))
```

### Pagination

Server-side pagination using Flask-SQLAlchemy's `paginate()`:

```python
pagination = query.paginate(page=page, per_page=per_page, error_out=False)
```

---

## How It Works

### Model (`models.py`)

The `Candidate` model maps to the `candidates` MySQL table using SQLAlchemy ORM:

```python
class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    # ... more columns
    education = db.Column(db.JSON, nullable=True)
```

The `to_dict()` method converts a model instance to a JSON-serializable dictionary for API responses.

### Database Initialization

On app startup (`app.py`):

```python
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates tables if they don't exist
```

### Save from Frontend

When the user clicks "Save to Database" on the builder page:

1. Frontend collects all form data into `resumeData` object
2. Sends `POST /api/candidates` (or `PUT` if editing)
3. Backend validates required fields (name, email)
4. Creates/updates the `Candidate` record
5. Returns the saved candidate data

---

## Common Operations

### Backup the Database

```bash
mysqldump -u root -p resume_builder > backup.sql
```

### Restore from Backup

```bash
mysql -u root -p resume_builder < backup.sql
```

### Reset the Database

```bash
mysql -u root -p -e "DROP DATABASE resume_builder;"
python init_db.py
```

### View All Candidates (MySQL CLI)

```sql
USE resume_builder;
SELECT id, full_name, email, location, created_at FROM candidates ORDER BY created_at DESC;
```

---

## Troubleshooting

### "Access denied for user 'root'@'localhost'"

Update `config.py` with the correct MySQL password, or set the environment variable:

```bash
set MYSQL_PASSWORD=your_actual_password
```

### "Can't connect to MySQL server"

Ensure MySQL is running:

```bash
# Windows
net start mysql

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

### "Unknown database 'resume_builder'"

Run the initialization script:

```bash
python init_db.py
```

### "Table 'candidates' doesn't exist"

The app auto-creates tables on startup. If it fails, run:

```bash
python init_db.py
```

### Database shows "disconnected" in /health

Check that:
1. MySQL server is running
2. Credentials in `config.py` are correct
3. The `resume_builder` database exists
4. PyMySQL is installed: `pip install PyMySQL`
