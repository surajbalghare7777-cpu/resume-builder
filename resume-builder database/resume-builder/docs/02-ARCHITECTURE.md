# Architecture Guide 🏗️

This document explains the system architecture, design patterns, and how different components work together in the Resume Builder application.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Technology Choices](#technology-choices)

---

## System Overview

The Resume Builder is a **client-server web application** with the following characteristics:

- **Architecture Type**: MVC (Model-View-Controller) pattern
- **Communication**: RESTful API
- **Data Persistence**: Browser LocalStorage + Server-side PDF generation
- **Rendering**: Client-side (JavaScript) + Server-side (Python)

### High-Level Components

```
┌─────────────────────────────────────────────────────┐
│                   USER BROWSER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │     HTML     │  │     CSS      │  │JavaScript │ │
│  │  (Structure) │  │   (Styling)  │  │  (Logic)  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                  │                │        │
│         └──────────────────┴────────────────┘        │
│                          │                           │
└──────────────────────────┼───────────────────────────┘
                           │ HTTP/AJAX
                           ▼
┌─────────────────────────────────────────────────────┐
│                  FLASK SERVER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Routes     │  │  Templates   │  │    PDF    │ │
│  │  (app.py)    │  │  (Jinja2)    │  │ Generator │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Architecture Diagram

### Detailed Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              index.html (View)                       │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │    │
│  │  │ Input Form   │  │   Preview    │  │ Controls │  │    │
│  │  │   Section    │  │   Section    │  │  Panel   │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              style.css (Presentation)                │    │
│  │  • Layout (Grid/Flexbox)                            │    │
│  │  • Responsive Design                                │    │
│  │  • Theme & Colors                                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              app.js (Controller)                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │    │
│  │  │ Form Handler │  │  Preview     │  │  Storage │  │    │
│  │  │              │  │  Updater     │  │  Manager │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │    │
│  │  ┌──────────────┐  ┌──────────────┐                │    │
│  │  │ PDF Export   │  │  Template    │                │    │
│  │  │   Handler    │  │  Switcher    │                │    │
│  │  └──────────────┘  └──────────────┘                │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                    HTTP POST/GET
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                        BACKEND LAYER                          │
├────────────────────────────┼─────────────────────────────────┤
│                            ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              app.py (Flask Application)              │    │
│  │                                                       │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         Route Handlers                       │    │    │
│  │  │  • GET  /           → Serve HTML            │    │    │
│  │  │  • POST /generate   → Generate PDF          │    │    │
│  │  │  • GET  /download   → Download PDF          │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                        │                             │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         PDF Generator Module                 │    │    │
│  │  │  • ReportLab integration                    │    │    │
│  │  │  • Template rendering                       │    │    │
│  │  │  • Styling & formatting                     │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                        │                             │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         Template Engine (Jinja2)            │    │    │
│  │  │  • HTML rendering                           │    │    │
│  │  │  • Dynamic content injection                │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Components

#### A. HTML (index.html)

**Purpose**: Structure and content organization

**Key Sections**:

- **Header**: App title and navigation
- **Form Section**: User input fields
  - Personal Information
  - Education (dynamic entries)
  - Experience (dynamic entries)
  - Skills (dynamic tags)
  - Projects (dynamic entries)
- **Preview Section**: Live resume preview
- **Control Panel**: Export, save, template selection

**Responsibilities**:

- Define semantic structure
- Provide form inputs
- Display preview area
- Include necessary scripts and styles

#### B. CSS (style.css)

**Purpose**: Visual presentation and layout

**Key Features**:

- **Layout System**: CSS Grid for main layout, Flexbox for components
- **Responsive Design**: Media queries for mobile/tablet/desktop
- **Theme Variables**: CSS custom properties for colors and spacing
- **Animations**: Smooth transitions and hover effects

**Responsibilities**:

- Visual styling
- Responsive behavior
- User experience enhancements
- Print-friendly styles

#### C. JavaScript (app.js)

**Purpose**: Application logic and interactivity

**Key Modules**:

1. **State Management**

   ```javascript
   const resumeData = {
     personal: {},
     education: [],
     experience: [],
     skills: [],
     projects: [],
   };
   ```

2. **Event Handlers**
   - Form input listeners
   - Add/remove section buttons
   - Template switcher
   - Export button

3. **Preview Updater**
   - Real-time DOM manipulation
   - Template rendering
   - Data formatting

4. **Storage Manager**
   - LocalStorage save/load
   - Auto-save functionality
   - Data serialization

5. **API Communication**
   - AJAX requests to Flask
   - PDF generation trigger
   - Error handling

**Responsibilities**:

- Handle user interactions
- Update preview in real-time
- Manage application state
- Communicate with backend
- Persist data locally

---

### 2. Backend Components

#### A. Flask Application (app.py)

**Purpose**: Server-side logic and API endpoints

**Route Structure**:

```python
@app.route('/')
def index():
    # Serve main HTML page
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Receive resume data
    # Generate PDF using ReportLab
    # Return PDF file or download link

@app.route('/download/<filename>')
def download_file(filename):
    # Serve generated PDF file
```

**Responsibilities**:

- Route handling
- Request/response processing
- PDF generation orchestration
- File serving
- Error handling

#### B. PDF Generator Module

**Purpose**: Convert resume data to PDF format

**Process Flow**:

1. Receive JSON data from frontend
2. Parse and validate data
3. Apply selected template
4. Generate PDF using ReportLab
5. Save to temporary location
6. Return file path or stream

**Key Functions**:

```python
def create_pdf(data, template='modern'):
    # Initialize PDF canvas
    # Apply template styling
    # Render sections
    # Save and return
```

**Responsibilities**:

- PDF document creation
- Template application
- Formatting and styling
- File management

---

## Data Flow

### 1. Initial Page Load

```
User → Browser → GET / → Flask Server
                          ↓
                    Render index.html
                          ↓
                    Load CSS & JS
                          ↓
                    Check LocalStorage
                          ↓
                    Populate Form (if data exists)
                          ↓
                    Display to User
```

### 2. Form Input & Preview Update

```
User Types → Input Event → JavaScript Handler
                              ↓
                         Update State
                              ↓
                         Update Preview DOM
                              ↓
                         Save to LocalStorage
                              ↓
                         Display Updated Preview
```

### 3. PDF Generation & Download

```
User Clicks Export → JavaScript
                        ↓
                   Collect Form Data
                        ↓
                   Validate Data
                        ↓
                   POST /generate-pdf → Flask Server
                                           ↓
                                      Receive JSON
                                           ↓
                                      Generate PDF
                                           ↓
                                      Save File
                                           ↓
                                      Return Response
                        ↓
                   Receive Response
                        ↓
                   Trigger Download
                        ↓
                   User Gets PDF
```

---

## Design Patterns

### 1. MVC Pattern

- **Model**: Resume data structure (JavaScript object)
- **View**: HTML templates and preview section
- **Controller**: JavaScript event handlers and Flask routes

### 2. Observer Pattern

- Form inputs observe user actions
- Preview section observes data changes
- LocalStorage observes state updates

### 3. Module Pattern

JavaScript code organized into modules:

- Form handling module
- Preview rendering module
- Storage module
- API communication module

### 4. Template Pattern

Multiple resume templates with consistent interface:

```javascript
const templates = {
  modern: renderModernTemplate,
  classic: renderClassicTemplate,
  minimal: renderMinimalTemplate,
};
```

---

## Technology Choices

### Why Flask?

✅ **Pros**:

- Lightweight and easy to learn
- Perfect for small to medium projects
- Excellent documentation
- Built-in development server
- Jinja2 templating

❌ **Alternatives Considered**:

- Django (too heavy for this project)
- FastAPI (requires async knowledge)
- Node.js/Express (wanted to use Python)

### Why ReportLab?

✅ **Pros**:

- Powerful PDF generation
- Fine-grained control
- Pure Python
- Good documentation

❌ **Alternatives Considered**:

- WeasyPrint (HTML to PDF, less control)
- PyPDF2 (more for manipulation)
- Puppeteer (requires Node.js)

### Why Vanilla JavaScript?

✅ **Pros**:

- No build tools needed
- Learn fundamentals
- Lightweight
- No dependencies

❌ **Alternatives Considered**:

- React (overkill for this project)
- Vue.js (adds complexity)
- jQuery (outdated)

### Why LocalStorage?

✅ **Pros**:

- Simple API
- No server needed
- Instant save/load
- Good for client-side data

❌ **Alternatives Considered**:

- Database (adds complexity)
- Cookies (size limitations)
- IndexedDB (too complex)

---

## Security Considerations

### Input Validation

- Sanitize user input on both client and server
- Validate data types and formats
- Prevent XSS attacks

### File Handling

- Use secure file paths
- Limit file sizes
- Clean up temporary files
- Validate file types

### CORS Configuration

- Configure Flask-CORS properly
- Limit allowed origins in production

---

## Scalability Considerations

### Current Limitations

- LocalStorage has 5-10MB limit
- Single-server architecture
- No user authentication
- No database persistence

### Future Enhancements

- Add user authentication
- Database integration (PostgreSQL/MongoDB)
- Cloud storage for PDFs
- Multiple resume management
- Collaborative editing
- Email functionality

---

## Performance Optimization

### Frontend

- Debounce input events
- Lazy load preview updates
- Minimize DOM manipulations
- Use CSS transforms for animations

### Backend

- Cache PDF templates
- Async PDF generation
- Compress responses
- Use CDN for static files

---

## Next Steps

Now that you understand the architecture, proceed to:

- **[Building Frontend](03-BUILDING-FRONTEND.md)** - Implement HTML, CSS, and JavaScript
- **[Building Backend](04-BUILDING-BACKEND.md)** - Implement Flask server and PDF generation

---

**Questions?** Review this document or check the [Troubleshooting Guide](06-TROUBLESHOOTING.md).
