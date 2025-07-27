# GitHub Repository Setup Guide

## Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `gaia-ai-voice-assistant`
3. Description: `Production-ready AI voice assistant with Azure TTS, Whisper recognition, and Windows automation`
4. Set to **Public** or **Private** (your choice)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Local Repository to GitHub
After creating the GitHub repository, run these commands in your terminal:

```bash
# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/gaia-ai-voice-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload
- Check that all files appear on GitHub
- Verify README.md displays properly
- Confirm .gitignore is protecting config.json (it shouldn't be visible)

## Step 4: Repository Management Best Practices

### Regular Commits
```bash
# After making changes
git add .
git commit -m "Description of changes"
git push origin main
```

### Branching for Features
```bash
# Create feature branch
git checkout -b feature/new-voice-commands
# Work on feature...
git add .
git commit -m "Add new voice commands"
git push origin feature/new-voice-commands
# Create pull request on GitHub
```

### Tags for Releases
```bash
# Tag stable versions
git tag -a v1.0.0 -m "Stable release with TTS fallback"
git push origin v1.0.0
```

## Security Notes
- config.json is in .gitignore (contains Azure credentials)
- Use config.json.example as template for others
- Never commit actual API keys to the repository
- Consider using environment variables for sensitive data

## Collaboration
- Share repository URL with team members
- Use Issues for bug tracking
- Use Discussions for feature requests
- Review pull requests before merging
