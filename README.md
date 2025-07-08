# otterai-py

Unofficial Python API for [otter.ai](http://otter.ai)

**Note:** This project is a fork of [gmchad/otterai-api](https://github.com/gmchad/otterai-api), as the original repository appears to be abandoned. Improvements and updates will be maintained here.

## Contents

-   [Installation](#installation)
-   [Setup](#setup)
-   [APIs](#apis)
    -   [User](#user)
    -   [Speeches](#speeches)
    -   [Speakers](#speakers)
    -   [Folders](#folders)
    -   [Groups](#groups)
    -   [Notifications](#notifications)
-   [Exceptions](#exceptions)
-   [Testing](#testing)
-   [Development](#development)
-   [Contribution](#contribution)

## Installation

Install via PyPI:

```bash
pip install otterai-py
```

For development (from source):

```bash
git clone https://github.com/coderberry/otterai-py.git
cd otterai-py
python3 -m venv .venv
source .venv/bin/activate
pip install .[dev]
```

## Setup

```python
from otterai import OtterAI
otter = OtterAI()
otter.login('USERNAME', 'PASSWORD')
```

### Structured Data Models

This library now includes Pydantic models for structured data handling:

```python
from otterai import User, Workspace, Permission, BaseResponse

# Models provide type safety and validation
user = User(id=123, name="John Doe", email="john@example.com", 
           first_name="John", last_name="Doe")
```

Future versions will include structured methods (e.g., `get_user_structured()`) that return these models instead of raw dictionaries.

## APIs

### User

Get user-specific data:

```python
otter.get_user()
```

### Speeches

Get all speeches.

**Optional parameters**: `folder`, `page_size`, `source`

```python
otter.get_speeches()
```

Get a speech by ID:

```python
otter.get_speech(OTID)
```

Query a speech:

```python
otter.query_speech(QUERY, OTID)
```

Upload a speech.

**Optional parameters**: `content_type` (default: `audio/mp4`)

```python
otter.upload_speech(FILE_NAME)
```

Download a speech.

**Optional parameters**: `filename` (default: `id`), `format` (default: all available formats (`txt,pdf,mp3,docx,srt`) as a zip file)

```python
otter.download_speech(OTID, FILE_NAME)
```

Move a speech to the trash:

```python
otter.move_to_trash_bin(OTID)
```

Set speech title:

```python
otter.set_speech_title(OTID, TITLE)
```

#### TODO

-   Start a live speech
-   Stop a live speech
-   Assign a speaker to a speech transcript

### Speakers

Get all speakers:

```python
otter.get_speakers()
```

Create a speaker:

```python
otter.create_speaker(SPEAKER_NAME)
```

### Folders

Get all folders:

```python
otter.get_folders()
```

### Groups

Get all groups:

```python
otter.list_groups()
```

### Notifications

Get notification settings:

```python
otter.get_notification_settings()
```

## Exceptions

```python
from otterai import OtterAIException

try:
    ...
except OtterAIException as e:
    ...
```

## Testing

⚠️ **Important**: This project has two types of tests:

- **Unit tests**: Mock tests that don't hit the API (safe to run)
- **Integration tests**: Tests that make real API calls (can cause rate limits)

### Running Tests Safely

```bash
# Run only unit tests (recommended for development)
pytest tests/ -m 'not integration'

# Run a single integration test
pytest tests/test_otterai.py::test_get_user -s

# See all available tests
pytest tests/ --collect-only
```

### Rate Limiting Warning

Running all tests together **will cause 429 rate limit errors** from the Otter.ai API. The test suite will warn you if you attempt this:

```
⚠️  WARNING: Running 12 integration tests together!
This will likely result in 429 rate limit errors from the Otter.ai API.
```

## Development

### Quick Start

```bash
# Setup development environment
./run.sh
```

This script:
- Creates a virtual environment
- Installs dependencies
- Runs pre-commit hooks
- Executes unit tests (skipping integration tests)
- Starts the example application

### Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install .[dev]

# Run unit tests only
pytest tests/ -m 'not integration'
```

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:

```bash
pre-commit install
pre-commit run --all-files
```

## Contribution

To contribute to this project, follow these steps:

1. **Fork the repository** and create a feature branch

2. **Setup development environment**:
   ```bash
   ./run.sh
   ```

3. **For integration testing** (optional), create a `.env` file:
   ```plaintext
   OTTERAI_USERNAME=""
   OTTERAI_PASSWORD=""
   TEST_OTTERAI_SPEECH_OTID=""
   ```
   
   - Replace with your Otter.ai credentials
   - Replace `TEST_OTTERAI_SPEECH_OTID` with an actual speech ID from your account
   - **Note**: Only needed if you want to run integration tests

4. **Run tests**:
   ```bash
   # Unit tests only (recommended)
   pytest tests/ -m 'not integration'
   
   # Individual integration test (if needed)
   pytest tests/test_otterai.py::test_get_user -s
   ```

5. **Code quality**:
   ```bash
   # Format code
   black .
   
   # Run pre-commit hooks
   pre-commit run --all-files
   ```

6. **Submit a pull request** with:
   - Clear description of changes
   - Updated tests if adding functionality
   - All unit tests passing
