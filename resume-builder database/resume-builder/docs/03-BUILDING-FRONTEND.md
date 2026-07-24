# Building the Frontend 🎨

This guide walks you through building the frontend step-by-step. You'll create the HTML structure, style it with CSS, and add interactivity with JavaScript.

## Table of Contents

1. [HTML Structure](#html-structure)
2. [CSS Styling](#css-styling)
3. [JavaScript Functionality](#javascript-functionality)
4. [Testing the Frontend](#testing-the-frontend)

---

## HTML Structure

### Step 1: Create index.html

Create `templates/index.html` with the basic structure:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Resume Builder - Create Your Professional Resume</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
  </head>
  <body>
    <div class="container">
      <!-- Header -->
      <header class="header">
        <h1>📄 Resume Builder</h1>
        <p class="subtitle">Create your professional resume in minutes</p>
      </header>

      <!-- Main Content -->
      <main class="main-content">
        <!-- Left Panel: Form -->
        <section class="form-section">
          <!-- Form content will go here -->
        </section>

        <!-- Right Panel: Preview -->
        <section class="preview-section">
          <!-- Preview content will go here -->
        </section>
      </main>
    </div>

    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
  </body>
</html>
```

**Key Points**:

- `{{ url_for() }}` is Flask's template syntax for linking static files
- Responsive viewport meta tag for mobile support
- Semantic HTML5 elements (header, main, section)

---

### Step 2: Build the Form Section

Add this inside the `<section class="form-section">`:

```html
<div class="form-container">
  <h2>Your Information</h2>

  <!-- Personal Information -->
  <div class="form-group">
    <h3>Personal Details</h3>
    <div class="input-row">
      <div class="input-field">
        <label for="fullName">Full Name *</label>
        <input type="text" id="fullName" placeholder="John Doe" required />
      </div>
      <div class="input-field">
        <label for="email">Email *</label>
        <input type="email" id="email" placeholder="john@example.com" required />
      </div>
    </div>

    <div class="input-row">
      <div class="input-field">
        <label for="phone">Phone</label>
        <input type="tel" id="phone" placeholder="+1 234 567 8900" />
      </div>
      <div class="input-field">
        <label for="location">Location</label>
        <input type="text" id="location" placeholder="New York, USA" />
      </div>
    </div>

    <div class="input-field">
      <label for="linkedin">LinkedIn</label>
      <input type="url" id="linkedin" placeholder="linkedin.com/in/johndoe" />
    </div>

    <div class="input-field">
      <label for="summary">Professional Summary</label>
      <textarea id="summary" rows="4" placeholder="Brief overview of your professional background..."></textarea>
    </div>
  </div>

  <!-- Education Section -->
  <div class="form-group">
    <div class="section-header">
      <h3>Education</h3>
      <button type="button" class="btn-add" onclick="addEducation()">+ Add Education</button>
    </div>
    <div id="educationContainer">
      <!-- Education entries will be added here dynamically -->
    </div>
  </div>

  <!-- Experience Section -->
  <div class="form-group">
    <div class="section-header">
      <h3>Work Experience</h3>
      <button type="button" class="btn-add" onclick="addExperience()">+ Add Experience</button>
    </div>
    <div id="experienceContainer">
      <!-- Experience entries will be added here dynamically -->
    </div>
  </div>

  <!-- Skills Section -->
  <div class="form-group">
    <h3>Skills</h3>
    <div class="input-field">
      <label for="skillInput">Add Skills (press Enter)</label>
      <input type="text" id="skillInput" placeholder="e.g., JavaScript, Python, React" />
    </div>
    <div id="skillsContainer" class="skills-tags">
      <!-- Skill tags will appear here -->
    </div>
  </div>

  <!-- Projects Section -->
  <div class="form-group">
    <div class="section-header">
      <h3>Projects</h3>
      <button type="button" class="btn-add" onclick="addProject()">+ Add Project</button>
    </div>
    <div id="projectsContainer">
      <!-- Project entries will be added here dynamically -->
    </div>
  </div>

  <!-- Action Buttons -->
  <div class="form-actions">
    <button type="button" class="btn-secondary" onclick="clearForm()">Clear All</button>
    <button type="button" class="btn-secondary" onclick="saveData()">Save Draft</button>
    <button type="button" class="btn-primary" onclick="generatePDF()">Download PDF</button>
  </div>
</div>
```

**Understanding the Structure**:

- **Form Groups**: Each section (Personal, Education, etc.) is wrapped in `.form-group`
- **Dynamic Sections**: Education, Experience, and Projects use containers that JavaScript will populate
- **Input Fields**: Consistent structure with labels and inputs
- **Action Buttons**: Clear, Save, and Download functionality

---

### Step 3: Build the Preview Section

Add this inside `<section class="preview-section">`:

```html
<div class="preview-container">
  <div class="preview-header">
    <h2>Live Preview</h2>
    <select id="templateSelector" onchange="changeTemplate()">
      <option value="modern">Modern</option>
      <option value="classic">Classic</option>
      <option value="minimal">Minimal</option>
    </select>
  </div>

  <div class="resume-preview" id="resumePreview">
    <!-- Personal Info -->
    <div class="preview-personal">
      <h1 id="previewName">Your Name</h1>
      <div class="preview-contact">
        <span id="previewEmail"></span>
        <span id="previewPhone"></span>
        <span id="previewLocation"></span>
      </div>
      <div id="previewLinkedin"></div>
      <p id="previewSummary" class="preview-summary"></p>
    </div>

    <!-- Education -->
    <div class="preview-section" id="previewEducationSection" style="display: none;">
      <h2 class="section-title">Education</h2>
      <div id="previewEducation"></div>
    </div>

    <!-- Experience -->
    <div class="preview-section" id="previewExperienceSection" style="display: none;">
      <h2 class="section-title">Experience</h2>
      <div id="previewExperience"></div>
    </div>

    <!-- Skills -->
    <div class="preview-section" id="previewSkillsSection" style="display: none;">
      <h2 class="section-title">Skills</h2>
      <div id="previewSkills" class="skills-list"></div>
    </div>

    <!-- Projects -->
    <div class="preview-section" id="previewProjectsSection" style="display: none;">
      <h2 class="section-title">Projects</h2>
      <div id="previewProjects"></div>
    </div>
  </div>
</div>
```

**Key Features**:

- **Template Selector**: Dropdown to switch between resume styles
- **Live Preview**: Updates as user types
- **Conditional Sections**: Sections hidden until data is added
- **Structured Layout**: Mirrors professional resume format

---

## CSS Styling

### Step 1: Create style.css

Create `static/css/style.css` with CSS variables and reset:

```css
/* ===== CSS VARIABLES ===== */
:root {
  /* Colors */
  --primary-color: #2563eb;
  --primary-dark: #1e40af;
  --secondary-color: #64748b;
  --success-color: #10b981;
  --danger-color: #ef4444;

  /* Neutrals */
  --bg-color: #f8fafc;
  --surface-color: #ffffff;
  --border-color: #e2e8f0;
  --text-primary: #1e293b;
  --text-secondary: #64748b;

  /* Spacing */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Typography */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, sans-serif;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
}

/* ===== RESET & BASE ===== */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: var(--font-size-base);
}

/* ===== LAYOUT ===== */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-xl) 0;
}

.header h1 {
  font-size: var(--font-size-2xl);
  color: var(--primary-color);
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-lg);
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  align-items: start;
}

/* ===== FORM SECTION ===== */
.form-section {
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
}

.form-container h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--text-primary);
}

.form-group {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--border-color);
}

.form-group:last-child {
  border-bottom: none;
}

.form-group h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: var(--font-size-lg);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

/* ===== INPUT FIELDS ===== */
.input-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.input-field {
  margin-bottom: var(--spacing-md);
}

.input-field label {
  display: block;
  margin-bottom: var(--spacing-xs);
  font-weight: 500;
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.input-field input,
.input-field textarea,
.input-field select {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: var(--font-size-base);
  transition: all 0.2s ease;
}

.input-field input:focus,
.input-field textarea:focus,
.input-field select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.input-field textarea {
  resize: vertical;
  min-height: 80px;
}

/* ===== BUTTONS ===== */
.btn-primary,
.btn-secondary,
.btn-add,
.btn-remove {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background-color: var(--surface-color);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--bg-color);
}

.btn-add {
  background-color: var(--success-color);
  color: white;
  font-size: var(--font-size-sm);
  padding: var(--spacing-xs) var(--spacing-md);
}

.btn-add:hover {
  opacity: 0.9;
}

.btn-remove {
  background-color: var(--danger-color);
  color: white;
  font-size: var(--font-size-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
}

.btn-remove:hover {
  opacity: 0.9;
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  margin-top: var(--spacing-xl);
}

/* ===== DYNAMIC ENTRIES ===== */
.entry-item {
  background-color: var(--bg-color);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
  position: relative;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

/* ===== SKILLS TAGS ===== */
.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
}

.skill-tag {
  background-color: var(--primary-color);
  color: white;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.skill-tag .remove-skill {
  cursor: pointer;
  font-weight: bold;
}

.skill-tag .remove-skill:hover {
  color: var(--danger-color);
}

/* ===== PREVIEW SECTION ===== */
.preview-section {
  position: sticky;
  top: var(--spacing-lg);
  background: var(--surface-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-color);
}

.preview-header h2 {
  color: var(--text-primary);
}

#templateSelector {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

/* ===== RESUME PREVIEW STYLES ===== */
.resume-preview {
  background: white;
  padding: var(--spacing-xl);
  min-height: 400px;
}

.preview-personal {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--primary-color);
}

.preview-personal h1 {
  font-size: var(--font-size-2xl);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.preview-contact {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-sm);
}

.preview-contact span:not(:empty)::after {
  content: " • ";
  margin-left: var(--spacing-md);
}

.preview-contact span:last-child::after {
  content: "";
}

.preview-summary {
  color: var(--text-secondary);
  line-height: 1.8;
  margin-top: var(--spacing-md);
}

.preview-section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  color: var(--primary-color);
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.preview-item {
  margin-bottom: var(--spacing-lg);
}

.preview-item h3 {
  color: var(--text-primary);
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xs);
}

.preview-item .item-meta {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-sm);
}

.preview-item p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.skill-badge {
  background-color: var(--bg-color);
  color: var(--primary-color);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  border: 1px solid var(--border-color);
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .preview-section {
    position: static;
    max-height: none;
  }
}

@media (max-width: 768px) {
  .container {
    padding: var(--spacing-md);
  }

  .input-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }
}

/* ===== ANIMATIONS ===== */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.entry-item,
.skill-tag {
  animation: fadeIn 0.3s ease;
}

/* ===== PRINT STYLES ===== */
@media print {
  body {
    background: white;
  }

  .form-section,
  .preview-header {
    display: none;
  }

  .preview-section {
    box-shadow: none;
    padding: 0;
  }
}
```

**CSS Organization**:

1. **Variables**: Centralized design tokens
2. **Reset**: Consistent baseline
3. **Layout**: Grid-based responsive layout
4. **Components**: Modular, reusable styles
5. **Responsive**: Mobile-first approach
6. **Animations**: Smooth transitions

---

## JavaScript Functionality

### Step 1: Create app.js

Create `static/js/app.js` with the core functionality:

```javascript
// ===== STATE MANAGEMENT =====
let resumeData = {
  personal: {
    fullName: "",
    email: "",
    phone: "",
    location: "",
    linkedin: "",
    summary: "",
  },
  education: [],
  experience: [],
  skills: [],
  projects: [],
};

let currentTemplate = "modern";

// ===== INITIALIZATION =====
document.addEventListener("DOMContentLoaded", function () {
  loadFromStorage();
  setupEventListeners();
  addEducation(); // Add one education entry by default
  addExperience(); // Add one experience entry by default
});

// ===== EVENT LISTENERS =====
function setupEventListeners() {
  // Personal info inputs
  const personalFields = ["fullName", "email", "phone", "location", "linkedin", "summary"];
  personalFields.forEach((field) => {
    const element = document.getElementById(field);
    if (element) {
      element.addEventListener("input", function () {
        resumeData.personal[field] = this.value;
        updatePreview();
        autoSave();
      });
    }
  });

  // Skills input
  const skillInput = document.getElementById("skillInput");
  if (skillInput) {
    skillInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        addSkill(this.value.trim());
        this.value = "";
      }
    });
  }
}

// ===== DYNAMIC SECTIONS =====

// Education
function addEducation() {
  const container = document.getElementById("educationContainer");
  const index = resumeData.education.length;

  const educationEntry = {
    degree: "",
    institution: "",
    location: "",
    startDate: "",
    endDate: "",
    description: "",
  };

  resumeData.education.push(educationEntry);

  const entryHTML = `
        <div class="entry-item" data-index="${index}">
            <div class="entry-header">
                <strong>Education ${index + 1}</strong>
                <button type="button" class="btn-remove" onclick="removeEducation(${index})">Remove</button>
            </div>
            <div class="input-field">
                <label>Degree/Certification</label>
                <input type="text" placeholder="e.g., Bachelor of Science in Computer Science" 
                       onchange="updateEducation(${index}, 'degree', this.value)">
            </div>
            <div class="input-field">
                <label>Institution</label>
                <input type="text" placeholder="e.g., University Name" 
                       onchange="updateEducation(${index}, 'institution', this.value)">
            </div>
            <div class="input-row">
                <div class="input-field">
                    <label>Location</label>
                    <input type="text" placeholder="e.g., New York, USA" 
                           onchange="updateEducation(${index}, 'location', this.value)">
                </div>
                <div class="input-field">
                    <label>Duration</label>
                    <input type="text" placeholder="e.g., 2020 - 2024" 
                           onchange="updateEducation(${index}, 'duration', this.value)">
                </div>
            </div>
            <div class="input-field">
                <label>Description (Optional)</label>
                <textarea placeholder="GPA, achievements, relevant coursework..." 
                          onchange="updateEducation(${index}, 'description', this.value)"></textarea>
            </div>
        </div>
    `;

  container.insertAdjacentHTML("beforeend", entryHTML);
}

function updateEducation(index, field, value) {
  if (resumeData.education[index]) {
    resumeData.education[index][field] = value;
    updatePreview();
    autoSave();
  }
}

function removeEducation(index) {
  resumeData.education.splice(index, 1);
  refreshEducationSection();
  updatePreview();
  autoSave();
}

function refreshEducationSection() {
  const container = document.getElementById("educationContainer");
  container.innerHTML = "";
  resumeData.education.forEach((_, index) => {
    addEducation();
  });
}

// Experience
function addExperience() {
  const container = document.getElementById("experienceContainer");
  const index = resumeData.experience.length;

  const experienceEntry = {
    title: "",
    company: "",
    location: "",
    duration: "",
    description: "",
  };

  resumeData.experience.push(experienceEntry);

  const entryHTML = `
        <div class="entry-item" data-index="${index}">
            <div class="entry-header">
                <strong>Experience ${index + 1}</strong>
                <button type="button" class="btn-remove" onclick="removeExperience(${index})">Remove</button>
            </div>
            <div class="input-field">
                <label>Job Title</label>
                <input type="text" placeholder="e.g., Software Engineer" 
                       onchange="updateExperience(${index}, 'title', this.value)">
            </div>
            <div class="input-field">
                <label>Company</label>
                <input type="text" placeholder="e.g., Tech Company Inc." 
                       onchange="updateExperience(${index}, 'company', this.value)">
            </div>
            <div class="input-row">
                <div class="input-field">
                    <label>Location</label>
                    <input type="text" placeholder="e.g., San Francisco, CA" 
                           onchange="updateExperience(${index}, 'location', this.value)">
                </div>
                <div class="input-field">
                    <label>Duration</label>
                    <input type="text" placeholder="e.g., Jan 2023 - Present" 
                           onchange="updateExperience(${index}, 'duration', this.value)">
                </div>
            </div>
            <div class="input-field">
                <label>Description</label>
                <textarea placeholder="Key responsibilities and achievements..." 
                          onchange="updateExperience(${index}, 'description', this.value)"></textarea>
            </div>
        </div>
    `;

  container.insertAdjacentHTML("beforeend", entryHTML);
}

function updateExperience(index, field, value) {
  if (resumeData.experience[index]) {
    resumeData.experience[index][field] = value;
    updatePreview();
    autoSave();
  }
}

function removeExperience(index) {
  resumeData.experience.splice(index, 1);
  refreshExperienceSection();
  updatePreview();
  autoSave();
}

function refreshExperienceSection() {
  const container = document.getElementById("experienceContainer");
  container.innerHTML = "";
  resumeData.experience.forEach((_, index) => {
    addExperience();
  });
}

// Skills
function addSkill(skill) {
  if (skill && !resumeData.skills.includes(skill)) {
    resumeData.skills.push(skill);
    renderSkills();
    updatePreview();
    autoSave();
  }
}

function removeSkill(skill) {
  const index = resumeData.skills.indexOf(skill);
  if (index > -1) {
    resumeData.skills.splice(index, 1);
    renderSkills();
    updatePreview();
    autoSave();
  }
}

function renderSkills() {
  const container = document.getElementById("skillsContainer");
  container.innerHTML = resumeData.skills
    .map(
      (skill) => `
        <span class="skill-tag">
            ${skill}
            <span class="remove-skill" onclick="removeSkill('${skill}')">×</span>
        </span>
    `,
    )
    .join("");
}

// Projects
function addProject() {
  const container = document.getElementById("projectsContainer");
  const index = resumeData.projects.length;

  const projectEntry = {
    name: "",
    technologies: "",
    duration: "",
    description: "",
    link: "",
  };

  resumeData.projects.push(projectEntry);

  const entryHTML = `
        <div class="entry-item" data-index="${index}">
            <div class="entry-header">
                <strong>Project ${index + 1}</strong>
                <button type="button" class="btn-remove" onclick="removeProject(${index})">Remove</button>
            </div>
            <div class="input-field">
                <label>Project Name</label>
                <input type="text" placeholder="e.g., E-commerce Website" 
                       onchange="updateProject(${index}, 'name', this.value)">
            </div>
            <div class="input-row">
                <div class="input-field">
                    <label>Technologies Used</label>
                    <input type="text" placeholder="e.g., React, Node.js, MongoDB" 
                           onchange="updateProject(${index}, 'technologies', this.value)">
                </div>
                <div class="input-field">
                    <label>Duration</label>
                    <input type="text" placeholder="e.g., 3 months" 
                           onchange="updateProject(${index}, 'duration', this.value)">
                </div>
            </div>
            <div class="input-field">
                <label>Description</label>
                <textarea placeholder="Project details and your contributions..." 
                          onchange="updateProject(${index}, 'description', this.value)"></textarea>
            </div>
            <div class="input-field">
                <label>Link (Optional)</label>
                <input type="url" placeholder="https://github.com/..." 
                       onchange="updateProject(${index}, 'link', this.value)">
            </div>
        </div>
    `;

  container.insertAdjacentHTML("beforeend", entryHTML);
}

function updateProject(index, field, value) {
  if (resumeData.projects[index]) {
    resumeData.projects[index][field] = value;
    updatePreview();
    autoSave();
  }
}

function removeProject(index) {
  resumeData.projects.splice(index, 1);
  refreshProjectsSection();
  updatePreview();
  autoSave();
}

function refreshProjectsSection() {
  const container = document.getElementById("projectsContainer");
  container.innerHTML = "";
  resumeData.projects.forEach((_, index) => {
    addProject();
  });
}

// ===== PREVIEW UPDATE =====
function updatePreview() {
  // Personal Info
  document.getElementById("previewName").textContent = resumeData.personal.fullName || "Your Name";
  document.getElementById("previewEmail").textContent = resumeData.personal.email;
  document.getElementById("previewPhone").textContent = resumeData.personal.phone;
  document.getElementById("previewLocation").textContent = resumeData.personal.location;
  document.getElementById("previewLinkedin").textContent = resumeData.personal.linkedin;
  document.getElementById("previewSummary").textContent = resumeData.personal.summary;

  // Education
  const educationSection = document.getElementById("previewEducationSection");
  const educationContainer = document.getElementById("previewEducation");
  if (resumeData.education.length > 0 && resumeData.education.some((e) => e.degree || e.institution)) {
    educationSection.style.display = "block";
    educationContainer.innerHTML = resumeData.education
      .filter((e) => e.degree || e.institution)
      .map(
        (edu) => `
                <div class="preview-item">
                    <h3>${edu.degree || "Degree"}</h3>
                    <div class="item-meta">
                        ${edu.institution || ""}${edu.location ? " • " + edu.location : ""}
                        ${edu.duration ? " • " + edu.duration : ""}
                    </div>
                    ${edu.description ? `<p>${edu.description}</p>` : ""}
                </div>
            `,
      )
      .join("");
  } else {
    educationSection.style.display = "none";
  }

  // Experience
  const experienceSection = document.getElementById("previewExperienceSection");
  const experienceContainer = document.getElementById("previewExperience");
  if (resumeData.experience.length > 0 && resumeData.experience.some((e) => e.title || e.company)) {
    experienceSection.style.display = "block";
    experienceContainer.innerHTML = resumeData.experience
      .filter((e) => e.title || e.company)
      .map(
        (exp) => `
                <div class="preview-item">
                    <h3>${exp.title || "Job Title"}</h3>
                    <div class="item-meta">
                        ${exp.company || ""}${exp.location ? " • " + exp.location : ""}
                        ${exp.duration ? " • " + exp.duration : ""}
                    </div>
                    ${exp.description ? `<p>${exp.description}</p>` : ""}
                </div>
            `,
      )
      .join("");
  } else {
    experienceSection.style.display = "none";
  }

  // Skills
  const skillsSection = document.getElementById("previewSkillsSection");
  const skillsContainer = document.getElementById("previewSkills");
  if (resumeData.skills.length > 0) {
    skillsSection.style.display = "block";
    skillsContainer.innerHTML = resumeData.skills.map((skill) => `<span class="skill-badge">${skill}</span>`).join("");
  } else {
    skillsSection.style.display = "none";
  }

  // Projects
  const projectsSection = document.getElementById("previewProjectsSection");
  const projectsContainer = document.getElementById("previewProjects");
  if (resumeData.projects.length > 0 && resumeData.projects.some((p) => p.name)) {
    projectsSection.style.display = "block";
    projectsContainer.innerHTML = resumeData.projects
      .filter((p) => p.name)
      .map(
        (proj) => `
                <div class="preview-item">
                    <h3>${proj.name}${proj.link ? ` <a href="${proj.link}" target="_blank">🔗</a>` : ""}</h3>
                    <div class="item-meta">
                        ${proj.technologies || ""}${proj.duration ? " • " + proj.duration : ""}
                    </div>
                    ${proj.description ? `<p>${proj.description}</p>` : ""}
                </div>
            `,
      )
      .join("");
  } else {
    projectsSection.style.display = "none";
  }
}

// ===== TEMPLATE SWITCHING =====
function changeTemplate() {
  currentTemplate = document.getElementById("templateSelector").value;
  const preview = document.getElementById("resumePreview");

  // Remove existing template classes
  preview.classList.remove("template-modern", "template-classic", "template-minimal");

  // Add new template class
  preview.classList.add(`template-${currentTemplate}`);

  autoSave();
}

// ===== STORAGE =====
function autoSave() {
  try {
    localStorage.setItem("resumeData", JSON.stringify(resumeData));
    localStorage.setItem("currentTemplate", currentTemplate);
  } catch (e) {
    console.error("Failed to save to localStorage:", e);
  }
}

function loadFromStorage() {
  try {
    const saved = localStorage.getItem("resumeData");
    const savedTemplate = localStorage.getItem("currentTemplate");

    if (saved) {
      resumeData = JSON.parse(saved);

      // Populate personal fields
      Object.keys(resumeData.personal).forEach((key) => {
        const element = document.getElementById(key);
        if (element) {
          element.value = resumeData.personal[key];
        }
      });

      // Render skills
      renderSkills();

      // Update preview
      updatePreview();
    }

    if (savedTemplate) {
      currentTemplate = savedTemplate;
      document.getElementById("templateSelector").value = currentTemplate;
      changeTemplate();
    }
  } catch (e) {
    console.error("Failed to load from localStorage:", e);
  }
}

function saveData() {
  autoSave();
  alert("Resume data saved successfully!");
}

function clearForm() {
  if (confirm("Are you sure you want to clear all data? This cannot be undone.")) {
    localStorage.clear();
    location.reload();
  }
}

// ===== PDF GENERATION =====
function generatePDF() {
  // Show loading state
  const btn = event.target;
  const originalText = btn.textContent;
  btn.textContent = "Generating...";
  btn.disabled = true;

  // Send data to backend
  fetch("/generate-pdf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      data: resumeData,
      template: currentTemplate,
    }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume_${resumeData.personal.fullName.replace(/\s+/g, "_") || "download"}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Reset button
      btn.textContent = originalText;
      btn.disabled = false;
    })
    .catch((error) => {
      console.error("Error generating PDF:", error);
      alert("Failed to generate PDF. Please try again.");
      btn.textContent = originalText;
      btn.disabled = false;
    });
}
```

**JavaScript Architecture**:

1. **State Management**: Central `resumeData` object
2. **Event Handling**: Listeners for all user interactions
3. **Dynamic DOM**: Add/remove sections dynamically
4. **Real-time Updates**: Preview updates as user types
5. **Persistence**: Auto-save to LocalStorage
6. **API Communication**: Fetch API for PDF generation

---

## Testing the Frontend

### Step 1: Manual Testing Checklist

✅ **Personal Information**

- [ ] Enter name, email, phone
- [ ] Check preview updates in real-time
- [ ] Verify all fields display correctly

✅ **Education Section**

- [ ] Click "Add Education"
- [ ] Fill in degree, institution, dates
- [ ] Add multiple education entries
- [ ] Remove an entry
- [ ] Check preview formatting

✅ **Experience Section**

- [ ] Add work experience
- [ ] Fill all fields
- [ ] Test with multiple entries
- [ ] Remove entries

✅ **Skills**

- [ ] Type skill and press Enter
- [ ] Add multiple skills
- [ ] Remove skills by clicking ×
- [ ] Check preview displays as badges

✅ **Projects**

- [ ] Add project entries
- [ ] Include links
- [ ] Test description formatting

✅ **Template Switching**

- [ ] Switch between Modern, Classic, Minimal
- [ ] Verify layout changes
- [ ] Check all sections display correctly

✅ **Storage**

- [ ] Fill in data
- [ ] Refresh page
- [ ] Verify data persists
- [ ] Test "Clear All" button

### Step 2: Browser Console Testing

Open DevTools (F12) and check:

```javascript
// Check if data is saving
console.log(localStorage.getItem("resumeData"));

// Check current state
console.log(resumeData);

// Test a function
updatePreview();
```

### Step 3: Responsive Testing

Test on different screen sizes:

- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

Use Chrome DevTools Device Mode (Ctrl+Shift+M)

---

## Common Issues & Solutions

### Issue: Preview not updating

**Solution**: Check browser console for errors. Ensure all IDs match between HTML and JavaScript.

### Issue: LocalStorage not working

**Solution**: Check browser privacy settings. Some browsers block LocalStorage in incognito mode.

### Issue: Buttons not working

**Solution**: Verify onclick handlers are correctly named and functions are defined.

### Issue: Styling looks broken

**Solution**: Check if CSS file is loading. Verify Flask static file paths.

---

## Next Steps

Frontend complete! Now proceed to:

- **[Building Backend](04-BUILDING-BACKEND.md)** - Create Flask server and PDF generation

---

**Great job!** You've built a fully functional frontend. Test thoroughly before moving to the backend.
