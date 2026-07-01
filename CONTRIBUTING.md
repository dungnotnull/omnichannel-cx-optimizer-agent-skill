# Contributing to Omnichannel CX Optimizer

Thank you for your interest in contributing to the Omnichannel CX Optimizer skill! This document provides guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Familiarity with customer experience concepts
- Understanding of the skill's architecture

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd omnichannel-cx-optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest pytest-cov black mypy
```

## Development Workflow

1. **Fork and Branch**
   - Fork the repository
   - Create a feature branch: `git checkout -b feature/your-feature-name`

2. **Make Changes**
   - Write code following coding standards
   - Add tests for new functionality
   - Update documentation

3. **Test Changes**
   - Run test suite: `pytest`
   - Check code style: `black .`
   - Type check: `mypy .`

4. **Commit Changes**
   - Write clear commit messages
   - Reference related issues

5. **Submit Pull Request**
   - Describe your changes
   - Link to related issues
   - Ensure CI checks pass

## Coding Standards

### Python Code

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write docstrings for all public functions
- Keep functions focused and modular
- Use meaningful variable names

### Example

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class KnowledgeEntry:
    """Immutable knowledge entry with complete metadata."""
    
    title: str
    url: str
    authors: str
    year: int
    abstract: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "url": self.url,
            "authors": self.authors,
            "year": self.year,
            "abstract": self.abstract,
        }
```

### Markdown Files

- Use proper heading hierarchy
- Include table of contents for long documents
- Use code blocks for technical content
- Add links to related documentation

### YAML Schemas

- Follow YAML syntax and best practices
- Include comments for clarity
- Use consistent indentation
- Document schema structure

## Testing Guidelines

### Test Structure

Tests are organized in `tests/test-scenarios.md` and cover:

1. **Happy Path Tests** — Normal usage scenarios
2. **Edge Case Tests** — Boundary conditions and unusual inputs
3. **Adversarial Tests** — Malicious or conflicting inputs
4. **Integration Tests** — Cross-skill interactions

### Adding New Tests

When adding new features:

1. Add at least one test scenario per feature
2. Include edge cases and adversarial scenarios
3. Document expected behavior clearly
4. Update pass/fail criteria

### Example Test Scenario

```markdown
## Scenario 11: Your Feature Test
**Input:** Description of test input

**Expected behavior:**
- Expected outcome 1
- Expected outcome 2

**Quality gates checked:**
- Gate 1 description
- Gate 2 description

**Pass criteria:**
- Success criterion 1
- Success criterion 2

**Test Date:** YYYY-MM-DD
**Status:** ✅ PASSED / ❌ FAILED
**Notes:** Additional context
```

## Documentation

### Required Documentation

When making changes, update:

1. **README.md** — For user-facing changes
2. **CHANGELOG.md** — For version history
3. **Relevant docs/** — For technical changes
4. **Code comments** — For complex logic

### Documentation Style

- Use clear, concise language
- Include examples where helpful
- Maintain consistent formatting
- Update dates and version numbers

### Adding New Sub-Skills

When creating new sub-skills:

1. Follow the established frontmatter format
2. Define clear inputs, outputs, and workflow
3. Specify quality gates
4. Include examples in documentation
5. Update the main harness to invoke the sub-skill

## Submitting Changes

### Pull Request Checklist

Before submitting a PR, ensure:

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages are clear
- [ ] PR description is comprehensive

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass

## Documentation
- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] Other docs updated

## Checklist
- [ ] Code follows project standards
- [ ] Self-review completed
- [ ] Ready for review
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority
- Additional CX frameworks and dimensions
- Enhanced test scenarios
- Knowledge source expansion
- Documentation improvements

### Medium Priority
- Performance optimizations
- Additional language support
- Integration with other skills
- Example use cases

### Low Priority
- UI/UX improvements
- Tooling and automation
- Monitoring and observability

## Questions or Issues?

For questions about contributing:

1. Check existing documentation
2. Review open issues for similar topics
3. Open a new issue with the `question` label
4. Join community discussions (if available)

## Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project documentation for ongoing contributions

Thank you for contributing to the Omnichannel CX Optimizer!

---

**Last Updated:** 2026-07-01
