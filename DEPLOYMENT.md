# 🚀 Deployment Guide

## PyPI Deployment (Automatisch)

### Wie es funktioniert

```
Git Tag v1.0.0 → GitHub Actions → PyPI Release
```

### Schritt-für-Schritt

**1. Lokal Version bumpen**
```bash
# In pyproject.toml Version ändern
version = "1.0.1"

# Commit & Push
git add pyproject.toml
git commit -m "Bump version to 1.0.1"
git push origin main
```

**2. Git Tag erstellen**
```bash
# Tag erstellen
git tag -a v1.0.1 -m "Release v1.0.1"

# Push Tag
git push origin v1.0.1
```

**3. GitHub Actions macht den Rest**
- ✅ Tests laufen
- ✅ Package wird gebaut
- ✅ PyPI Upload (automatisch!)
- ✅ GitHub Release erstellt

### Manuelles Deployment (Notfall)

```bash
# Build
python -m build

# Check
twine check dist/*

# Upload (Token muss in ~/.pypirc sein)
twine upload dist/*
```

---

## 📊 Code Coverage

### Was ist Code Coverage?

Zeigt wie viel % deines Codes durch Tests abgedeckt ist:
```
memoryguard/core.py:     85% covered
memoryguard/dashboard.py: 60% covered
```

### Coverage lokal messen

```bash
# Installieren
pip install pytest-cov

# Tests mit Coverage
pytest tests/ --cov=memoryguard --cov-report=term-missing

# HTML Report generieren
pytest tests/ --cov=memoryguard --cov-report=html

# Öffnen
open htmlcov/index.html
```

### Coverage in CI/CD

```yaml
# .github/workflows/coverage.yml
name: Coverage

on: [push]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install
      run: pip install pytest pytest-cov psutil
    
    - name: Run tests with coverage
      run: pytest tests/ --cov=memoryguard --cov-report=xml
    
    - name: Upload to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

### Coverage Badge

```markdown
[![Coverage](https://codecov.io/gh/SHAdd0WTAka/memoryguard/branch/main/graph/badge.svg)](https://codecov.io/gh/SHAdd0WTAka/memoryguard)
```

---

## 🐳 Docker Deployment

### Automatisch bei Push

Jeder Push zu `main` baut ein neues Docker Image:
```
git push origin main → Docker Image: ghcr.io/shadd0wtaka/memoryguard:latest
```

### Manuelles Build

```bash
# Build
docker build -t memoryguard:latest .

# Tag
docker tag memoryguard:latest ghcr.io/shadd0wtaka/memoryguard:v1.0.0

# Push
docker push ghcr.io/shadd0wtaka/memoryguard:v1.0.0
```

---

## 🏷️ Release Checklist

- [ ] Version in `pyproject.toml` aktualisiert
- [ ] `CHANGELOG.md` aktualisiert
- [ ] Tests laufen grün
- [ ] Git Tag erstellt: `git tag -a vX.X.X`
- [ ] Tag gepusht: `git push origin vX.X.X`
- [ ] GitHub Release erstellt
- [ ] PyPI Package geprüft: `pip install memoryguard==X.X.X`

---

## 🔗 Nützliche Links

| Service | URL |
|---------|-----|
| PyPI | https://pypi.org/project/memoryguard/ |
| GitHub Packages | https://github.com/SHAdd0WTAka/memoryguard/pkgs/container/memoryguard |
| TestPyPI | https://test.pypi.org/project/memoryguard/ |
