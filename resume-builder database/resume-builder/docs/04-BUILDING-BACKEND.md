# Building the Backend 🐍

This guide walks you through building the Flask backend server and implementing PDF generation functionality.

## Table of Contents

1. [Flask Application Setup](#flask-application-setup)
2. [PDF Generation with ReportLab](#pdf-generation-with-reportlab)
3. [API Endpoints](#api-endpoints)
4. [Testing the Backend](#testing-the-backend)

---

## Flask Application Setup

### Step 1: Create app.py

Create `app.py` in the project root:

```python
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = 'generated_pdfs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ===== ROUTES =====

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF from resume data"""
    try:
        data = request.json
        resume_data = data.get('data', {})
        template = data.get('template', 'modern')

        # Generate PDF
        pdf_buffer = create_resume_pdf(resume_data, template)

        # Return PDF as downloadable file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})

# ===== PDF GENERATION =====

def create_resume_pdf(data, template='modern'):
    """
    Create a PDF resume from the provided data

    Args:
        data (dict): Resume data containing personal, education, experience, etc.
        template (str): Template style ('modern', 'classic', 'minimal')

    Returns:
        BytesIO: PDF file buffer
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for PDF elements
    story = []

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles based on template
    if template == 'modern':
        styles = get_modern_styles(styles)
    elif template == 'classic':
        styles = get_classic_styles(styles)
    else:  # minimal
        styles = get_minimal_styles(styles)

    # Build PDF sections
    story.extend(build_personal_section(data.get('personal', {}), styles))
    story.extend(build_education_section(data.get('education', []), styles))
    story.extend(build_experience_section(data.get('experience', []), styles))
    story.extend(build_skills_section(data.get('skills', []), styles))
    story.extend(build_projects_section(data.get('projects', []), styles))

    # Build PDF
    doc.build(story)
    buffer.seek(0)

    return buffer

# ===== STYLE DEFINITIONS =====

def get_modern_styles(base_styles):
    """Modern template styles"""
    styles = base_styles

    # Name style
    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Contact style
    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    # Summary style
    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_JUSTIFY,
        spaceAfter=16,
        leading=14
    ))

    # Section heading
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#e2e8f0'),
        borderPadding=4
    ))

    # Item title
    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    ))

    # Item meta
    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=6
    ))

    # Item description
    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=13
    ))

    return styles

def get_classic_styles(base_styles):
    """Classic template styles"""
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.black,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Times-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=16,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.black,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Times-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        fontName='Times-Bold',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        fontName='Times-Italic'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Times-Roman'
    ))

    return styles

def get_minimal_styles(base_styles):
    """Minimal template styles"""
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_LEFT,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT,
        spaceAfter=14
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceAfter=3
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#475569'),
        alignment=TA_LEFT,
        spaceAfter=10
    ))

    return styles

# ===== SECTION BUILDERS =====

def build_personal_section(personal, styles):
    """Build personal information section"""
    story = []

    # Name
    if personal.get('fullName'):
        story.append(Paragraph(personal['fullName'], styles['CustomName']))

    # Contact info
    contact_parts = []
    if personal.get('email'):
        contact_parts.append(personal['email'])
    if personal.get('phone'):
        contact_parts.append(personal['phone'])
    if personal.get('location'):
        contact_parts.append(personal['location'])

    if contact_parts:
        contact_text = ' • '.join(contact_parts)
        story.append(Paragraph(contact_text, styles['CustomContact']))

    # LinkedIn
    if personal.get('linkedin'):
        story.append(Paragraph(f"LinkedIn: {personal['linkedin']}", styles['CustomContact']))

    # Summary
    if personal.get('summary'):
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(personal['summary'], styles['CustomSummary']))

    story.append(Spacer(1, 0.15*inch))

    return story

def build_education_section(education, styles):
    """Build education section"""
    story = []

    # Filter out empty entries
    education = [e for e in education if e.get('degree') or e.get('institution')]

    if not education:
        return story

    # Section heading
    story.append(Paragraph('EDUCATION', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for edu in education:
        # Degree
        if edu.get('degree'):
            story.append(Paragraph(edu['degree'], styles['CustomItemTitle']))

        # Institution, location, duration
        meta_parts = []
        if edu.get('institution'):
            meta_parts.append(edu['institution'])
        if edu.get('location'):
            meta_parts.append(edu['location'])
        if edu.get('duration'):
            meta_parts.append(edu['duration'])

        if meta_parts:
            meta_text = ' • '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        # Description
        if edu.get('description'):
            story.append(Paragraph(edu['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

def build_experience_section(experience, styles):
    """Build work experience section"""
    story = []

    # Filter out empty entries
    experience = [e for e in experience if e.get('title') or e.get('company')]

    if not experience:
        return story

    # Section heading
    story.append(Paragraph('EXPERIENCE', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for exp in experience:
        # Job title
        if exp.get('title'):
            story.append(Paragraph(exp['title'], styles['CustomItemTitle']))

        # Company, location, duration
        meta_parts = []
        if exp.get('company'):
            meta_parts.append(exp['company'])
        if exp.get('location'):
            meta_parts.append(exp['location'])
        if exp.get('duration'):
            meta_parts.append(exp['duration'])

        if meta_parts:
            meta_text = ' • '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        # Description
        if exp.get('description'):
            story.append(Paragraph(exp['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

def build_skills_section(skills, styles):
    """Build skills section"""
    story = []

    if not skills:
        return story

    # Section heading
    story.append(Paragraph('SKILLS', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    # Skills as comma-separated list
    skills_text = ' • '.join(skills)
    story.append(Paragraph(skills_text, styles['CustomItemDesc']))
    story.append(Spacer(1, 0.1*inch))

    return story

def build_projects_section(projects, styles):
    """Build projects section"""
    story = []

    # Filter out empty entries
    projects = [p for p in projects if p.get('name')]

    if not projects:
        return story

    # Section heading
    story.append(Paragraph('PROJECTS', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for proj in projects:
        # Project name
        project_title = proj['name']
        if proj.get('link'):
            project_title += f" ({proj['link']})"
        story.append(Paragraph(project_title, styles['CustomItemTitle']))

        # Technologies and duration
        meta_parts = []
        if proj.get('technologies'):
            meta_parts.append(f"Technologies: {proj['technologies']}")
        if proj.get('duration'):
            meta_parts.append(proj['duration'])

        if meta_parts:
            meta_text = ' • '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        # Description
        if proj.get('description'):
            story.append(Paragraph(proj['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

# ===== RUN APPLICATION =====

if __name__ == '__main__':
    print("=" * 50)
    print("Resume Builder Server Starting...")
    print("=" * 50)
    print(f"Server running at: http://localhost:5000")
    print(f"Press CTRL+C to quit")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Key Components**:

- **Flask Routes**: Serve HTML and handle PDF generation
- **PDF Generation**: ReportLab-based PDF creation
- **Template Styles**: Three different resume styles
- **Section Builders**: Modular functions for each resume section

---

### Step 2: Understanding the Code

#### Flask Configuration

```python
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
```

**Why CORS?**

- Allows frontend to make requests to backend
- Required for AJAX/Fetch API calls
- Essential for development

#### PDF Generation Flow

```
1. Receive JSON data from frontend
2. Extract resume data and template choice
3. Create BytesIO buffer (in-memory file)
4. Build PDF using ReportLab
5. Return PDF as downloadable file
```

#### ReportLab Concepts

**SimpleDocTemplate**:

- Main PDF document container
- Handles page layout and margins

**Paragraph**:

- Text element with styling
- Supports HTML-like formatting

**Styles**:

- Define text appearance
- Reusable across document

**Spacer**:

- Adds vertical space
- Controls layout spacing

---

## PDF Generation with ReportLab

### Understanding ReportLab Structure

```python
# 1. Create document
doc = SimpleDocTemplate(buffer, pagesize=letter)

# 2. Create story (list of elements)
story = []

# 3. Add elements to story
story.append(Paragraph("Text", style))
story.append(Spacer(1, 0.2*inch))

# 4. Build PDF
doc.build(story)
```

### Custom Styles Explained

```python
ParagraphStyle(
    name='CustomName',           # Unique identifier
    parent=styles['Heading1'],   # Inherit from base style
    fontSize=24,                 # Text size
    textColor=colors.blue,       # Text color
    spaceAfter=6,               # Space after element
    alignment=TA_CENTER,         # Text alignment
    fontName='Helvetica-Bold'    # Font family
)
```

### Color System

```python
# Hex colors
colors.HexColor('#2563eb')

# Named colors
colors.black
colors.blue
colors.red

# RGB colors
colors.Color(0.5, 0.5, 0.5)  # Gray
```

### Template Differences

**Modern Template**:

- Blue accent color (#2563eb)
- Centered name
- Helvetica font
- Border on section headings

**Classic Template**:

- Black text throughout
- Times New Roman font
- Traditional layout
- No colors or borders

**Minimal Template**:

- Left-aligned
- Smaller font sizes
- Gray text for meta info
- Clean and simple

---

## API Endpoints

### 1. GET /

**Purpose**: Serve the main HTML page

**Response**: HTML template

**Example**:

```
GET http://localhost:5000/
```

### 2. POST /generate-pdf

**Purpose**: Generate PDF from resume data

**Request Body**:

```json
{
  "data": {
    "personal": {
      "fullName": "John Doe",
      "email": "john@example.com",
      ...
    },
    "education": [...],
    "experience": [...],
    "skills": [...],
    "projects": [...]
  },
  "template": "modern"
}
```

**Response**: PDF file (application/pdf)

**Error Response**:

```json
{
  "error": "Error message"
}
```

### 3. GET /health

**Purpose**: Check if server is running

**Response**:

```json
{
  "status": "ok",
  "message": "Server is running"
}
```

---

## Testing the Backend

### Step 1: Start the Server

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run the server
python app.py
```

**Expected Output**:

```
==================================================
Resume Builder Server Starting...
==================================================
Server running at: http://localhost:5000
Press CTRL+C to quit
==================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Step 2: Test Health Endpoint

Open browser and navigate to:

```
http://localhost:5000/health
```

**Expected Response**:

```json
{ "status": "ok", "message": "Server is running" }
```

### Step 3: Test Main Page

Navigate to:

```
http://localhost:5000/
```

You should see the Resume Builder interface.

### Step 4: Test PDF Generation

1. Fill in the form with sample data
2. Click "Download PDF"
3. Check if PDF downloads
4. Open PDF and verify content

### Step 5: Test Different Templates

1. Switch template selector to "Classic"
2. Generate PDF
3. Compare with "Modern" template
4. Test "Minimal" template

### Step 6: Test Error Handling

**Test with empty data**:

```javascript
// In browser console
fetch("/generate-pdf", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ data: {}, template: "modern" }),
})
  .then((r) => r.blob())
  .then((blob) => console.log("PDF size:", blob.size));
```

### Step 7: Check Server Logs

Monitor terminal for:

- Request logs
- Error messages
- Status codes

**Example logs**:

```
127.0.0.1 - - [20/Jan/2026 12:00:00] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Jan/2026 12:00:05] "POST /generate-pdf HTTP/1.1" 200 -
```

---

## Advanced Features

### Adding Watermark

```python
def add_watermark(canvas, doc):
    """Add watermark to PDF"""
    canvas.saveState()
    canvas.setFont('Helvetica', 40)
    canvas.setFillColorRGB(0.9, 0.9, 0.9)
    canvas.drawCentredString(4.25*inch, 5.5*inch, "DRAFT")
    canvas.restoreState()

# Use in SimpleDocTemplate
doc = SimpleDocTemplate(
    buffer,
    pagesize=letter,
    onFirstPage=add_watermark,
    onLaterPages=add_watermark
)
```

### Adding Page Numbers

```python
def add_page_number(canvas, doc):
    """Add page numbers"""
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(7.5*inch, 0.5*inch, text)
```

### Custom Fonts

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register custom font
pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))

# Use in style
ParagraphStyle(
    name='CustomStyle',
    fontName='CustomFont',
    ...
)
```

### Adding Images/Logo

```python
from reportlab.platypus import Image

# Add to story
logo = Image('path/to/logo.png', width=1*inch, height=1*inch)
story.append(logo)
```

---

## Debugging Tips

### Issue: PDF not generating

**Check**:

1. Is ReportLab installed? `pip list | grep reportlab`
2. Are there errors in terminal?
3. Is data structure correct?

**Debug**:

```python
# Add print statements
print(f"Received data: {data}")
print(f"Template: {template}")
```

### Issue: PDF formatting looks wrong

**Check**:

1. Style definitions
2. Spacer values
3. Font availability

**Debug**:

```python
# Test individual sections
story = []
story.extend(build_personal_section(data['personal'], styles))
# Comment out other sections to isolate issue
```

### Issue: Server crashes

**Check**:

1. Python version compatibility
2. Missing dependencies
3. Port conflicts

**Solution**:

```bash
# Check what's using port 5000
# Windows:
netstat -ano | findstr :5000

# macOS/Linux:
lsof -i :5000

# Use different port
app.run(debug=True, port=5001)
```

### Issue: CORS errors

**Check browser console**:

```
Access to fetch at 'http://localhost:5000/generate-pdf' from origin 'null'
has been blocked by CORS policy
```

**Solution**:

```python
# Make sure Flask-CORS is installed and configured
from flask_cors import CORS
CORS(app)
```

---

## Performance Optimization

### Caching Styles

```python
# Cache styles globally
_cached_styles = {}

def get_styles(template):
    if template not in _cached_styles:
        _cached_styles[template] = create_styles(template)
    return _cached_styles[template]
```

### Async PDF Generation

```python
from threading import Thread

def generate_pdf_async(data, template, callback):
    thread = Thread(target=lambda: callback(create_resume_pdf(data, template)))
    thread.start()
```

### Compression

```python
# Enable PDF compression
doc = SimpleDocTemplate(
    buffer,
    pagesize=letter,
    compress=True  # Reduce file size
)
```

---

## Security Considerations

### Input Validation

```python
def validate_resume_data(data):
    """Validate incoming data"""
    required_fields = ['personal']

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Sanitize strings
    if 'personal' in data:
        for key, value in data['personal'].items():
            if isinstance(value, str):
                # Remove potentially harmful characters
                data['personal'][key] = value.strip()

    return data

# Use in route
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.json
    validated_data = validate_resume_data(data.get('data', {}))
    # ... continue
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/generate-pdf', methods=['POST'])
@limiter.limit("10 per minute")
def generate_pdf():
    # ... route logic
```

### File Size Limits

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413
```

---

## Next Steps

Backend complete! Now you have:

- ✅ Working Flask server
- ✅ PDF generation functionality
- ✅ Multiple template support
- ✅ Error handling

Proceed to:

- **[Features Guide](05-FEATURES-GUIDE.md)** - Understand all features in detail
- **[Troubleshooting](06-TROUBLESHOOTING.md)** - Fix common issues

---

## Testing Checklist

- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] Main page loads correctly
- [ ] PDF generates with sample data
- [ ] All three templates work
- [ ] PDF contains correct data
- [ ] Error handling works
- [ ] No console errors
- [ ] PDF downloads properly
- [ ] File naming is correct

---

**Congratulations!** You've built a complete backend. Test thoroughly and move on to exploring features!
