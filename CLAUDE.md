# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Testing
- **Setup development environment**: `./run.sh` - Sets up virtual environment, installs dependencies, runs pre-commit hooks, executes tests with coverage, and runs the main application
- **Run tests**: `pytest -s --cov=otterai --cov-report=term-missing --cov-report=lcov:lcov.info --cov-report=xml:cov.xml`
- **Run single test**: `pytest -s tests/test_otterai.py::test_function_name`
- **Code formatting**: `black .` (configured for line length 88, Python 3.9+)
- **Pre-commit hooks**: `pre-commit run --all-files`

### Development Dependencies
Install development dependencies with: `pip install .[dev]`

### Manual Application Testing
Run the main application: `python main.py`

## Architecture Overview

This is a Python library providing an unofficial API client for Otter.ai transcription services. The project follows a simple, single-module architecture:

### Core Components

**Main API Client (`otterai/otterai.py`)**:
- `OtterAI` class: Main client with session management and retry logic using tenacity
- `OtterAIException`: Custom exception for API-related errors
- Authentication via username/password with session persistence
- Built-in rate limiting and retry mechanisms with exponential backoff
- Supports all major Otter.ai operations: speeches, speakers, folders, groups, notifications

**Key API Endpoints**:
- User management: login, get_user
- Speech operations: get_speeches, get_speech, query_speech, upload_speech, download_speech, set_speech_title, move_to_trash_bin
- Speaker management: get_speakers, create_speaker
- Organization: get_folders, list_groups
- Settings: get_notification_settings

**Authentication Flow**:
1. Login stores `_userid` and `_cookies` for session management
2. Most operations require valid userid (checked via `_is_userid_invalid()`)
3. CSRF tokens from cookies used for POST operations

**Request Handling**:
- All HTTP requests go through `_make_request()` with retry logic
- Rate limiting handled automatically with `Retry-After` header support
- Supports both GET and POST with proper header management

## Testing Setup

Tests require a `.env` file with:
```
OTTERAI_USERNAME=""
OTTERAI_PASSWORD=""
TEST_OTTERAI_SPEECH_OTID=""
```

The test suite uses pytest with extensive mocking and covers:
- Authentication flows
- All API endpoints
- Error handling and edge cases
- File download functionality

## Project Structure

- `otterai/`: Main package directory
  - `__init__.py`: Package exports
  - `otterai.py`: Core API client implementation
- `tests/`: Test suite with comprehensive coverage
- `main.py`: Example usage script
- `run.sh`: Development setup and testing script

## Dependencies

**Runtime**: requests, requests-toolbelt, tenacity, python-dotenv
**Development**: pytest, pytest-cov, black, pre-commit

## Common Development Patterns

When adding new API endpoints:
1. Add method to `OtterAI` class following existing patterns
2. Include userid validation for authenticated endpoints
3. Use `_make_request()` for all HTTP calls
4. Return `_handle_response()` for consistent response format
5. Add corresponding tests with both success and failure cases

The codebase uses tenacity for robust retry logic and requests-toolbelt for multipart uploads.