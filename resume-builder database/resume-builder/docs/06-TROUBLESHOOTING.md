# Troubleshooting Guide 🔧

This guide helps you diagnose and fix common issues you might encounter while building or using the Resume Builder application.

## Table of Contents

1. [Setup Issues](#setup-issues)
2. [Frontend Issues](#frontend-issues)
3. [Backend Issues](#backend-issues)
4. [PDF Generation Issues](#pdf-generation-issues)
5. [Browser Issues](#browser-issues)
6. [Common Error Messages](#common-error-messages)

---

## Setup Issues

### Python Not Found

**Error**:

```
'python' is not recognized as an internal or external command
```

**Solutions**:

1. **Reinstall Python with PATH**
   - Download from python.org
   - ✅ Check "Add Python to PATH"
   - Complete installation

2. **Manually Add to PATH (Windows)**

   ```
   Control Panel → System → Advanced → Environment Variables
   Add: C:\Python311 and C:\Python311\Scripts
   ```

3. **Use Python Launcher**
   ```bash
   py --version
   py -m pip install -r requirements.txt
   ```

---

### pip Not Found

**Error**:

```
'pip' is not recognized as an internal or external command
```

**Solutions**:

1. **Install pip**

   ```bash
   python -m ensurepip --upgrade
   ```

2. **Use python -m pip**

   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Reinstall Python**
   - Download latest version
   - Ensure pip is included

---

### Virtual Environment Issues

**Error**:

```
venv\Scripts\activate : cannot be loaded because running scripts is disabled
```

**Solution (Windows PowerShell)**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Alternative**: Use Command Prompt instead

```cmd
venv\Scripts\activate.bat
```

---

### Dependency Installation Fails

**Error**:

```
ERROR: Could not find a version that satisfies the requirement Flask==3.0.0
```

**Solutions**:

1. **Update pip**

   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install without version constraints**

   ```bash
   pip install Flask Flask-CORS reportlab Pillow
   ```

3. **Check Python version**

   ```bash
   python --version
   # Should be 3.8 or higher
   ```

4. **Use compatible versions**
   ```txt
   Flask>=2.0.0
   Flask-CORS>=3.0.0
   reportlab>=3.6.0
   Pillow>=9.0.0
   ```

---

### Port Already in Use

**Error**:

```
OSError: [Errno 48] Address already in use
```

**Solutions**:

1. **Find and kill process (Windows)**

   ```bash
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Find and kill process (macOS/Linux)**

   ```bash
   lsof -i :5000
   kill -9 <PID>
   ```

3. **Use different port**
   ```python
   # In app.py
   app.run(debug=True, port=5001)
   ```

---

## Frontend Issues

### Preview Not Updating

**Symptoms**: Typing in form doesn't update preview

**Diagnosis**:

1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check if JavaScript file is loaded

**Solutions**:

1. **Check JavaScript file path**

   ```html
   <!-- In index.html -->
   <script src="{{ url_for('static', filename='js/app.js') }}"></script>
   ```

2. **Verify event listeners**

   ```javascript
   // In app.js
   console.log("Script loaded");

   document.addEventListener("DOMContentLoaded", function () {
     console.log("DOM loaded");
     setupEventListeners();
   });
   ```

3. **Check for JavaScript errors**
   - Look for red errors in Console
   - Fix syntax errors
   - Ensure all functions are defined

4. **Hard refresh browser**
   - Windows/Linux: Ctrl + Shift + R
   - macOS: Cmd + Shift + R

---

### Buttons Not Working

**Symptoms**: Clicking buttons does nothing

**Solutions**:

1. **Check onclick handlers**

   ```html
   <!-- Correct -->
   <button onclick="addEducation()">Add</button>

   <!-- Wrong -->
   <button onclick="addEducation">Add</button>
   ```

2. **Verify function exists**

   ```javascript
   // In browser console
   typeof addEducation;
   // Should return "function"
   ```

3. **Check for errors**
   ```javascript
   // Add error handling
   function addEducation() {
     try {
       // Function code
     } catch (error) {
       console.error("Error in addEducation:", error);
     }
   }
   ```

---

### LocalStorage Not Working

**Symptoms**: Data doesn't persist after refresh

**Solutions**:

1. **Check browser privacy settings**
   - Disable "Block third-party cookies"
   - Allow site data

2. **Check incognito/private mode**
   - LocalStorage disabled in private browsing
   - Use regular browser window

3. **Check storage quota**

   ```javascript
   // In browser console
   console.log(localStorage.length);
   console.log(JSON.stringify(localStorage).length);
   ```

4. **Clear and retry**
   ```javascript
   localStorage.clear();
   location.reload();
   ```

---

### CSS Not Loading

**Symptoms**: Page looks unstyled

**Solutions**:

1. **Check file path**

   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
   ```

2. **Verify file exists**

   ```
   static/
   └── css/
       └── style.css
   ```

3. **Check Flask static folder**

   ```python
   # In app.py
   app = Flask(__name__, static_folder='static')
   ```

4. **Hard refresh**
   - Ctrl + Shift + R (Windows/Linux)
   - Cmd + Shift + R (macOS)

---

### Responsive Design Issues

**Symptoms**: Layout broken on mobile

**Solutions**:

1. **Check viewport meta tag**

   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   ```

2. **Test media queries**

   ```css
   /* Add temporary border to test */
   @media (max-width: 768px) {
     body {
       border: 5px solid red;
     }
   }
   ```

3. **Use browser DevTools**
   - Press F12
   - Click device icon (Ctrl + Shift + M)
   - Test different screen sizes

---

## Backend Issues

### Flask Server Won't Start

**Error**:

```
ModuleNotFoundError: No module named 'flask'
```

**Solutions**:

1. **Activate virtual environment**

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install Flask**

   ```bash
   pip install Flask
   ```

3. **Check Python path**
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

---

### Template Not Found

**Error**:

```
jinja2.exceptions.TemplateNotFound: index.html
```

**Solutions**:

1. **Check folder structure**

   ```
   project/
   ├── app.py
   └── templates/
       └── index.html
   ```

2. **Verify template folder**

   ```python
   # In app.py
   app = Flask(__name__, template_folder='templates')
   ```

3. **Check file name**
   - Must be exactly `index.html`
   - Case-sensitive on Linux/macOS

---

### CORS Errors

**Error** (in browser console):

```
Access to fetch has been blocked by CORS policy
```

**Solutions**:

1. **Install Flask-CORS**

   ```bash
   pip install Flask-CORS
   ```

2. **Enable CORS**

   ```python
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app)
   ```

3. **Configure specific origins**
   ```python
   CORS(app, resources={
       r"/generate-pdf": {"origins": "http://localhost:5000"}
   })
   ```

---

### 404 Not Found

**Error**:

```
404 Not Found: The requested URL was not found
```

**Solutions**:

1. **Check route definition**

   ```python
   @app.route('/generate-pdf', methods=['POST'])
   def generate_pdf():
       # ...
   ```

2. **Verify URL in frontend**

   ```javascript
   fetch('/generate-pdf', {  // Correct
   fetch('generate-pdf', {   // Wrong - missing /
   ```

3. **Check Flask logs**
   - Look in terminal where Flask is running
   - See which routes are registered

---

## PDF Generation Issues

### PDF Not Generating

**Error**:

```
500 Internal Server Error
```

**Diagnosis**:

1. Check Flask terminal for error details
2. Look for Python traceback

**Solutions**:

1. **Check ReportLab installation**

   ```bash
   pip list | grep reportlab
   pip install --upgrade reportlab
   ```

2. **Add error logging**

   ```python
   @app.route('/generate-pdf', methods=['POST'])
   def generate_pdf():
       try:
           # PDF generation code
       except Exception as e:
           print(f"Error: {str(e)}")
           import traceback
           traceback.print_exc()
           return jsonify({'error': str(e)}), 500
   ```

3. **Test with minimal data**
   ```python
   # Test with simple data
   test_data = {
       'personal': {'fullName': 'Test User', 'email': 'test@test.com'},
       'education': [],
       'experience': [],
       'skills': [],
       'projects': []
   }
   ```

---

### PDF Contains Wrong Data

**Symptoms**: Generated PDF doesn't match form input

**Solutions**:

1. **Check data being sent**

   ```javascript
   // In app.js, before fetch
   console.log("Sending data:", resumeData);
   ```

2. **Check data received**

   ```python
   # In app.py
   @app.route('/generate-pdf', methods=['POST'])
   def generate_pdf():
       data = request.json
       print('Received data:', data)
   ```

3. **Verify JSON serialization**
   ```javascript
   // Ensure data is properly structured
   const payload = {
     data: resumeData,
     template: currentTemplate,
   };
   console.log(JSON.stringify(payload));
   ```

---

### PDF Formatting Issues

**Symptoms**: PDF looks wrong, text overlaps, spacing off

**Solutions**:

1. **Check style definitions**

   ```python
   # Verify fontSize, spaceAfter, etc.
   ParagraphStyle(
       name='CustomStyle',
       fontSize=12,  # Not too large
       spaceAfter=6,  # Adequate spacing
   )
   ```

2. **Add more spacing**

   ```python
   story.append(Spacer(1, 0.2*inch))
   ```

3. **Test with shorter text**
   - Long text might overflow
   - Use shorter descriptions

4. **Check page margins**
   ```python
   doc = SimpleDocTemplate(
       buffer,
       pagesize=letter,
       rightMargin=0.75*inch,
       leftMargin=0.75*inch,
       topMargin=0.75*inch,
       bottomMargin=0.75*inch
   )
   ```

---

### PDF Download Fails

**Symptoms**: Click download but nothing happens

**Solutions**:

1. **Check browser console**
   - Look for fetch errors
   - Check network tab

2. **Verify response type**

   ```javascript
   fetch("/generate-pdf", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify(data),
   }).then((response) => {
     console.log("Response status:", response.status);
     console.log("Response type:", response.headers.get("content-type"));
     return response.blob();
   });
   ```

3. **Check popup blocker**
   - Browser might block download
   - Allow popups for localhost

4. **Test direct endpoint**
   - Use Postman or curl
   - Verify PDF is generated

---

## Browser Issues

### Console Errors

**Common Errors and Solutions**:

#### Uncaught ReferenceError: function is not defined

```javascript
// Solution: Ensure function is defined before use
function myFunction() {
  // code
}

// Or move script to end of body
<script src="app.js" defer></script>;
```

#### Uncaught TypeError: Cannot read property of undefined

```javascript
// Solution: Check if element exists
const element = document.getElementById("myId");
if (element) {
  element.value = "test";
}
```

#### Failed to fetch

```javascript
// Solution: Check server is running and URL is correct
fetch("/generate-pdf").catch((error) => {
  console.error("Fetch error:", error);
  alert("Server not responding. Is it running?");
});
```

---

### Browser Compatibility

**Issue**: Works in Chrome but not Firefox/Safari

**Solutions**:

1. **Check JavaScript compatibility**
   - Avoid very new features
   - Use polyfills if needed

2. **Test CSS compatibility**
   - Use vendor prefixes
   - Test flexbox/grid support

3. **Check fetch API**
   ```javascript
   // Add polyfill for older browsers
   if (!window.fetch) {
     console.error("Fetch API not supported");
   }
   ```

---

### Performance Issues

**Symptoms**: App is slow, laggy input

**Solutions**:

1. **Debounce input events**

   ```javascript
   let timeout;
   element.addEventListener("input", function () {
     clearTimeout(timeout);
     timeout = setTimeout(() => {
       updatePreview();
     }, 300); // Wait 300ms after typing stops
   });
   ```

2. **Optimize DOM updates**

   ```javascript
   // Bad: Multiple updates
   for (let item of items) {
     container.innerHTML += `<div>${item}</div>`;
   }

   // Good: Single update
   const html = items.map((item) => `<div>${item}</div>`).join("");
   container.innerHTML = html;
   ```

3. **Reduce preview updates**
   - Only update changed sections
   - Use requestAnimationFrame

---

## Common Error Messages

### "Cannot POST /generate-pdf"

**Cause**: Route not defined or wrong method

**Solution**:

```python
# Ensure route exists with POST method
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # ...
```

---

### "JSON decode error"

**Cause**: Invalid JSON sent to server

**Solution**:

```javascript
// Ensure proper JSON formatting
fetch("/generate-pdf", {
  method: "POST",
  headers: {
    "Content-Type": "application/json", // Important!
  },
  body: JSON.stringify(data), // Must stringify
});
```

---

### "Maximum call stack size exceeded"

**Cause**: Infinite recursion or loop

**Solution**:

```javascript
// Check for circular references
function updatePreview() {
  // Don't call updatePreview() inside itself
  // unless there's a proper exit condition
}
```

---

### "QuotaExceededError"

**Cause**: LocalStorage full

**Solution**:

```javascript
try {
  localStorage.setItem("resumeData", JSON.stringify(data));
} catch (e) {
  if (e.name === "QuotaExceededError") {
    alert("Storage full. Please clear old data.");
    // Optionally clear old data
    localStorage.clear();
  }
}
```

---

## Debugging Tips

### Enable Debug Mode

**Flask**:

```python
app.run(debug=True)  # Shows detailed errors
```

**JavaScript**:

```javascript
// Add console.log statements
console.log("Variable value:", myVar);
console.table(resumeData); // Nice table format
```

---

### Use Browser DevTools

**Console Tab**:

- View errors and logs
- Test JavaScript code
- Inspect variables

**Network Tab**:

- See all requests
- Check request/response data
- Verify status codes

**Elements Tab**:

- Inspect HTML structure
- View applied CSS
- Test CSS changes live

**Application Tab**:

- View LocalStorage
- Clear storage
- Check cookies

---

### Check File Paths

**Common mistakes**:

```
Wrong: /static/css/style.css
Right: {{ url_for('static', filename='css/style.css') }}

Wrong: static\css\style.css  (Windows path)
Right: static/css/style.css  (Web path)
```

---

### Verify Data Flow

**Add logging at each step**:

```javascript
// 1. Form input
console.log("1. Input changed:", value);

// 2. Data update
console.log("2. Data updated:", resumeData);

// 3. Preview update
console.log("3. Updating preview");

// 4. Storage save
console.log("4. Saved to storage");
```

---

## Getting Help

### Before Asking for Help

1. **Check error message carefully**
   - Read the full error
   - Note the line number
   - Understand what it says

2. **Search for the error**
   - Google the exact error message
   - Check Stack Overflow
   - Read documentation

3. **Try to isolate the problem**
   - What were you doing when it broke?
   - Does it happen consistently?
   - What changed recently?

4. **Gather information**
   - Python version
   - Browser and version
   - Operating system
   - Full error message
   - Steps to reproduce

---

### Where to Get Help

1. **Documentation**
   - Flask: flask.palletsprojects.com
   - ReportLab: reportlab.com/docs
   - MDN Web Docs: developer.mozilla.org

2. **Community**
   - Stack Overflow
   - Reddit: r/flask, r/learnprogramming
   - Discord: Python, Web Dev servers

3. **GitHub Issues**
   - Check if others had same issue
   - Create new issue with details

---

## Prevention Tips

1. **Test frequently**
   - Test after each feature
   - Don't wait until the end

2. **Use version control**
   - Git for tracking changes
   - Easy to revert mistakes

3. **Read error messages**
   - They usually tell you what's wrong
   - Don't ignore warnings

4. **Keep backups**
   - Save working versions
   - Export data regularly

5. **Follow best practices**
   - Use consistent naming
   - Comment your code
   - Keep functions small

---

## Quick Reference

### Restart Everything

```bash
# 1. Stop Flask server (Ctrl+C)

# 2. Deactivate virtual environment
deactivate

# 3. Reactivate
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 4. Reinstall dependencies
pip install -r requirements.txt

# 5. Restart server
python app.py

# 6. Hard refresh browser
Ctrl + Shift + R
```

### Clear Everything

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Clear browser data
# In browser: Ctrl+Shift+Delete

# Clear LocalStorage
# In console: localStorage.clear()
```

---

**Still stuck?** Review the code carefully, check the documentation guides, and don't hesitate to search for specific error messages online.
