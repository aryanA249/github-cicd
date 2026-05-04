# Security Vulnerabilities in Sample App

This document explains each vulnerability in `app.py` and why it's a security risk.

---

## 🚨 Vulnerability #1: Hardcoded Credentials

**Location**: `app.py`, lines 12-14

```python
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-12345abcde"
SECRET_TOKEN = "supersecret_token_12345"
```

### Risk Level: 🔴 CRITICAL

### Why It's Dangerous

- Credentials in source code are visible to anyone with repository access
- Exposed in git history permanently (even after deletion)
- Anyone can impersonate the application or access databases
- No way to rotate credentials without code changes

### Bandit Detection

```
[B105:hardcoded_password_string] Possible hardcoded password: 'admin123'
Severity: HIGH
```

### ✅ Fix

```python
# Use environment variables or secrets management
import os
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')

# Or use GitHub Secrets in the workflow
# env:
#   DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

---

## 🚨 Vulnerability #2: Information Disclosure

**Location**: `app.py`, line 27

```python
@app.route("/")
def home():
    return {
        "message": "Welcome to Vulnerable App",
        "password": DATABASE_PASSWORD,  # ⚠️ Exposing password
        "api_key": API_KEY
    }
```

### Risk Level: 🔴 CRITICAL

### Why It's Dangerous

- Sensitive information leaked via API responses
- Attackers can harvest credentials by making simple HTTP requests
- Visible in browser console, logs, monitoring systems

### Fix

```python
@app.route("/")
def home():
    return {
        "message": "Welcome to Secure App",
        # Don't expose credentials!
    }
```

---

## 🚨 Vulnerability #3: Command Injection

**Location**: `app.py`, lines 31-36

```python
@app.route("/execute", methods=["POST"])
def execute_command():
    command = request.json.get("cmd")
    result = subprocess.run(command, shell=True, capture_output=True)
    return {"output": result.stdout.decode()}
```

### Risk Level: 🔴 CRITICAL

### Why It's Dangerous

- `shell=True` interprets shell metacharacters
- User input directly becomes shell commands
- Attacker can execute arbitrary code on the server
- Full system compromise possible

### Attack Example

```bash
POST /execute
{"cmd": "rm -rf /; echo 'hacked'"}
```

### Bandit Detection

```
[B602:shell_injection] A shell=True parameter was used with subprocess.
Severity: HIGH
```

### ✅ Fix

```python
import shlex

@app.route("/execute", methods=["POST"])
def execute_command():
    command = request.json.get("cmd")
    
    # Use shell=False and pass args as list
    result = subprocess.run(
        shlex.split(command),  # Parse safely
        shell=False,           # Don't use shell
        capture_output=True
    )
    return {"output": result.stdout.decode()}
```

---

## 🚨 Vulnerability #4: Insecure Deserialization

**Location**: `app.py`, lines 39-46

```python
@app.route("/deserialize", methods=["POST"])
def deserialize_data():
    data = request.json.get("payload")
    obj = pickle.loads(data)  # ⚠️ DANGEROUS
    return {"result": obj}
```

### Risk Level: 🔴 CRITICAL

### Why It's Dangerous

- `pickle.loads()` executes arbitrary Python code during deserialization
- Attackers can craft malicious pickle objects
- Remote Code Execution (RCE) possible
- One of Python's most dangerous functions

### Attack Example

```python
import pickle
import os

class Exploit:
    def __reduce__(self):
        return (os.system, ("rm -rf /",))

malicious = pickle.dumps(Exploit())
# Sends malicious to /deserialize endpoint
```

### Bandit Detection

```
[B301:pickle] Pickle can be dangerous. Only load data you trust.
Severity: HIGH
```

### ✅ Fix

```python
import json

@app.route("/deserialize", methods=["POST"])
def deserialize_data():
    data = request.json.get("payload")
    
    # Use JSON (safe) instead of pickle
    obj = json.loads(data)
    return {"result": obj}
```

---

## 🚨 Vulnerability #5: Debug Mode Enabled

**Location**: `app.py`, line 57

```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

### Risk Level: 🟠 HIGH

### Why It's Dangerous

- **Debugger accessible**: Attacker can use the interactive Python console
- **Stack traces exposed**: Reveals source code and internal structure
- **Auto-reload on code changes**: Risks unstable state
- **Never use in production**

### Information Exposed

```
- Source code
- Variable values
- System paths
- Framework version
- Server configuration
```

### Bandit Detection

```
[B201:flask_debug_true] Flask debug mode set to True.
Severity: MEDIUM
```

### ✅ Fix

```python
if __name__ == "__main__":
    # Read debug mode from environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        debug=debug_mode,           # False in production
        host="127.0.0.1",          # Localhost, not all interfaces
        port=5000
    )
```

---

## 🚨 Vulnerability #6: Insecure Host Binding

**Location**: `app.py`, line 57

```python
app.run(debug=True, host="0.0.0.0", port=5000)
```

### Risk Level: 🟠 HIGH

### Why It's Dangerous

- `0.0.0.0` means "listen on all network interfaces"
- Makes app accessible from external networks
- Increases attack surface
- Should only bind to localhost in development

### ✅ Fix

```python
# Development: bind to localhost only
app.run(host="127.0.0.1")

# Production: use reverse proxy (Nginx) to control exposure
```

---

## 🔍 How Bandit Detects These Issues

Bandit uses pattern matching to identify:
- Hardcoded strings that look like passwords
- Dangerous function calls (`pickle.loads`, `subprocess.run` with `shell=True`)
- Insecure Flask configurations
- Debug mode in code

### Run Bandit Yourself

```bash
# Install Bandit
pip install bandit

# Scan the app
bandit app.py

# Get more details
bandit app.py -v

# Only show HIGH severity
bandit app.py -ll
```

---

## 📋 Summary Table

| Vulnerability | Severity | Type | Fix |
|---|---|---|---|
| Hardcoded Credentials | 🔴 CRITICAL | Configuration | Use environment variables |
| Information Disclosure | 🔴 CRITICAL | Logic | Don't expose secrets in responses |
| Command Injection | 🔴 CRITICAL | Input Validation | Use `shell=False`, sanitize input |
| Insecure Deserialization | 🔴 CRITICAL | Deserialization | Use JSON instead of pickle |
| Debug Mode | 🟠 HIGH | Configuration | Disable in production |
| Insecure Binding | 🟠 HIGH | Configuration | Bind to localhost |

---

## 🎓 Learning Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

---

## ✅ Secure Code Example

Here's how to fix the vulnerable app:

```python
import os
from flask import Flask, request
import json

app = Flask(__name__)

# ✅ Load credentials from environment (not hardcoded)
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
API_KEY = os.environ.get('API_KEY')

@app.route("/")
def home():
    """✅ Don't expose sensitive data"""
    return {"message": "Welcome to Secure App"}

@app.route("/api/data", methods=["GET"])
def get_data():
    """✅ Safe endpoint that doesn't leak secrets"""
    return {"data": "public information only"}

if __name__ == "__main__":
    # ✅ Debug mode disabled, binds to localhost only
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(
        debug=debug_mode,
        host="127.0.0.1",  # Localhost only
        port=5000
    )
```

---

**Remember**: Security is everyone's responsibility! Always:
- Keep credentials out of source code
- Validate and sanitize user input
- Use HTTPS in production
- Keep dependencies updated
- Run security scans regularly
