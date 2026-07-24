# 08 - New Features Guide

This document covers the three major features added to the Resume Builder application:

1. **Passport Size Photo** — Upload and embed a photo in the resume
2. **Additional Themes/Templates** — 6 total resume templates
3. **Candidate Database** — MySQL-backed candidate management with search, sort, and filter

---

## Table of Contents

1. [Passport Size Photo](#1-passport-size-photo)
2. [Resume Templates & Themes](#2-resume-templates--themes)
3. [Candidate Database Management](#3-candidate-database-management)
4. [Architecture Overview](#4-architecture-overview)
5. [File Changes Summary](#5-file-changes-summary)

---

## 1. Passport Size Photo

### Overview

Users can upload a passport-size photo (PNG or JPG, max 5MB) that appears:
- In the **live preview** (top-right corner next to the name)
- In the **generated PDF** (top-right, 1.2" × 1.5" passport size)
- In the **candidates database** table and detail modal

### How to Use

1. In the **Personal Details** section of the builder, find the "Passport Size Photo" area
2. Click the dashed box or the **Upload Photo** button
3. Select a PNG or JPG image (max 5MB)
4. The photo appears immediately in the preview
5. Click **Remove** to delete the photo
6. Drag-and-drop is also supported

### Technical Details

**Frontend (`app.js`):**
- `setupPhotoUpload()` — Initializes click, change, and drag-and-drop listeners
- `uploadPhoto(file)` — Validates file type/size, sends to server via `FormData`
- `showPhotoPreview(url)` — Displays the uploaded photo in both the form and live preview
- `removePhoto()` — Clears the photo from state and UI
- Photo filename is stored in `resumeData.personal.photo_filename`

**Backend (`app.py`):**
- `POST /upload-photo` — Receives the file, validates extension, resizes to max 600×800px, saves with a UUID filename to `uploads/photos/`
- `GET /uploads/photos/<filename>` — Serves uploaded photos
- `get_photo_for_pdf()` — Loads the photo as a ReportLab `Image` object (1.2" × 1.5")
- `build_personal_section()` — If a photo exists, creates a two-column `Table` layout with personal info on the left and the photo on the right

**Storage:**
- Photos are saved to `uploads/photos/` directory
- Filenames are UUID-based to prevent collisions (e.g., `a1b2c3d4.jpg`)
- Images are auto-resized to max 600×800px and converted to RGB JPEG

**PDF Layout with Photo:**
```
┌─────────────────────────────────────────────┐
│  John Doe                        ┌────────┐ │
│  john@email.com | +1234567890    │ PHOTO  │ │
│  LinkedIn: linkedin.com/in/john  │ 1.2x1.5│ │
│                                  └────────┘ │
│  Professional summary text here...          │
├─────────────────────────────────────────────┤
│  EDUCATION                                  │
│  ...                                        │
└─────────────────────────────────────────────┘
```

---

## 2. Resume Templates & Themes

### Available Templates

The application now offers **6 resume templates**:

| Template       | Font Family    | Accent Color | Alignment | Style Description                    |
|---------------|----------------|--------------|-----------|--------------------------------------|
| **Modern**     | Helvetica      | `#2563eb`    | Center    | Clean blue accents, modern sans-serif|
| **Classic**    | Times          | Black        | Center    | Traditional serif, formal look       |
| **Minimal**    | Helvetica      | `#1e293b`    | Left      | Compact, minimal spacing             |
| **Executive**  | Times          | `#1a1a2e`    | Center    | Premium serif, deep navy tones       |
| **Creative**   | Helvetica      | `#e74c3c`    | Left      | Bold red accents, large name         |
| **Professional**| Helvetica     | `#0f4c75`    | Center    | Corporate blue, balanced layout      |

### How to Use

1. In the **Live Preview** panel, use the template dropdown selector
2. The preview updates instantly to show the selected theme
3. The selected template is used when generating the PDF
4. The template choice is saved with the candidate in the database

### Technical Details

**Backend — Style Functions (`app.py`):**

Each template has a dedicated style function:
- `get_modern_styles()` — Blue accent, Helvetica, centered
- `get_classic_styles()` — Black, Times, centered
- `get_minimal_styles()` — Dark slate, Helvetica, left-aligned
- `get_executive_styles()` — Deep navy, Times, serif, formal
- `get_creative_styles()` — Red accent, Helvetica, left-aligned, large name
- `get_professional_styles()` — Corporate blue, Helvetica, centered

Template selection in `create_resume_pdf()`:
```python
template_map = {
    'modern': get_modern_styles,
    'classic': get_classic_styles,
    'minimal': get_minimal_styles,
    'executive': get_executive_styles,
    'creative': get_creative_styles,
    'professional': get_professional_styles,
}
style_fn = template_map.get(template, get_modern_styles)
styles = style_fn(styles)
```

**Frontend — Live Preview Themes (`style.css`):**

Each template has CSS overrides for the live preview:
```css
.template-executive .preview-personal h1 { color: #1a1a2e; font-family: Georgia, serif; }
.template-creative .preview-personal h1 { color: #e74c3c; font-size: 2.2rem; }
.template-professional .section-title { color: #0f4c75; }
```

Template switching in `app.js`:
```javascript
function changeTemplate() {
  currentTemplate = document.getElementById("templateSelector").value;
  const preview = document.getElementById("resumePreview");
  preview.classList.remove("template-modern", "template-classic", ...);
  preview.classList.add(`template-${currentTemplate}`);
}
```

---

## 3. Candidate Database Management

### Overview

The candidate database allows you to:
- **Save** resume data from the builder to MySQL
- **Browse** all candidates in a searchable, sortable table
- **Search** by name, email, phone, or location
- **Filter** by location or specific skill
- **Sort** by name, email, location, date added, or last updated
- **View** full candidate details in a modal popup
- **Edit** a candidate by loading their data back into the builder
- **Delete** candidates from the database

### How to Use

#### Saving a Candidate
1. Fill out the resume form on the builder page
2. Click **💾 Save to Database**
3. If the email already exists, you'll be prompted to update the existing record

#### Managing Candidates
1. Click **Candidates Database** in the navigation bar
2. Use the search bar to find candidates by name, email, phone, or location
3. Use the filter dropdowns to narrow results by location or skill
4. Click on any row to view full details
5. Click **Edit in Builder** to load a candidate's data into the form
6. Click **Delete** to remove a candidate

#### Sorting
- **Date Added** — When the candidate was first saved (default)
- **Name** — Alphabetical by full name
- **Email** — Alphabetical by email
- **Location** — Alphabetical by location
- **Last Updated** — Most recently modified

### Technical Details

**Pages:**
- `/` — Resume builder (existing, enhanced with Save to DB button)
- `/candidates` — Candidate database management page

**API Endpoints:**

| Method | Endpoint                    | Description                      |
|--------|-----------------------------|----------------------------------|
| GET    | `/api/candidates`           | List with search/sort/filter     |
| POST   | `/api/candidates`           | Create new candidate             |
| GET    | `/api/candidates/<id>`      | Get single candidate             |
| PUT    | `/api/candidates/<id>`      | Update candidate                 |
| DELETE | `/api/candidates/<id>`      | Delete candidate                 |
| GET    | `/api/candidates/stats`     | Get statistics                   |

**Frontend Files:**
- `templates/candidates.html` — Database management page with table, filters, modal
- `static/js/candidates.js` — All candidate page logic (CRUD, search, pagination)

**Key Frontend Functions (`candidates.js`):**
- `loadCandidates(page)` — Fetches candidates with current filters
- `renderCandidates(candidates)` — Builds the HTML table rows
- `renderPagination(total, pages, current)` — Builds page navigation
- `searchCandidates()` — Triggers search with current input
- `viewCandidate(id)` — Opens the detail modal
- `editCandidate()` — Saves candidate data to localStorage and redirects to builder
- `deleteCandidate(id, name)` — Deletes with confirmation

**Edit Flow:**
1. User clicks "Edit in Builder" in the candidate modal
2. Candidate data is fetched and stored in `localStorage` as `resumeData`
3. The `editingCandidateId` is also stored
4. User is redirected to `/` (builder page)
5. Builder loads the data from localStorage and populates all fields
6. When user clicks "Save to Database", it sends a `PUT` request (update) instead of `POST` (create)

---

## 4. Architecture Overview

### Updated Project Structure

```
resume-builder/
├── app.py                     # Flask app with all routes & PDF generation
├── config.py                  # Database & app configuration
├── models.py                  # SQLAlchemy Candidate model
├── init_db.py                 # Database initialization script
├── requirements.txt           # Python dependencies
├── uploads/                   # Uploaded files
│   └── photos/                # Passport photos
├── generated_pdfs/            # Generated PDF files
├── static/
│   ├── css/
│   │   └── style.css          # All styles (builder + candidates + themes)
│   └── js/
│       ├── app.js             # Builder page logic + photo upload
│       └── candidates.js      # Candidates database page logic
├── templates/
│   ├── index.html             # Builder page
│   └── candidates.html        # Candidates database page
├── docs/
│   ├── 01-SETUP-GUIDE.md
│   ├── 02-ARCHITECTURE.md
│   ├── 03-BUILDING-FRONTEND.md
│   ├── 04-BUILDING-BACKEND.md
│   ├── 05-FEATURES-GUIDE.md
│   ├── 06-TROUBLESHOOTING.md
│   ├── 07-DATABASE-GUIDE.md   # MySQL setup & API reference
│   └── 08-NEW-FEATURES-GUIDE.md  # This file
└── README.md
```

### Data Flow

```
┌──────────────┐     POST /upload-photo     ┌──────────────┐
│   Browser    │ ──────────────────────────> │  Flask App   │
│  (index.html)│                             │  (app.py)    │
│              │     POST /api/candidates    │              │
│              │ ──────────────────────────> │              │
│              │                             │   ┌────────┐ │
│              │     GET /api/candidates     │   │ MySQL  │ │
│ (candidates  │ ──────────────────────────> │   │  DB    │ │
│   .html)     │ <────────────────────────── │   └────────┘ │
│              │     JSON response           │              │
│              │                             │   ┌────────┐ │
│              │     POST /generate-pdf      │   │uploads/│ │
│              │ ──────────────────────────> │   │photos/ │ │
│              │ <────────────────────────── │   └────────┘ │
│              │     PDF file                │              │
└──────────────┘                             └──────────────┘
```

### Technology Stack

| Layer      | Technology                                    |
|-----------|-----------------------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JavaScript (ES6+)        |
| Backend   | Python 3.8+, Flask 3.0                        |
| Database  | MySQL 8.0+ via Flask-SQLAlchemy + PyMySQL      |
| PDF       | ReportLab 4.0                                 |
| Images    | Pillow (PIL) for photo processing              |

---

## 5. File Changes Summary

### New Files

| File                          | Purpose                                    |
|-------------------------------|--------------------------------------------|
| `config.py`                   | Centralized configuration (DB, uploads)    |
| `models.py`                   | SQLAlchemy Candidate model                 |
| `init_db.py`                  | Database creation script                   |
| `templates/candidates.html`   | Candidates database management page        |
| `static/js/candidates.js`     | Candidates page JavaScript                 |
| `docs/07-DATABASE-GUIDE.md`   | MySQL setup & API documentation            |
| `docs/08-NEW-FEATURES-GUIDE.md` | This features guide                     |

### Modified Files

| File                    | Changes                                                     |
|------------------------|-------------------------------------------------------------|
| `app.py`               | Added MySQL init, photo upload, CRUD APIs, new templates, photo in PDF |
| `requirements.txt`     | Added Flask-SQLAlchemy, PyMySQL, Werkzeug                   |
| `templates/index.html` | Added navbar, photo upload UI, new template options, save-to-DB button |
| `static/js/app.js`     | Added photo upload/preview, save-to-database, edit candidate flow |
| `static/css/style.css` | Added navbar, photo, candidates table, modal, template theme styles |
| `README.md`            | Updated with new features, setup instructions, structure    |
