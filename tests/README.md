# Gaia AI Test Suite

This directory contains organized test files for the modular Gaia AI system.

## Directory Structure

```text
tests/
├── __init__.py              # Test package initialization
├── run_tests.py             # Main test runner script
├── README.md                # This file
├── core/                    # Core component tests
│   ├── __init__.py
│   ├── test_components.py   # General component tests
│   └── test_whisper.py      # Whisper/voice processing tests
├── llm/                     # LLM and training tests
│   ├── __init__.py
│   └── test_local_llm.py    # Local LLM interface tests
├── hotel/                   # Hotel management tests
│   ├── __init__.py
│   ├── test_hotel_advanced.py
│   ├── test_hotel_commands.py
│   ├── test_hotel_emails.py
│   └── test_hotel_gui.py
├── interfaces/              # Interface tests
│   └── __init__.py
└── architecture/            # System architecture tests
    ├── __init__.py
    ├── test_modular.py      # Modular system tests
    └── test_new_architecture.py
```

## Running Tests

### Run All Tests

```bash
cd tests
python run_tests.py
```

### Run Specific Category

```bash
cd tests
python run_tests.py core      # Run core tests
python run_tests.py llm       # Run LLM tests
python run_tests.py hotel     # Run hotel tests
python run_tests.py interfaces # Run interface tests
python run_tests.py architecture # Run architecture tests
```

### Verbose Output

```bash
python run_tests.py --verbose
```

## Test Categories

### 🔧 Core Tests

- Component functionality tests
- Voice processing and Whisper tests
- Basic system operations

### 🧠 LLM Tests

- Local LLM interface tests
- Model loading and inference tests
- Training pipeline tests

### 🏨 Hotel Tests

- Hotel management system tests
- GUI interface tests
- Email integration tests
- Command processing tests

### 🖥️ Interface Tests

- CLI interface tests
- GUI interface tests
- API interface tests

### 🏗️ Architecture Tests

- Modular system tests
- Component integration tests
- System-wide functionality tests

## Writing New Tests

### Test File Naming

- Use `test_*.py` naming convention
- Place in appropriate category directory
- Include descriptive names (e.g., `test_hotel_booking.py`)

### Test Structure

```python
#!/usr/bin/env python3
"""
Test description
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Your imports here
from src.module import YourClass

def test_function_name():
    """Test specific functionality"""
    # Test implementation
    pass

def main():
    """Main test function (optional)"""
    test_function_name()
    print("All tests passed!")

if __name__ == "__main__":
    main()
```

## Best Practices

1. **Import Path**: Always add project root to sys.path for consistent imports
2. **Error Handling**: Include proper error handling and meaningful messages
3. **Documentation**: Document what each test is verifying
4. **Isolation**: Tests should be independent and not rely on external state
5. **Cleanup**: Clean up any resources or temporary files created during tests

## Integration with CI/CD

The test runner can be integrated into automated build pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd tests
    python run_tests.py
```
