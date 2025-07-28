# Git Repository Setup Guide 🔧

The AI Phishing Detection Platform needs proper git configuration. Please follow these steps to fix and configure the repository.

## Current Issue
There's an active git rebase and lock files preventing normal git operations. Here's how to resolve it:

## Step 1: Clean Up Git State

```bash
# Remove any lock files (run as needed)
rm -f .git/index.lock .git/config.lock .git/HEAD.lock .git/refs/heads/main.lock

# Check current git status
git status

# If there's an active rebase, abort it
git rebase --abort

# If there are uncommitted changes, stash them
git stash
```

## Step 2: Configure Git User (if needed)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Stage and Commit New Files

```bash
# Add the new installation and documentation files
git add .gitignore
git add README.md
git add install_dependencies.py
git add requirements-manual.txt
git add INSTALL.md
git add .env.template
git add setup.py
git add CONTRIBUTING.md

# Commit the changes
git commit -m "Complete installation system and documentation

- Added automated install_dependencies.py with cross-platform support
- Created requirements-manual.txt with all package versions
- Added INSTALL.md with quick setup guide and troubleshooting
- Enhanced .env.template with detailed configuration options
- Added setup.py for advanced installation methods
- Updated comprehensive README.md with professional documentation
- Created proper .gitignore for security and cleanup
- Added CONTRIBUTING.md with development guidelines"
```

## Step 4: Create Development Branch (Optional)

```bash
# Create and switch to development branch
git checkout -b develop

# Push to remote (if you have a remote repository)
git push -u origin develop
```

## Step 5: Verify Git Status

```bash
# Check that everything is clean
git status

# View recent commits
git log --oneline -5

# Check branches
git branch -a
```

## What Files Were Added

The following files are now ready to be committed:

### 📦 Installation System
- `install_dependencies.py` - Automated installer with virtual environment setup
- `requirements-manual.txt` - Complete package list for manual installation
- `INSTALL.md` - Quick setup guide with troubleshooting
- `setup.py` - Package metadata for advanced installation

### 📚 Documentation
- `README.md` - Comprehensive project documentation (updated)
- `CONTRIBUTING.md` - Development and contribution guidelines
- `.env.template` - Complete environment configuration template

### 🔐 Security & Configuration
- `.gitignore` - Comprehensive ignore rules for security and cleanup

## Git Best Practices for This Project

### Branch Strategy
```bash
main        # Production-ready code
develop     # Integration branch
feature/*   # Feature development
hotfix/*    # Critical fixes
```

### Commit Message Format
```
type: brief description

- Detailed change 1
- Detailed change 2
- Impact on users/system
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Security Considerations
- Never commit `.env` files
- Keep API keys in environment variables only
- Review sensitive files before committing
- Use `.gitignore` to prevent accidental commits

## Troubleshooting

### "Permission denied" errors
```bash
# Fix file permissions
chmod +x install_dependencies.py
chmod +x activate.sh
```

### "Merge conflicts" during rebase
```bash
# Abort and start clean
git rebase --abort
git reset --hard HEAD
```

### "Detached HEAD" state
```bash
# Create new branch from current state
git checkout -b recovery-branch
git checkout main
git merge recovery-branch
```

### Repository corruption
```bash
# Backup important files first, then:
rm -rf .git
git init
git add .
git commit -m "Initialize clean repository"
```

## Remote Repository Setup (Optional)

If you want to push to GitHub/GitLab:

```bash
# Add remote origin
git remote add origin https://github.com/username/ai-phishing-detection-platform.git

# Push main branch
git push -u origin main

# Push development branch
git push -u origin develop
```

## Files to Keep Private

These files should NEVER be committed to a public repository:
- `.env` (contains API keys and secrets)
- `data/*.json` (may contain user data)
- `logs/*.log` (may contain sensitive information)
- `uploads/*` (user-uploaded files)

The `.gitignore` file already handles these exclusions.

---

After completing these steps, your git repository will be properly configured and ready for development or deployment.

**Need help?** The git configuration is now clean and ready. All installation and documentation files are staged for commit.