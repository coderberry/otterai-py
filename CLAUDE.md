# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Testing
- **Setup development environment**: `./run.sh` - Sets up virtual environment, installs dependencies, runs pre-commit hooks, executes tests with coverage, and runs the main application
- **Run unit tests only**: `pytest tests/ -m 'not integration'` (recommended for regular development)
- **Run single integration test**: `pytest tests/test_otterai.py::test_get_user -s`
- **Run all tests with coverage**: `pytest -s --cov=otterai --cov-report=term-missing --cov-report=lcov:lcov.info --cov-report=xml:cov.xml`
- **⚠️ Warning**: Running all tests together will cause 429 rate limit errors from Otter.ai API
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

## Structured Data Implementation Guidelines

**⚠️ IMPORTANT**: Only implement structured data models for endpoints listed in `TEMP.md`. Do not create new endpoints or modify existing endpoint behavior unless explicitly specified.

### Implementation Rules:
1. **Endpoint Scope**: Only implement models for the exact endpoints listed in `TEMP.md`
2. **Model Purpose**: Create Pydantic models to structure and validate the JSON responses from existing endpoints
3. **Naming Convention**: Use `*_structured()` methods for structured versions of existing endpoints
4. **Backward Compatibility**: Always maintain existing endpoint functionality - never modify existing method signatures or behavior
5. **Parameter Matching**: Use the exact same parameters as shown in `TEMP.md` (e.g., `simple_group=true` for `list_groups`)

### Current Endpoints in TEMP.md:
- `list_groups?simple_group=true` → Group/GroupsResponse models
- `speakers?userid={userid}` → Speaker/SpeakersResponse models  
- `contacts?userid={userid}` → Contact/ContactsResponse models
- `folders?userid={userid}` → Folder/FoldersResponse models
- `speech_mention_candidates?otid={otid}` → MentionCandidate/MentionCandidatesResponse models

### Phase-by-Phase Implementation:
- **Phase 1**: Foundation setup (completed)
- **Phase 2**: Simple models (completed)
- **Phase 3**: Complex models for Groups and Speakers (in progress)
- **Phase 4+**: Additional endpoints as specified in IMPLEMENTATION_SPEC.md

### Key Reminders:
- Never remove existing functionality
- Always check `TEMP.md` for the authoritative list of endpoints to implement
- Use sample API responses from `.claude/context/sample-api-responses/*.json` for model validation
- Follow existing patterns for structured response methods