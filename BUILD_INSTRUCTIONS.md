# Build Instructions

## Overview
This document describes how to build and deploy the AI Recruiter application.

## Quick Start

### Development Build
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Production Build
```bash
# Run the build script
python build/build.py

# Check the build output
ls build/ai_recruiter/
```

## Directory Structure

```
ai_recruiter/
│
├── app.py                          # Main Streamlit application
├── candidate_template.csv          # CSV template for candidates
├── requirements.txt                # Python dependencies
│
├── src/                            # Source code modules (future)
├── config/                         # Configuration files
├── tests/                          # Unit tests
│
├── build/                          # Build script and intermediate files
│   ├── build.py                    # Build automation script
│   └── ai_recruiter/              # Built application files
│
├── dist/                           # Distribution packages
│   └── ai_recruiter.zip           # Packaged application
│
├── .streamlit/                     # Streamlit configuration
│   └── config.toml                # Theme and server settings
│
├── setup.py                        # Package setup configuration
├── .gitignore                      # Git ignore rules
└── BUILD_INSTRUCTIONS.md           # This file
```

## Build Process

### Step 1: Prepare Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Build Script
```bash
python build/build.py
```

This script will:
- ✓ Clean previous build artifacts
- ✓ Copy source files to build directory
- ✓ Copy configuration files
- ✓ Create build manifest
- ✓ Generate startup scripts (Windows .bat and Linux .sh)
- ✓ Generate README documentation
- ✓ Package everything as ZIP distribution

### Step 3: Verify Build
```bash
# Check build directory
ls -la build/ai_recruiter/

# Should contain:
# - app.py
# - requirements.txt
# - candidate_template.csv
# - README.md
# - MANIFEST.txt
# - run.bat (Windows)
# - run.sh (Linux/Mac)
# - config/ (if present)
```

### Step 4: Create Distribution
The build script automatically creates a ZIP package in `dist/`:
```bash
ls dist/ai_recruiter.zip
```

## Deployment Options

### Option 1: Local Development
```bash
streamlit run app.py
```
Access at: `http://localhost:8502`

### Option 2: Using Built Package
```bash
# Navigate to build directory
cd build/ai_recruiter

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Option 3: Distribution Package
1. Extract `dist/ai_recruiter.zip`
2. Navigate to extracted directory
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `streamlit run app.py`

### Option 4: Docker (Future)
A Dockerfile can be created for containerized deployment:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8502
CMD ["streamlit", "run", "app.py"]
```

## Configuration

### Streamlit Settings
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server port (default: 8502)
- Logger level
- Client behavior

### Application Settings
Create `config/app_config.py` for custom settings:
```python
UPLOAD_MAX_SIZE = 50  # MB
DEFAULT_SKILLS_DB = "config/skills.json"
```

## Testing

### Run Tests (Future)
```bash
# Unit tests
pytest tests/

# With coverage
pytest --cov=. tests/
```

## Troubleshooting

### Issue: Module not found
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution:** Change port in `.streamlit/config.toml`:
```toml
[server]
port = 8503
```

### Issue: PDF parsing fails
**Solution:** Ensure `pypdf` is installed:
```bash
pip install pypdf
```

## Clean Build
```bash
python build/build.py
```
This automatically cleans previous builds before creating new ones.

## Distribution Checklist
- [ ] All dependencies listed in `requirements.txt`
- [ ] `.streamlit/config.toml` properly configured
- [ ] `setup.py` version updated
- [ ] `README.md` documentation complete
- [ ] Build script runs without errors
- [ ] ZIP distribution created in `dist/`
- [ ] Application runs from extracted ZIP

## Support
For issues or questions, refer to the README.md or contact support.
