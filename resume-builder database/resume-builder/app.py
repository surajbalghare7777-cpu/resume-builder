from flask import Flask, render_template, request, send_file, jsonify, url_for
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from PIL import Image as PILImage
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

from config import Config
from models import db, Candidate

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

for folder in [Config.UPLOAD_FOLDER, Config.PHOTO_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

GENERATED_PDFS_FOLDER = 'generated_pdfs'
if not os.path.exists(GENERATED_PDFS_FOLDER):
    os.makedirs(GENERATED_PDFS_FOLDER)

def allowed_photo(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_PHOTO_EXTENSIONS

# ─── Page Routes ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidates')
def candidates_page():
    return render_template('candidates.html')

# ─── Photo Upload ───────────────────────────────────────────────────────────────

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({'error': 'No photo file provided'}), 400

        file = request.files['photo']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_photo(file.filename):
            return jsonify({'error': 'Only PNG, JPG, JPEG files are allowed'}), 400

        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(Config.PHOTO_FOLDER, unique_name)

        img = PILImage.open(file.stream)
        img = img.convert('RGB')
        img.thumbnail((600, 800), PILImage.LANCZOS)
        img.save(filepath, quality=90)

        return jsonify({
            'success': True,
            'filename': unique_name,
            'url': f'/uploads/photos/{unique_name}'
        })

    except Exception as e:
        print(f"Error uploading photo: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/photos/<filename>')
def serve_photo(filename):
    return send_file(os.path.join(Config.PHOTO_FOLDER, secure_filename(filename)))

# ─── PDF Generation ─────────────────────────────────────────────────────────────

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        resume_data = data.get('data', {})
        template = data.get('template', 'modern')

        pdf_buffer = create_resume_pdf(resume_data, template)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ─── Candidate CRUD API ────────────────────────────────────────────────────────

@app.route('/api/candidates', methods=['GET'])
def list_candidates():
    try:
        search = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        skill_filter = request.args.get('skill', '').strip()
        location_filter = request.args.get('location', '').strip()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        query = Candidate.query

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Candidate.full_name.ilike(search_term),
                    Candidate.email.ilike(search_term),
                    Candidate.phone.ilike(search_term),
                    Candidate.location.ilike(search_term)
                )
            )

        if location_filter:
            query = query.filter(Candidate.location.ilike(f"%{location_filter}%"))

        if skill_filter:
            query = query.filter(Candidate.skills.like(f'%"{skill_filter}"%'))

        allowed_sort = {
            'full_name': Candidate.full_name,
            'email': Candidate.email,
            'location': Candidate.location,
            'created_at': Candidate.created_at,
            'updated_at': Candidate.updated_at,
        }
        sort_col = allowed_sort.get(sort_by, Candidate.created_at)
        if sort_order == 'asc':
            query = query.order_by(sort_col.asc())
        else:
            query = query.order_by(sort_col.desc())

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'candidates': [c.to_dict() for c in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page
        })

    except Exception as e:
        print(f"Error listing candidates: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates', methods=['POST'])
def create_candidate():
    try:
        data = request.json
        resume = data.get('data', {})
        personal = resume.get('personal', {})

        if not personal.get('fullName') or not personal.get('email'):
            return jsonify({'error': 'Full name and email are required'}), 400

        existing = Candidate.query.filter_by(email=personal['email']).first()
        if existing:
            return jsonify({'error': 'A candidate with this email already exists', 'candidate_id': existing.id}), 409

        candidate = Candidate(
            full_name=personal.get('fullName', ''),
            email=personal.get('email', ''),
            phone=personal.get('phone', ''),
            location=personal.get('location', ''),
            linkedin=personal.get('linkedin', ''),
            summary=personal.get('summary', ''),
            photo_filename=personal.get('photo_filename', ''),
            template=data.get('template', 'modern'),
            education=resume.get('education', []),
            experience=resume.get('experience', []),
            skills=resume.get('skills', []),
            projects=resume.get('projects', []),
        )

        db.session.add(candidate)
        db.session.commit()

        return jsonify({'success': True, 'candidate': candidate.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating candidate: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        return jsonify({'candidate': candidate.to_dict()})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/candidates/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        data = request.json
        resume = data.get('data', {})
        personal = resume.get('personal', {})

        if personal.get('fullName'):
            candidate.full_name = personal['fullName']
        if personal.get('email'):
            candidate.email = personal['email']
        candidate.phone = personal.get('phone', candidate.phone)
        candidate.location = personal.get('location', candidate.location)
        candidate.linkedin = personal.get('linkedin', candidate.linkedin)
        candidate.summary = personal.get('summary', candidate.summary)
        if personal.get('photo_filename'):
            candidate.photo_filename = personal['photo_filename']
        candidate.template = data.get('template', candidate.template)
        candidate.education = resume.get('education', candidate.education)
        candidate.experience = resume.get('experience', candidate.experience)
        candidate.skills = resume.get('skills', candidate.skills)
        candidate.projects = resume.get('projects', candidate.projects)

        db.session.commit()

        return jsonify({'success': True, 'candidate': candidate.to_dict()})

    except Exception as e:
        db.session.rollback()
        print(f"Error updating candidate: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        if candidate.photo_filename:
            photo_path = os.path.join(Config.PHOTO_FOLDER, candidate.photo_filename)
            if os.path.exists(photo_path):
                os.remove(photo_path)

        db.session.delete(candidate)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Candidate deleted'})

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting candidate: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates/stats', methods=['GET'])
def candidate_stats():
    try:
        total = Candidate.query.count()
        locations = db.session.query(
            Candidate.location, db.func.count(Candidate.id)
        ).filter(Candidate.location.isnot(None), Candidate.location != '').group_by(
            Candidate.location
        ).all()

        return jsonify({
            'total_candidates': total,
            'locations': [{'location': loc, 'count': cnt} for loc, cnt in locations],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    db_status = 'unknown'
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception:
        db_status = 'disconnected'

    return jsonify({'status': 'ok', 'message': 'Server is running', 'database': db_status})

def get_photo_for_pdf(photo_filename):
    if not photo_filename:
        return None
    photo_path = os.path.join(Config.PHOTO_FOLDER, photo_filename)
    if not os.path.exists(photo_path):
        return None
    try:
        img = Image(photo_path, width=1.2*inch, height=1.5*inch)
        return img
    except Exception:
        return None

def create_resume_pdf(data, template='modern'):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []
    styles = getSampleStyleSheet()

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

    story.extend(build_personal_section(data.get('personal', {}), styles))
    story.extend(build_education_section(data.get('education', []), styles))
    story.extend(build_experience_section(data.get('experience', []), styles))
    story.extend(build_skills_section(data.get('skills', []), styles))
    story.extend(build_projects_section(data.get('projects', []), styles))

    doc.build(story)
    buffer.seek(0)

    return buffer

# ─── Template Style Definitions ─────────────────────────────────────────────────

def get_modern_styles(base_styles):
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_JUSTIFY,
        spaceAfter=16,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=6
    ))

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

def get_executive_styles(base_styles):
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Times-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4a4a6a'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#4a4a6a'),
        alignment=TA_JUSTIFY,
        spaceAfter=18,
        leading=15,
        fontName='Times-Roman'
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#16213e'),
        spaceAfter=8,
        spaceBefore=14,
        fontName='Times-Bold',
        borderWidth=0,
        borderColor=colors.HexColor('#16213e'),
        borderPadding=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1a1a2e'),
        fontName='Times-Bold',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4a4a6a'),
        spaceAfter=6,
        fontName='Times-Italic'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333355'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14,
        fontName='Times-Roman'
    ))

    return styles

def get_creative_styles(base_styles):
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#e74c3c'),
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_LEFT,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_LEFT,
        spaceAfter=16,
        leading=15
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=15,
        textColor=colors.HexColor('#e74c3c'),
        spaceAfter=8,
        spaceBefore=14,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#34495e'),
        alignment=TA_LEFT,
        spaceAfter=12,
        leading=14
    ))

    return styles

def get_professional_styles(base_styles):
    styles = base_styles

    styles.add(ParagraphStyle(
        name='CustomName',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#0f4c75'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#3282b8'),
        alignment=TA_CENTER,
        spaceAfter=12
    ))

    styles.add(ParagraphStyle(
        name='CustomSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1b262c'),
        alignment=TA_JUSTIFY,
        spaceAfter=16,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#0f4c75'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='CustomItemTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1b262c'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='CustomItemMeta',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#3282b8'),
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CustomItemDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1b262c'),
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=13
    ))

    return styles

# ─── PDF Section Builders ───────────────────────────────────────────────────────

def build_personal_section(personal, styles):
    story = []

    photo_img = get_photo_for_pdf(personal.get('photo_filename'))

    if photo_img and personal.get('fullName'):
        name_para = Paragraph(personal['fullName'], styles['CustomName'])

        contact_parts = []
        if personal.get('email'):
            contact_parts.append(personal['email'])
        if personal.get('phone'):
            contact_parts.append(personal['phone'])
        if personal.get('location'):
            contact_parts.append(personal['location'])
        contact_para = Paragraph(' | '.join(contact_parts), styles['CustomContact']) if contact_parts else Paragraph('', styles['CustomContact'])

        info_cell = [name_para, Spacer(1, 4), contact_para]
        if personal.get('linkedin'):
            info_cell.append(Paragraph(f"LinkedIn: {personal['linkedin']}", styles['CustomContact']))

        header_table = Table(
            [[info_cell, photo_img]],
            colWidths=[5.0*inch, 1.5*inch]
        )
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
    else:
        if personal.get('fullName'):
            story.append(Paragraph(personal['fullName'], styles['CustomName']))

        contact_parts = []
        if personal.get('email'):
            contact_parts.append(personal['email'])
        if personal.get('phone'):
            contact_parts.append(personal['phone'])
        if personal.get('location'):
            contact_parts.append(personal['location'])

        if contact_parts:
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, styles['CustomContact']))

        if personal.get('linkedin'):
            story.append(Paragraph(f"LinkedIn: {personal['linkedin']}", styles['CustomContact']))

    if personal.get('summary'):
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(personal['summary'], styles['CustomSummary']))

    story.append(Spacer(1, 0.15*inch))

    return story

def build_education_section(education, styles):
    story = []

    education = [e for e in education if e.get('degree') or e.get('institution')]

    if not education:
        return story

    story.append(Paragraph('EDUCATION', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for edu in education:
        if edu.get('degree'):
            story.append(Paragraph(edu['degree'], styles['CustomItemTitle']))

        meta_parts = []
        if edu.get('institution'):
            meta_parts.append(edu['institution'])
        if edu.get('location'):
            meta_parts.append(edu['location'])
        if edu.get('duration'):
            meta_parts.append(edu['duration'])

        if meta_parts:
            meta_text = ' | '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        if edu.get('description'):
            story.append(Paragraph(edu['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

def build_experience_section(experience, styles):
    story = []

    experience = [e for e in experience if e.get('title') or e.get('company')]

    if not experience:
        return story

    story.append(Paragraph('EXPERIENCE', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for exp in experience:
        if exp.get('title'):
            story.append(Paragraph(exp['title'], styles['CustomItemTitle']))

        meta_parts = []
        if exp.get('company'):
            meta_parts.append(exp['company'])
        if exp.get('location'):
            meta_parts.append(exp['location'])
        if exp.get('duration'):
            meta_parts.append(exp['duration'])

        if meta_parts:
            meta_text = ' | '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        if exp.get('description'):
            story.append(Paragraph(exp['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

def build_skills_section(skills, styles):
    story = []

    if not skills:
        return story

    story.append(Paragraph('SKILLS', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    skills_text = ' | '.join(skills)
    story.append(Paragraph(skills_text, styles['CustomItemDesc']))
    story.append(Spacer(1, 0.1*inch))

    return story

def build_projects_section(projects, styles):
    story = []

    projects = [p for p in projects if p.get('name')]

    if not projects:
        return story

    story.append(Paragraph('PROJECTS', styles['CustomHeading']))
    story.append(Spacer(1, 0.05*inch))

    for proj in projects:
        project_title = proj['name']
        if proj.get('link'):
            project_title += f" ({proj['link']})"
        story.append(Paragraph(project_title, styles['CustomItemTitle']))

        meta_parts = []
        if proj.get('technologies'):
            meta_parts.append(f"Technologies: {proj['technologies']}")
        if proj.get('duration'):
            meta_parts.append(proj['duration'])

        if meta_parts:
            meta_text = ' | '.join(meta_parts)
            story.append(Paragraph(meta_text, styles['CustomItemMeta']))

        if proj.get('description'):
            story.append(Paragraph(proj['description'], styles['CustomItemDesc']))

        story.append(Spacer(1, 0.1*inch))

    return story

# ─── App Entry Point ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    print("=" * 50)
    print("Resume Builder Server Starting...")
    print("=" * 50)
    print(f"Server running at: http://localhost:5000")
    print(f"Candidates page:   http://localhost:5000/candidates")
    print(f"Press CTRL+C to quit")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
