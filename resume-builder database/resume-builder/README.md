# Resume Builder App 📄

A modern, full-stack resume builder web application with **MySQL database**, **passport photo support**, **6 resume templates**, and a **candidate management system** with search, sort, and filter capabilities.

## 🎯 Project Overview

This is an **intermediate-level** project suitable for 3rd-year college students. It combines frontend technologies (HTML, CSS, JavaScript) with a Python Flask backend and MySQL database to create a full-stack web application.

### Key Features

- ✨ Real-time resume preview
- 📝 Dynamic form sections (Education, Experience, Skills, Projects)
- 🎨 **6 resume templates** (Modern, Classic, Minimal, Executive, Creative, Professional)
- 📸 **Passport size photo upload** with drag-and-drop support
- 📥 PDF export with embedded photo
- 🗄️ **MySQL database** for candidate storage
- 🔍 **Search, sort, and filter** candidates by name, email, location, skill
- 👥 **Candidate management page** with table view, detail modal, edit & delete
- 💾 Local storage for auto-save + database persistence
- 📱 Responsive design
- 🎯 Clean and modern UI with navigation

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask 3.0
- **Database**: MySQL 8.0+ via Flask-SQLAlchemy + PyMySQL
- **PDF Generation**: ReportLab 4.0
- **Image Processing**: Pillow (PIL)
- **Storage**: Browser LocalStorage + MySQL + File System

## 📁 Project Structure

```
resume-builder/
├── app.py                     # Flask application (routes, APIs, PDF generation)
├── config.py                  # Database & app configuration
├── models.py                  # SQLAlchemy Candidate model
├── init_db.py                 # Database initialization script
├── requirements.txt           # Python dependencies
├── uploads/                   # Uploaded files (auto-created)
│   └── photos/                # Passport photos
├── generated_pdfs/            # Generated PDF files
├── static/                    # Static files
│   ├── css/
│   │   └── style.css          # All styles (builder + candidates + themes)
│   └── js/
│       ├── app.js             # Builder page logic + photo upload
│       └── candidates.js      # Candidates database page logic
├── templates/                 # HTML templates
│   ├── index.html             # Resume builder page
│   └── candidates.html        # Candidates database page
├── docs/                      # Documentation files
│   ├── 01-SETUP-GUIDE.md
│   ├── 02-ARCHITECTURE.md
│   ├── 03-BUILDING-FRONTEND.md
│   ├── 04-BUILDING-BACKEND.md
│   ├── 05-FEATURES-GUIDE.md
│   ├── 06-TROUBLESHOOTING.md
│   ├── 07-DATABASE-GUIDE.md   # MySQL setup & API reference
│   └── 08-NEW-FEATURES-GUIDE.md # Photo, templates, DB features
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- **MySQL Server 8.0+** installed and running
- Modern web browser (Chrome, Firefox, Edge)
- Text editor or IDE (VS Code recommended)

### Installation

1. **Clone or download the project**

   ```bash
   cd resume-builder
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL credentials**

   Edit `config.py` and set your MySQL password:

   ```python
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'your_password_here'
   ```

   Or use environment variables:

   ```bash
   set MYSQL_PASSWORD=your_password_here
   ```

4. **Initialize the database**

   ```bash
   python init_db.py
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Open in browser**
   - Resume Builder: `http://localhost:5000`
   - Candidates Database: `http://localhost:5000/candidates`
   - Health Check: `http://localhost:5000/health`

## 📚 Documentation Guide

This project includes comprehensive documentation to help you build and understand the application:

1. **[Setup Guide](docs/01-SETUP-GUIDE.md)** - Environment setup and installation
2. **[Architecture](docs/02-ARCHITECTURE.md)** - System design and component overview
3. **[Building Frontend](docs/03-BUILDING-FRONTEND.md)** - Step-by-step HTML, CSS, JS implementation
4. **[Building Backend](docs/04-BUILDING-BACKEND.md)** - Flask server and PDF generation
5. **[Features Guide](docs/05-FEATURES-GUIDE.md)** - Detailed feature explanations
6. **[Troubleshooting](docs/06-TROUBLESHOOTING.md)** - Common issues and solutions
7. **[Database Guide](docs/07-DATABASE-GUIDE.md)** - MySQL setup, schema, API reference
8. **[New Features Guide](docs/08-NEW-FEATURES-GUIDE.md)** - Photo upload, templates, candidate DB

## 🔌 API Reference

| Method | Endpoint                 | Description                   |
| ------ | ------------------------ | ----------------------------- |
| GET    | `/`                      | Resume builder page           |
| GET    | `/candidates`            | Candidates database page      |
| POST   | `/upload-photo`          | Upload passport photo         |
| GET    | `/uploads/photos/<file>` | Serve uploaded photo          |
| POST   | `/generate-pdf`          | Generate resume PDF           |
| GET    | `/api/candidates`        | List candidates (search/sort) |
| POST   | `/api/candidates`        | Create new candidate          |
| GET    | `/api/candidates/<id>`   | Get single candidate          |
| PUT    | `/api/candidates/<id>`   | Update candidate              |
| DELETE | `/api/candidates/<id>`   | Delete candidate              |
| GET    | `/api/candidates/stats`  | Get statistics                |
| GET    | `/health`                | Server & DB health check      |

## 🎓 Learning Objectives

By building this project, you will learn:

- Frontend development with vanilla JavaScript
- DOM manipulation and event handling
- CSS Grid and Flexbox layouts
- RESTful API design with CRUD operations
- Flask web framework
- **MySQL database design and ORM (SQLAlchemy)**
- **File upload handling and image processing**
- PDF generation in Python with embedded images
- Client-server communication
- Local storage management
- Responsive web design
- **Search, sort, and pagination patterns**

## 🤝 Contributing

This is an educational project. Feel free to:

- Add new resume templates
- Improve the UI/UX
- Add new features (e.g., export to Word, email functionality)
- Optimize the code

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Built as an intermediate-level college project to demonstrate full-stack web development skills.

---

**Ready to start building?** Head over to [Setup Guide](docs/01-SETUP-GUIDE.md) to begin! 🚀
