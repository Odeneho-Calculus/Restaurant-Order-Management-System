# Contributing to Restaurant Order Management System

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Contribution Workflow](#contribution-workflow)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git for version control
- Text editor or IDE (VS Code, PyCharm recommended)

### First Time Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/restaurant-order-management.git
   cd restaurant-order-management
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/restaurant-order-management.git
   ```
4. **Verify the system works**:
   ```bash
   python test_system.py
   ```

## 🔧 Development Setup

### Running the Application

```bash
# Option 1: Use the launcher
python run_restaurant_system.py

# Option 2: Direct launch
python restaurant_system/main.py

# Option 3: Windows batch file
start_restaurant_system.bat
```

### Testing Your Changes

```bash
# Run all tests
python test_system.py

# Run feature demonstration
python demo_features.py

# Manual testing
python restaurant_system/main.py
```

## 📏 Code Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Structure

```python
"""
Module docstring explaining the purpose.
"""

import sys
import os
from typing import Optional, List, Dict

class ExampleClass:
    """
    Class docstring explaining purpose and usage.
    """

    def __init__(self, param: str) -> None:
        """Initialize with parameter."""
        self.param = param

    def example_method(self, value: int) -> bool:
        """
        Method docstring explaining parameters and return value.

        Args:
            value: Integer value to process

        Returns:
            Boolean indicating success

        Raises:
            ValueError: If value is negative
        """
        if value < 0:
            raise ValueError("Value cannot be negative")
        return True
```

### Type Hints

- Use type hints for all function parameters and return values
- Import types from `typing` module when needed
- Use `Optional[Type]` for optional parameters

### Error Handling

- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Implement graceful degradation

## 🔄 Contribution Workflow

### 1. Create a Feature Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, well-documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
python test_system.py

# Test the GUI manually
python run_restaurant_system.py

# Check for any errors in logs
cat restaurant_system/logs/restaurant_system.log
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add feature: detailed description of changes

- Specific change 1
- Specific change 2
- Fix for issue #123"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Include screenshots for UI changes
- List what you tested

## 🧪 Testing

### Running Tests

```bash
# Full test suite
python test_system.py

# Individual component tests
python -m pytest tests/ -v  # If pytest is available
```

### Test Coverage

- Write tests for new functionality
- Test both success and failure cases
- Include edge cases and boundary conditions
- Test GUI components where possible

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] All menu operations work
- [ ] Order processing is functional
- [ ] Queue updates correctly
- [ ] Receipts generate properly
- [ ] Reports export correctly
- [ ] Data persists between sessions

## 📚 Documentation

### Code Documentation

- Write docstrings for all classes and methods
- Use clear, concise language
- Include examples where helpful
- Document parameters, return values, and exceptions

### User Documentation

- Update user manual for new features
- Include screenshots for UI changes
- Update installation guide if needed
- Add troubleshooting information

### Documentation Files

- `README.md` - Main project overview
- `USER_MANUAL.md` - Detailed usage instructions
- `INSTALLATION_GUIDE.md` - Setup and deployment
- `PROJECT_SUMMARY.md` - Technical overview

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Update to the latest version** to see if issue persists
3. **Run the test suite** to identify any system problems
4. **Check the logs** in `restaurant_system/logs/`

### Creating a Good Issue Report

Include:

- **Clear title** summarizing the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **System information** (OS, Python version)
- **Error messages** or log excerpts
- **Screenshots** if applicable

### Issue Templates

#### Bug Report
```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**System Info**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.9.2]
- Application Version: [e.g., 1.0.0]

**Additional Context**
Any other context about the problem.
```

#### Feature Request
```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Use Case**
Explain why this feature would be useful.

**Proposed Solution**
How you think this could be implemented.

**Additional Context**
Any other context or screenshots.
```

## 🎯 Priority Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Performance optimizations
- Accessibility enhancements
- Cross-platform compatibility

### Medium Priority
- New features and functionality
- UI/UX improvements
- Documentation improvements
- Test coverage expansion

### Low Priority
- Code refactoring
- Additional examples
- Integration features
- Advanced analytics

## 🏆 Recognition

Contributors will be recognized in:
- Project README.md
- Release notes
- Special contributor documentation

## 📞 Getting Help

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the comprehensive docs included

## 📝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a welcoming environment

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Any unprofessional conduct

## 🎉 Thank You!

Your contributions help make this project better for everyone. Whether you're fixing bugs, adding features, improving documentation, or helping other users, every contribution is valuable and appreciated!

---

**Happy coding! 🚀**