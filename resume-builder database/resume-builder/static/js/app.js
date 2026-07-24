let resumeData = {
  personal: {
    fullName: "",
    email: "",
    phone: "",
    location: "",
    linkedin: "",
    summary: "",
    photo_filename: "",
  },
  education: [],
  experience: [],
  skills: [],
  projects: [],
};

let currentTemplate = "modern";
let editingCandidateId = null;

document.addEventListener("DOMContentLoaded", function () {
  loadFromStorage();
  setupEventListeners();
  setupPhotoUpload();
  addEducation();
  addExperience();

  const savedEditId = localStorage.getItem("editingCandidateId");
  if (savedEditId) {
    editingCandidateId = parseInt(savedEditId);
    localStorage.removeItem("editingCandidateId");
  }
});

function setupEventListeners() {
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

function setupPhotoUpload() {
  const photoInput = document.getElementById("photoInput");
  const photoArea = document.getElementById("photoUploadArea");

  if (!photoInput || !photoArea) return;

  photoInput.addEventListener("change", function () {
    if (this.files && this.files[0]) {
      uploadPhoto(this.files[0]);
    }
  });

  const previewDiv = document.getElementById("photoPreview");
  if (previewDiv) {
    previewDiv.addEventListener("click", function () {
      photoInput.click();
    });

    previewDiv.addEventListener("dragover", function (e) {
      e.preventDefault();
      previewDiv.classList.add("drag-over");
    });

    previewDiv.addEventListener("dragleave", function () {
      previewDiv.classList.remove("drag-over");
    });

    previewDiv.addEventListener("drop", function (e) {
      e.preventDefault();
      previewDiv.classList.remove("drag-over");
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        uploadPhoto(e.dataTransfer.files[0]);
      }
    });
  }
}

function uploadPhoto(file) {
  if (file.size > 5 * 1024 * 1024) {
    alert("Photo must be under 5MB.");
    return;
  }

  const allowed = ["image/png", "image/jpeg", "image/jpg"];
  if (!allowed.includes(file.type)) {
    alert("Only PNG and JPG files are allowed.");
    return;
  }

  const formData = new FormData();
  formData.append("photo", file);

  const previewDiv = document.getElementById("photoPreview");
  previewDiv.innerHTML = '<span class="photo-placeholder">Uploading...</span>';

  fetch("/upload-photo", { method: "POST", body: formData })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        resumeData.personal.photo_filename = data.filename;
        showPhotoPreview(data.url);
        updatePreview();
        autoSave();
      } else {
        alert("Upload failed: " + (data.error || "Unknown error"));
        previewDiv.innerHTML = '<span class="photo-placeholder">📷 Click or drag to upload</span>';
      }
    })
    .catch((err) => {
      console.error("Photo upload error:", err);
      alert("Failed to upload photo.");
      previewDiv.innerHTML = '<span class="photo-placeholder">📷 Click or drag to upload</span>';
    });
}

function showPhotoPreview(url) {
  const previewDiv = document.getElementById("photoPreview");
  previewDiv.innerHTML = `<img src="${url}" alt="Passport Photo" class="uploaded-photo" />`;
  document.getElementById("removePhotoBtn").style.display = "inline-block";

  const previewPhoto = document.getElementById("previewPhoto");
  const previewPhotoImg = document.getElementById("previewPhotoImg");
  if (previewPhoto && previewPhotoImg) {
    previewPhotoImg.src = url;
    previewPhoto.style.display = "block";
  }
}

function removePhoto() {
  resumeData.personal.photo_filename = "";
  const previewDiv = document.getElementById("photoPreview");
  previewDiv.innerHTML = '<span class="photo-placeholder">📷 Click or drag to upload</span>';
  document.getElementById("removePhotoBtn").style.display = "none";
  document.getElementById("photoInput").value = "";

  const previewPhoto = document.getElementById("previewPhoto");
  if (previewPhoto) previewPhoto.style.display = "none";

  updatePreview();
  autoSave();
}

function saveToDatabase() {
  if (!resumeData.personal.fullName || !resumeData.personal.email) {
    alert("Please fill in at least Full Name and Email before saving to database.");
    return;
  }

  const payload = {
    data: resumeData,
    template: currentTemplate,
  };

  const url = editingCandidateId ? `/api/candidates/${editingCandidateId}` : "/api/candidates";
  const method = editingCandidateId ? "PUT" : "POST";

  fetch(url, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const action = editingCandidateId ? "updated" : "saved";
        editingCandidateId = data.candidate.id;
        alert(`Candidate ${action} to database successfully!`);
      } else if (data.candidate_id) {
        if (confirm("A candidate with this email already exists. Update their record?")) {
          editingCandidateId = data.candidate_id;
          saveToDatabase();
        }
      } else {
        alert("Error: " + (data.error || "Unknown error"));
      }
    })
    .catch((err) => {
      console.error("Save to DB error:", err);
      alert("Failed to save to database. Is the server running with MySQL connected?");
    });
}

function addEducation() {
  const container = document.getElementById("educationContainer");
  const index = resumeData.education.length;

  const educationEntry = {
    degree: "",
    institution: "",
    location: "",
    duration: "",
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
                    <input type="text" placeholder="e.g., Maharashtra ,India " 
                           onchange="updateEducation(${index}, 'location', this.value)">
                </div>
                <div class="input-field">
                    <label>Duration</label>
                    <input type="text" placeholder="e.g., 2021 - 2024" 
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
                    <input type="text" placeholder="e.g., Banglore ,India" 
                           onchange="updateExperience(${index}, 'location', this.value)">
                </div>
                <div class="input-field">
                    <label>Duration</label>
                    <input type="text" placeholder="e.g., July 2025 - Present" 
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

function updatePreview() {
  document.getElementById("previewName").textContent = resumeData.personal.fullName || "Your Name";
  document.getElementById("previewEmail").textContent = resumeData.personal.email;
  document.getElementById("previewPhone").textContent = resumeData.personal.phone;
  document.getElementById("previewLocation").textContent = resumeData.personal.location;
  document.getElementById("previewLinkedin").textContent = resumeData.personal.linkedin;
  document.getElementById("previewSummary").textContent = resumeData.personal.summary;

  const previewPhoto = document.getElementById("previewPhoto");
  const previewPhotoImg = document.getElementById("previewPhotoImg");
  if (previewPhoto && previewPhotoImg) {
    if (resumeData.personal.photo_filename) {
      previewPhotoImg.src = `/uploads/photos/${resumeData.personal.photo_filename}`;
      previewPhoto.style.display = "block";
    } else {
      previewPhoto.style.display = "none";
    }
  }

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

  const skillsSection = document.getElementById("previewSkillsSection");
  const skillsContainer = document.getElementById("previewSkills");
  if (resumeData.skills.length > 0) {
    skillsSection.style.display = "block";
    skillsContainer.innerHTML = resumeData.skills.map((skill) => `<span class="skill-badge">${skill}</span>`).join("");
  } else {
    skillsSection.style.display = "none";
  }

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

function changeTemplate() {
  currentTemplate = document.getElementById("templateSelector").value;
  const preview = document.getElementById("resumePreview");

  preview.classList.remove(
    "template-modern",
    "template-classic",
    "template-minimal",
    "template-executive",
    "template-creative",
    "template-professional",
  );
  preview.classList.add(`template-${currentTemplate}`);

  autoSave();
}

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

      if (!resumeData.personal.photo_filename) {
        resumeData.personal.photo_filename = "";
      }

      Object.keys(resumeData.personal).forEach((key) => {
        if (key === "photo_filename") return;
        const element = document.getElementById(key);
        if (element) {
          element.value = resumeData.personal[key];
        }
      });

      if (resumeData.personal.photo_filename) {
        showPhotoPreview(`/uploads/photos/${resumeData.personal.photo_filename}`);
      }

      renderSkills();
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

function generatePDF() {
  const btn = event.target;
  const originalText = btn.textContent;
  btn.textContent = "Generating...";
  btn.disabled = true;

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
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `resume_${resumeData.personal.fullName.replace(/\s+/g, "_") || "download"}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

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
