let currentPage = 1;
let currentCandidateId = null;

document.addEventListener("DOMContentLoaded", function () {
  loadCandidates();

  document.getElementById("searchInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      searchCandidates();
    }
  });

  document.getElementById("locationFilter").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      applyFilters();
    }
  });

  document.getElementById("skillFilter").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      applyFilters();
    }
  });
});

function loadCandidates(page) {
  if (page) currentPage = page;

  const search = document.getElementById("searchInput").value.trim();
  const sortBy = document.getElementById("sortBy").value;
  const sortOrder = document.getElementById("sortOrder").value;
  const location = document.getElementById("locationFilter").value.trim();
  const skill = document.getElementById("skillFilter").value.trim();

  const params = new URLSearchParams({
    page: currentPage,
    per_page: 20,
    sort_by: sortBy,
    sort_order: sortOrder,
  });

  if (search) params.append("search", search);
  if (location) params.append("location", location);
  if (skill) params.append("skill", skill);

  fetch(`/api/candidates?${params.toString()}`)
    .then((res) => res.json())
    .then((data) => {
      renderCandidates(data.candidates);
      renderPagination(data.total, data.pages, data.current_page);
      document.getElementById("totalCount").textContent = `Total: ${data.total} candidate(s)`;
    })
    .catch((err) => {
      console.error("Error loading candidates:", err);
      document.getElementById("candidatesBody").innerHTML =
        '<tr><td colspan="9" class="loading-cell">Failed to load candidates. Is the database connected?</td></tr>';
      document.getElementById("totalCount").textContent = "Error loading data";
    });
}

function renderCandidates(candidates) {
  const tbody = document.getElementById("candidatesBody");

  if (!candidates || candidates.length === 0) {
    tbody.innerHTML = '<tr><td colspan="9" class="loading-cell">No candidates found.</td></tr>';
    return;
  }

  tbody.innerHTML = candidates
    .map(
      (c) => `
    <tr onclick="viewCandidate(${c.id})" class="candidate-row">
      <td>
        ${
          c.photo_filename
            ? `<img src="/uploads/photos/${c.photo_filename}" class="table-photo" alt="Photo" />`
            : '<span class="no-photo">—</span>'
        }
      </td>
      <td class="name-cell">${escapeHtml(c.full_name)}</td>
      <td>${escapeHtml(c.email)}</td>
      <td>${escapeHtml(c.phone || "—")}</td>
      <td>${escapeHtml(c.location || "—")}</td>
      <td class="skills-cell">
        ${
          c.skills && c.skills.length > 0
            ? c.skills
                .slice(0, 3)
                .map((s) => `<span class="skill-badge-sm">${escapeHtml(s)}</span>`)
                .join("") + (c.skills.length > 3 ? `<span class="skill-badge-sm more">+${c.skills.length - 3}</span>` : "")
            : "—"
        }
      </td>
      <td><span class="template-badge template-${c.template}">${c.template}</span></td>
      <td>${formatDate(c.created_at)}</td>
      <td class="actions-cell">
        <button class="btn-sm btn-view" onclick="event.stopPropagation(); viewCandidate(${c.id})">View</button>
        </<td>
    </tr>
  `,
    )
    .join("");
}

function renderPagination(total, pages, current) {
  const container = document.getElementById("pagination");
  if (pages <= 1) {
    container.innerHTML = "";
    return;
  }

  let html = "";
  if (current > 1) {
    html += `<button class="btn-page" onclick="loadCandidates(${current - 1})">Prev</button>`;
  }

  for (let i = 1; i <= pages; i++) {
    if (i === current) {
      html += `<button class="btn-page active">${i}</button>`;
    } else if (i <= 3 || i >= pages - 2 || Math.abs(i - current) <= 1) {
      html += `<button class="btn-page" onclick="loadCandidates(${i})">${i}</button>`;
    } else if (i === 4 && current > 5) {
      html += `<span class="page-dots">...</span>`;
    } else if (i === pages - 3 && current < pages - 4) {
      html += `<span class="page-dots">...</span>`;
    }
  }

  if (current < pages) {
    html += `<button class="btn-page" onclick="loadCandidates(${current + 1})">Next</button>`;
  }

  container.innerHTML = html;
}

function searchCandidates() {
  currentPage = 1;
  loadCandidates();
}

function applyFilters() {
  currentPage = 1;
  loadCandidates();
}

function clearFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("locationFilter").value = "";
  document.getElementById("skillFilter").value = "";
  document.getElementById("sortBy").value = "created_at";
  document.getElementById("sortOrder").value = "desc";
  currentPage = 1;
  loadCandidates();
}

function viewCandidate(id) {
  currentCandidateId = id;
  fetch(`/api/candidates/${id}`)
    .then((res) => res.json())
    .then((data) => {
      const c = data.candidate;
      document.getElementById("modalTitle").textContent = c.full_name;

      let html = '<div class="modal-candidate">';

      if (c.photo_filename) {
        html += `<div class="modal-photo"><img src="/uploads/photos/${c.photo_filename}" alt="Photo" /></div>`;
      }

      html += `
        <div class="modal-info">
          <div class="modal-row"><strong>Email:</strong> ${escapeHtml(c.email)}</div>
          <div class="modal-row"><strong>Phone:</strong> ${escapeHtml(c.phone || "N/A")}</div>
          <div class="modal-row"><strong>Location:</strong> ${escapeHtml(c.location || "N/A")}</div>
          <div class="modal-row"><strong>LinkedIn:</strong> ${escapeHtml(c.linkedin || "N/A")}</div>
          <div class="modal-row"><strong>Template:</strong> <span class="template-badge template-${c.template}">${c.template}</span></div>
        </div>
      `;

      if (c.summary) {
        html += `<div class="modal-section"><h3>Summary</h3><p>${escapeHtml(c.summary)}</p></div>`;
      }

      if (c.education && c.education.length > 0) {
        html += '<div class="modal-section"><h3>Education</h3>';
        c.education.forEach((edu) => {
          if (edu.degree || edu.institution) {
            html += `<div class="modal-item"><strong>${escapeHtml(edu.degree || "")}</strong>`;
            if (edu.institution) html += ` — ${escapeHtml(edu.institution)}`;
            if (edu.duration) html += ` (${escapeHtml(edu.duration)})`;
            html += "</div>";
          }
        });
        html += "</div>";
      }

      if (c.experience && c.experience.length > 0) {
        html += '<div class="modal-section"><h3>Experience</h3>';
        c.experience.forEach((exp) => {
          if (exp.title || exp.company) {
            html += `<div class="modal-item"><strong>${escapeHtml(exp.title || "")}</strong>`;
            if (exp.company) html += ` at ${escapeHtml(exp.company)}`;
            if (exp.duration) html += ` (${escapeHtml(exp.duration)})`;
            html += "</div>";
          }
        });
        html += "</div>";
      }

      if (c.skills && c.skills.length > 0) {
        html += '<div class="modal-section"><h3>Skills</h3><div class="modal-skills">';
        c.skills.forEach((s) => {
          html += `<span class="skill-badge">${escapeHtml(s)}</span>`;
        });
        html += "</div></div>";
      }

      if (c.projects && c.projects.length > 0) {
        html += '<div class="modal-section"><h3>Projects</h3>';
        c.projects.forEach((proj) => {
          if (proj.name) {
            html += `<div class="modal-item"><strong>${escapeHtml(proj.name)}</strong>`;
            if (proj.technologies) html += ` — ${escapeHtml(proj.technologies)}`;
            html += "</div>";
          }
        });
        html += "</div>";
      }

      html += `<div class="modal-meta">Added: ${formatDate(c.created_at)} | Updated: ${formatDate(c.updated_at)}</div>`;
      html += "</div>";

      document.getElementById("modalBody").innerHTML = html;
      document.getElementById("candidateModal").style.display = "flex";
    })
    .catch((err) => {
      console.error("Error loading candidate:", err);
      alert("Failed to load candidate details.");
    });
}

function closeModal() {
  document.getElementById("candidateModal").style.display = "none";
  currentCandidateId = null;
}

function editCandidate() {
  if (!currentCandidateId) return;
  fetch(`/api/candidates/${currentCandidateId}`)
    .then((res) => res.json())
    .then((data) => {
      const c = data.candidate;
      const resumeData = {
        personal: {
          fullName: c.full_name,
          email: c.email,
          phone: c.phone || "",
          location: c.location || "",
          linkedin: c.linkedin || "",
          summary: c.summary || "",
          photo_filename: c.photo_filename || "",
        },
        education: c.education || [],
        experience: c.experience || [],
        skills: c.skills || [],
        projects: c.projects || [],
      };
      localStorage.setItem("resumeData", JSON.stringify(resumeData));
      localStorage.setItem("currentTemplate", c.template || "modern");
      localStorage.setItem("editingCandidateId", currentCandidateId);
      window.location.href = "/";
    })
    .catch((err) => {
      console.error("Error:", err);
      alert("Failed to load candidate for editing.");
    });
}

function deleteCandidate(id, name) {
  if (!confirm(`Are you sure you want to delete "${name}"? This cannot be undone.`)) return;

  fetch(`/api/candidates/${id}`, { method: "DELETE" })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        loadCandidates();
        if (currentCandidateId === id) closeModal();
      } else {
        alert("Failed to delete: " + (data.error || "Unknown error"));
      }
    })
    .catch((err) => {
      console.error("Error deleting:", err);
      alert("Failed to delete candidate.");
    });
}

function deleteCurrentCandidate() {
  if (currentCandidateId) {
    const name = document.getElementById("modalTitle").textContent;
    deleteCandidate(currentCandidateId, name);
  }
}

function escapeHtml(str) {
  if (!str) return "";
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function formatDate(isoStr) {
  if (!isoStr) return "—";
  const d = new Date(isoStr);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}
