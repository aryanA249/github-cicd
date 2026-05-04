# 🚀 Deployment Guide

Complete step-by-step guide to deploy the Secure CI/CD Pipeline project to GitHub.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ A GitHub account (free or paid)
- ✅ Git installed on your machine
- ✅ Basic command-line knowledge
- ✅ A code editor (VS Code, etc.)

---

## 🔧 Option 1: Deploy Existing Project (Recommended)

If you already have these files, follow this option.

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **"+"** (top-right) → **"New repository"**
3. Fill in details:
   - **Repository name**: `secure-cicd`
   - **Description**: "Secure CI/CD Pipeline with GitHub Actions and Bandit"
   - **Visibility**: Choose "Public" or "Private"
   - **Initialize repository**: Leave unchecked (we'll push existing code)
4. Click **"Create repository"**

### Step 2: Initialize Git and Configure Remote

```bash
# Navigate to your project directory
cd c:\Users\Aryan\Desktop\mdc-cicd

# Initialize git repository
git init

# Configure git with your details
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add GitHub remote
git remote add origin https://github.com/<YOUR_USERNAME>/secure-cicd.git

# Verify remote
git remote -v
```

### Step 3: Add and Commit Files

```bash
# Add all files
git add .

# Verify files to be committed
git status

# Commit with message
git commit -m "Initial commit: Add secure CI/CD pipeline with Bandit scanning"
```

### Step 4: Push to GitHub

```bash
# Set default branch to 'main' and push
git branch -M main
git push -u origin main

# Wait for push to complete (should see progress bar)
```

### Step 5: Verify Workflow Triggered

1. Go to your GitHub repository
2. Click on the **"Actions"** tab
3. You should see a workflow run called "Secure CI/CD Pipeline with Security Scanning"
4. Click on the run to see details

---

## 🔧 Option 2: Create from Scratch

If you want to create the project from scratch on GitHub.

### Step 1: Create Repository with Files

1. Go to [GitHub](https://github.com) → **"New repository"**
2. Enter repository name: `secure-cicd`
3. **Check**: "Add a README file"
4. Click **"Create repository"**

### Step 2: Add Files via GitHub Web UI

1. Click **"Add file"** → **"Create new file"**
2. Create `app.py`:
   - In filename field, type: `app.py`
   - Copy content from the provided `app.py`
   - Click **"Commit changes"**

3. Create `requirements.txt`:
   - Click **"Add file"** → **"Create new file"**
   - Type: `requirements.txt`
   - Copy content
   - Commit

4. Create workflow file:
   - Click **"Add file"** → **"Create new file"**
   - Type: `.github/workflows/pipeline.yml`
   - Copy content from provided workflow
   - Commit

### Step 3: Trigger Workflow

The workflow automatically triggers after pushing files. Check **"Actions"** tab.

---

## ⚙️ Configuration

### Set Up GitHub Secrets (Optional)

To use real credentials safely:

1. Go to repository **"Settings"**
2. Sidebar → **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**
4. Add secrets (examples):
   - Name: `DB_PASSWORD` | Value: `your_actual_password`
   - Name: `API_KEY` | Value: `your_actual_key`

5. Use in workflow:
   ```yaml
   env:
     DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
     API_KEY: ${{ secrets.API_KEY }}
   ```

### Allow GitHub Actions (If Needed)

Some organizations require explicit permission:

1. Go to **"Settings"** → **"Actions"** → **"General"**
2. Under "Actions permissions", select:
   - ✅ **"Allow all actions and reusable workflows"**
3. Click **"Save"**

---

## 🧪 Verify Deployment

### Check Workflow Execution

1. **Go to Actions Tab**
   ```
   Repository → Actions tab → Latest workflow run
   ```

2. **Expand "Security Scan" Job**
   - See all steps executed
   - Check for errors or warnings

3. **View Log Output**
   - Look for Bandit scan results
   - Should show detected vulnerabilities

4. **Download Artifacts**
   - Expand "Artifacts" section
   - Download `bandit-security-report` JSON file

### Expected Results

The workflow should:
- ✅ Checkout code successfully
- ✅ Setup Python 3.10
- ✅ Install Bandit
- ✅ Run full Bandit scan (show vulnerabilities)
- ✅ Run strict scan (fail due to HIGH severity issues)
- ❌ **Fail the build** (intentionally, due to vulnerabilities in sample app)

This is **expected behavior** — the pipeline demonstrates failing on security issues!

---

## 🎯 Next Steps

### Fix the Vulnerable App (Learn Objective)

Create a new branch and fix vulnerabilities:

```bash
# Create feature branch
git checkout -b fix/security-vulnerabilities

# Edit app.py to fix issues
# Make the changes...

# Commit and push
git add app.py
git commit -m "Fix: Remove hardcoded credentials and insecure patterns"
git push origin fix/security-vulnerabilities
```

Then create a Pull Request on GitHub to see the pipeline run on your fixed code.

### Extend the Pipeline

Add more security tools:

```yaml
# Add to pipeline.yml
- name: Run Pylint
  run: |
    pip install pylint
    pylint app.py

- name: Run OWASP Dependency Check
  uses: jeremylong/DependencyCheck_Action@main
```

### Add Notifications

Notify team on security issues:

```yaml
- name: Slack Notification
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 🔄 Update and Maintain

### Pull Latest Changes Locally

```bash
git pull origin main
```

### Make Changes Locally and Push

```bash
# Make edits
# ... edit files ...

# Commit
git add .
git commit -m "Description of changes"

# Push
git push origin main

# Workflow automatically triggers
```

### Monitor Workflow Runs

1. Go to **Actions** tab
2. See all workflow executions
3. Click on any run for details
4. Download reports as needed

---

## 🆘 Troubleshooting

### Workflow Not Triggering

**Problem**: Actions tab is empty

**Solution**:
```bash
# Verify files are in correct location
# .github/workflows/pipeline.yml (note: .github, not github)

# Check git status
git status

# If workflow file missing, create it
git add .github/workflows/pipeline.yml
git commit -m "Add workflow file"
git push origin main
```

### Workflow Failed with Syntax Error

**Problem**: Workflow file has YAML syntax error

**Solution**:
1. Download the workflow file locally
2. Validate YAML: [YAML Validator](https://www.yamllint.com/)
3. Check indentation (YAML is space-sensitive)
4. Fix and re-push

### Python Version Mismatch

**Problem**: Workflow fails with Python compatibility error

**Solution**:
Edit `pipeline.yml`:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # Try 3.11 or 3.12
```

### Bandit Installation Fails

**Problem**: pip install bandit fails

**Solution**:
```yaml
- name: Install Bandit with Retry
  run: |
    pip install --upgrade pip
    pip install bandit[toml] --retries 3
```

---

## 📊 Workflow Dashboard

GitHub provides insights:

1. Go to **Settings** → **Insights** → **Graphs**
2. See workflow execution statistics
3. Identify trends and issues

---

## 🔐 Security Best Practices

### Repository Settings

1. **Enable branch protection**:
   - Settings → Branches → Add rule
   - Require pull request reviews
   - Require status checks to pass

2. **Enable vulnerability alerts**:
   - Settings → Code security and analysis
   - Enable "Dependabot alerts"
   - Enable "Secret scanning"

3. **Disable workflow write permissions**:
   - Settings → Actions → General
   - Set to "Read repository contents only"

---

## 📝 CI/CD Best Practices

1. **Always run security checks**: Make it mandatory in PRs
2. **Review scan results**: Don't ignore warnings
3. **Update dependencies**: Run `pip-audit` regularly
4. **Archive reports**: Keep historical records
5. **Monitor metrics**: Track vulnerability trends

---

## 🎓 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Bandit Security Tool](https://bandit.readthedocs.io/)
- [DevSecOps Best Practices](https://www.devsecops.org/)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## 📞 Support

### Get Logs for Debugging

1. Go to workflow run
2. Click on failed step
3. Copy entire log
4. Share for help

### Common GitHub Actions Issues

- [GitHub Actions Troubleshooting](https://docs.github.com/en/actions/guides)
- [Stack Overflow Tag: github-actions](https://stackoverflow.com/questions/tagged/github-actions)

---

**Your Secure CI/CD Pipeline is now ready! 🚀**

Next steps:
- [ ] Create GitHub repository
- [ ] Push files
- [ ] Verify workflow runs
- [ ] Review security scan results
- [ ] Explore GitHub Actions dashboard
