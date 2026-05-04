# 📚 Quick Reference Guide

Fast lookup for common tasks and commands.

---

## 🚀 Quick Start Commands

### Deploy to GitHub

```bash
# Navigate to project
cd c:\Users\Aryan\Desktop\mdc-cicd

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/secure-cicd.git

# Commit and push
git add .
git commit -m "Initial commit: Secure CI/CD Pipeline"
git branch -M main
git push -u origin main
```

---

## 🧪 Local Testing

### Test Bandit Locally

```bash
# Install Bandit
pip install bandit

# Run full scan
bandit -r .

# Run with verbose output
bandit -r . -v

# Fail on HIGH severity only
bandit -r . -ll

# Generate JSON report
bandit -r . -f json -o report.json

# Generate text report
bandit -r . -f txt -o report.txt

# Exclude directories
bandit -r . --exclude ".venv,tests"
```

### Test Python Environment

```bash
# Check Python version
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app (if needed)
python app.py
```

---

## 🔄 Git Workflow

### Basic Git Commands

```bash
# Check status
git status

# Add files
git add .              # Add all
git add app.py         # Add specific file

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main

# View history
git log --oneline

# Create branch
git checkout -b branch-name

# Switch branch
git checkout main

# Merge branch
git merge branch-name
```

---

## 📊 GitHub Actions Monitoring

### Check Workflow Status

```
Repository → Actions tab → Click workflow run → Expand job steps
```

### View Logs

```
Click on any step → See full execution log
```

### Download Reports

```
Workflow run → Artifacts section → Click and download
```

---

## 🔐 GitHub Configuration

### Add Repository Secrets

```
Settings → Secrets and variables → Actions → New repository secret
```

Useful secrets:
- `DB_PASSWORD`
- `API_KEY`
- `SLACK_WEBHOOK`
- `SONAR_TOKEN`

### Enable Branch Protection

```
Settings → Branches → Add rule
- Branch name pattern: main
✓ Require status checks to pass
✓ Require pull request reviews
```

---

## 📝 File Locations

### Critical Files

| File | Path | Purpose |
|------|------|---------|
| Vulnerable App | `app.py` | Sample Flask app with security issues |
| Dependencies | `requirements.txt` | Python packages |
| Workflow | `.github/workflows/pipeline.yml` | GitHub Actions pipeline |
| Documentation | `README.md` | Project overview |
| Security Guide | `SECURITY.md` | Vulnerability explanations |
| Deployment | `DEPLOYMENT.md` | Setup instructions |
| Ignore File | `.gitignore` | Git exclusions |

---

## 🎯 Workflow Triggers

### Current Configuration

```yaml
on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
```

### To Trigger Manually

```bash
# Just push to main or develop
git push origin main

# Or commit to PR to main
```

---

## 🛠️ Common Edits

### Change Python Version

**File**: `.github/workflows/pipeline.yml`

Find:
```yaml
python-version: '3.10'
```

Change to:
```yaml
python-version: '3.11'  # or 3.12, 3.9, etc.
```

### Change Bandit Strictness

**File**: `.github/workflows/pipeline.yml`

Find:
```yaml
bandit -r . -ll
```

Options:
```bash
-lll      # Only CRITICAL
-ll       # MEDIUM and above (current)
-l        # All issues including LOW
(no flag) # All issues
```

### Add New Python Package

**File**: `requirements.txt`

```
Flask==2.3.2
requests==2.31.0       # Add this
```

Then:
```bash
git add requirements.txt
git commit -m "Add requests library"
git push origin main
```

---

## 📋 Bandit Severity Levels

| Level | Symbol | Meaning |
|-------|--------|---------|
| CRITICAL | 🔴 | Immediate threat, fix required |
| HIGH | 🔴 | Serious issue, fix recommended |
| MEDIUM | 🟠 | Moderate concern, review needed |
| LOW | 🟡 | Minor issue, consider fixing |

---

## 🔍 Bandit Issue Codes

Common issue codes detected:

| Code | Issue | Severity |
|------|-------|----------|
| B105 | Hardcoded password | HIGH |
| B602 | Shell injection | HIGH |
| B301 | Pickle usage | HIGH |
| B201 | Flask debug=True | MEDIUM |
| B101 | Assert statements | LOW |

---

## 🚨 Common Issues & Fixes

### Issue: Workflow Not Found

**Fix**:
```bash
# Verify file path
# Should be: .github/workflows/pipeline.yml (NOT .github/workflows/)
git add .github/workflows/pipeline.yml
git push origin main
```

### Issue: Python Version Not Available

**Fix**: Edit workflow to supported Python version (3.8-3.12)

### Issue: Bandit Installation Fails

**Fix**: Use Python >= 3.6

### Issue: YAML Syntax Error

**Fix**: Validate YAML at [yamllint.com](https://www.yamllint.com)

---

## 📊 Monitoring Metrics

### Track These in GitHub Actions

- ✅ Workflow success/failure rate
- ⏱️ Average execution time
- 🐛 Vulnerabilities detected per scan
- 📈 Trend of security issues over time

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| GitHub Actions Docs | docs.github.com/en/actions |
| Bandit Documentation | bandit.readthedocs.io |
| YAML Validator | yamllint.com |
| GitHub Marketplace | github.com/marketplace |
| Actions Status | github.com/status |

---

## ⌨️ Keyboard Shortcuts (VS Code)

```
Ctrl+`         → Open terminal
Ctrl+K Ctrl+O  → Open folder
Ctrl+Shift+G   → Open Git sidebar
Ctrl+Shift+`   → New terminal
Ctrl+G         → Go to line
Ctrl+F         → Find
Ctrl+H         → Find and replace
```

---

## 📞 Quick Help

### Reset Workflow State

```bash
# If workflow is stuck, push a new commit to trigger it
git add .
git commit -m "Trigger workflow"
git push origin main
```

### View All Workflow Runs

```
Repository → Actions → All workflow runs
```

### Debug Workflow Locally

```bash
# Install act (local GitHub Actions runner)
pip install act

# Run workflow locally
act -j security-scan
```

---

## ✅ Deployment Checklist

- [ ] Create GitHub repository
- [ ] Clone repository locally
- [ ] Copy all project files
- [ ] Commit with git
- [ ] Push to GitHub
- [ ] Verify Actions tab shows workflow
- [ ] Review first workflow run
- [ ] Check artifact download
- [ ] Verify security scan results
- [ ] Document any custom changes

---

## 🎓 Learning Path

1. **Understanding CI/CD**: Read README.md
2. **Security Vulnerabilities**: Read SECURITY.md
3. **Deployment**: Follow DEPLOYMENT.md
4. **Practice**: Make changes and trigger workflows
5. **Extend**: Add more security tools
6. **Mastery**: Build custom workflows for your projects

---

**Happy DevSecOps engineering! 🚀**
