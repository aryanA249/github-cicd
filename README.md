# 🔐 Secure CI/CD Pipeline with GitHub Actions

A professional, production-ready DevSecOps project demonstrating security vulnerability scanning integrated into a GitHub Actions CI/CD pipeline.

---

## 📋 Project Overview

This project showcases **Shift-Left Security** — integrating security checks early in the development process through automated CI/CD pipelines. The pipeline automatically scans code for vulnerabilities when changes are pushed, preventing insecure code from reaching production.

### 🎯 Key Features

- ✅ **Automated Security Scanning**: Runs Bandit (Python SAST tool) on every push
- ✅ **Fail-Safe Pipeline**: Blocks deployment if high-severity vulnerabilities are detected
- ✅ **Detailed Reporting**: Generates JSON and text reports with vulnerability details
- ✅ **DevSecOps Best Practices**: Demonstrates industry-standard security workflows
- ✅ **Beginner-Friendly**: Simple, well-commented code and workflows
- ✅ **Production-Ready**: Includes concurrency controls and proper error handling

---

## 📁 Project Structure

```
secure-cicd/
│
├── README.md                    # This file
├── app.py                       # Sample vulnerable Python Flask app
├── requirements.txt             # Python dependencies
│
└── .github/
    └── workflows/
        └── pipeline.yml         # GitHub Actions workflow (CI/CD pipeline)
```

---

## 🚀 Quick Start

### 1. Prerequisites

- GitHub account
- GitHub repository (public or private)
- Git installed locally

### 2. Setup Instructions

#### Step 1: Create a GitHub Repository

```bash
# On GitHub, create a new repository named "secure-cicd"
# (or clone this repository)
```

#### Step 2: Clone or Initialize Repository Locally

```bash
# Option A: Clone if already created on GitHub
git clone https://github.com/<YOUR_USERNAME>/secure-cicd.git
cd secure-cicd

# Option B: Initialize locally and push to GitHub
git init
git remote add origin https://github.com/<YOUR_USERNAME>/secure-cicd.git
```

#### Step 3: Add Files to Repository

Copy the following files to your repository:

- `app.py`
- `requirements.txt`
- `.github/workflows/pipeline.yml`

#### Step 4: Push to GitHub

```bash
git add .
git commit -m "Initial commit: Add secure CI/CD pipeline"
git branch -M main
git push -u origin main
```

#### Step 5: Verify GitHub Actions

1. Go to your GitHub repository
2. Click on the **"Actions"** tab
3. You should see the workflow running
4. Check the logs to see security scan results

---

## 📝 File Descriptions

### 1. `app.py` - Vulnerable Sample Application

A Flask web application **intentionally containing security vulnerabilities** for demonstration purposes:

**Vulnerabilities Included:**
- ⚠️ **Hardcoded Credentials**: Database password and API keys exposed in source code
- ⚠️ **Command Injection**: `subprocess.run()` with `shell=True` and user input
- ⚠️ **Insecure Deserialization**: Using `pickle.loads()` on untrusted data
- ⚠️ **Debug Mode**: Flask running with `debug=True` in production-like environment
- ⚠️ **Insecure Binding**: App bound to `0.0.0.0` (all interfaces)
- ⚠️ **Information Disclosure**: API endpoints exposing sensitive information

**Purpose**: Demonstrate what NOT to do, and show how Bandit detects these issues.

### 2. `requirements.txt` - Python Dependencies

Specifies Python packages required by the application:

```
Flask==2.3.2        # Web framework
Werkzeug==2.3.6     # WSGI utilities
```

### 3. `.github/workflows/pipeline.yml` - GitHub Actions Workflow

The main CI/CD pipeline configuration with two jobs:

#### **Job 1: Security Scan** (`security-scan`)

Steps:
1. **Checkout code** - Get repository code
2. **Setup Python 3.10** - Configure Python environment
3. **Display Python version** - Verify setup
4. **Install Bandit** - Install security scanner
5. **Full Bandit scan** - Report all vulnerabilities
6. **Strict Bandit scan** - Fail on high-severity issues
7. **Parse results** - Generate human-readable report
8. **Upload report** - Store as GitHub Actions artifact
9. **Check for critical issues** - Fail build if needed
10. **Success message** - Confirm all checks passed

#### **Job 2: Dependencies Check** (`dependencies-check`)

Additional checks for Python dependencies:
- Verify `requirements.txt` exists
- Check for outdated/vulnerable packages using `pip-audit`

**Key Configuration:**
- **Trigger**: Runs on push to `main` and `develop` branches, and on PRs to `main`
- **Concurrency**: Prevents duplicate workflow runs
- **Continue-on-error**: Some steps don't block pipeline (informational only)
- **Artifacts**: Generates downloadable security reports

---

## 🔍 Understanding Bandit

### What is Bandit?

**Bandit** is a Python Static Application Security Testing (SAST) tool that scans code for common security issues.

### How It Works

```bash
# Run full scan (reports all issues)
bandit -r .

# Run strict scan (fails on HIGH severity)
bandit -r . -ll

# Generate JSON report
bandit -r . -f json -o report.json
```

### Severity Levels

- 🔴 **HIGH**: Critical security issues (e.g., hardcoded passwords)
- 🟠 **MEDIUM**: Significant concerns (e.g., weak cryptography)
- 🟡 **LOW**: Minor issues (e.g., debug mode enabled)

---

## 🧪 Testing the Pipeline

### Test Locally (Optional)

Install and run Bandit on your machine:

```bash
# Install Bandit
pip install bandit

# Run scan on current directory
bandit -r .

# Run with strict settings
bandit -r . -ll -v
```

### Expected Output

When Bandit scans the vulnerable `app.py`, it should detect:

```
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password
   Severity: HIGH   Confidence: MEDIUM
   Location: app.py, line 12

>> Issue: [B602:shell_injection] A shell=True parameter was used with subprocess
   Severity: HIGH   Confidence: HIGH
   Location: app.py, line 33
   
... (more issues)
```

### GitHub Actions Execution

After pushing to GitHub:

1. Go to **Actions** tab in your repository
2. Click on the workflow run
3. Expand **"Security Scan"** job to see detailed logs
4. Check **Artifacts** section to download the `bandit-security-report.json`
5. Pipeline will **fail** due to detected vulnerabilities (as intended)

---

## 🛠️ Customization

### Modify Bandit Strictness

In `pipeline.yml`, change the Bandit severity level:

```yaml
# Current: Fails on HIGH and above (-ll)
bandit -r . -ll

# Alternative options:
# -lll     : Only CRITICAL issues (most lenient)
# -ll      : MEDIUM and above
# -l       : All issues including LOW
```

### Add More Steps

Example: Add linting check with Pylint:

```yaml
- name: Run Pylint
  run: |
    pip install pylint
    pylint app.py || true
```

### Exclude Directories

Bandit scans all files by default. To exclude certain directories:

```yaml
bandit -r . --exclude ".venv,tests,build"
```

---

## 📊 Pipeline Workflow Visualization

```
┌─────────────────────────────────────────┐
│ Code Pushed to GitHub (main branch)     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ GitHub Actions Triggered                │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   ┌─────────────┐    ┌──────────────────┐
   │ Security    │    │ Dependencies     │
   │ Scan Job    │    │ Check Job        │
   └──────┬──────┘    └──────┬───────────┘
          │                  │
    ┌─────┴──────────────────┘
    │
    ├─► Checkout
    ├─► Setup Python
    ├─► Install Bandit
    ├─► Run Full Scan
    ├─► Run Strict Scan ──┐
    ├─► Parse Results    │
    ├─► Upload Report    │
    ├─► Check Critical ◄─┘
    │
    ▼
┌─────────────────────────────────────────┐
│ ❌ FAIL (High severity issues found)    │
│ OR                                      │
│ ✅ PASS (No critical vulnerabilities)   │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Best Practices Demonstrated

1. **Shift-Left Security**: Security checks run early, not at deployment
2. **Automated Scanning**: Human-free, consistent security reviews
3. **Fail-Safe Pipeline**: Prevents insecure code from merging
4. **Reporting**: Clear, actionable vulnerability reports
5. **Artifact Storage**: Historical records for compliance/audit
6. **Concurrency Control**: Prevents duplicate runs, saves resources

---

## ⚠️ Important Note

**This project intentionally contains vulnerable code for educational purposes.** 

In a real application, you should:
- ✅ Use secrets management (GitHub Secrets, AWS Secrets Manager)
- ✅ Sanitize user inputs to prevent injection attacks
- ✅ Use secure deserialization (JSON instead of pickle)
- ✅ Disable debug mode in production
- ✅ Apply least-privilege principles
- ✅ Run security scanning regularly

---

## 📚 Learning Resources

- [Bandit Documentation](https://bandit.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OWASP Top 10 Security Risks](https://owasp.org/Top10/)
- [DevSecOps Best Practices](https://www.devsecops.org/)

---

## 🤝 Contributing

Feel free to extend this project:
- Add more security tools (Snyk, Trivy, SonarQube)
- Implement code quality checks (Pylint, Black)
- Add performance testing
- Create deployment stages
- Add notifications (Slack, email)

---

## 📄 License

This project is open source and available under the MIT License.

---

## 📞 Support

For questions or issues:
1. Check the GitHub Actions logs
2. Review Bandit documentation
3. Consult GitHub Actions troubleshooting guides

---

**Happy secure coding! 🚀**
