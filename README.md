# otterai-py

Unofficial Python API for [otter.ai](http://otter.ai)

**Note:** This project is a fork of [gmchad/otterai-api](https://github.com/gmchad/otterai-api), as the original repository appears to be abandoned. Improvements and updates will be maintained here.

## Contents

-   [Installation](#installation)
-   [Setup](#setup)
-   [Interactive API Explorer](#interactive-api-explorer)
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

This library includes comprehensive Pydantic models for structured data handling with full type safety and validation:

```python
from otterai import (
    OtterAI,
    ContactsResponse, 
    GroupsResponse, 
    SpeechResponse,
    SpeakersResponse,
    FoldersResponse,
    SpeechTemplatesResponse,
    ActionItemsResponse,
    AbstractSummaryResponse,
    AvailableSpeechesResponse,
    MentionCandidatesResponse
)

# Initialize client
otter = OtterAI()
otter.login('USERNAME', 'PASSWORD')

# Use structured methods for type-safe responses
contacts = otter.get_contacts_structured()
print(f"Found {len(contacts.contacts)} contacts")
for contact in contacts.contacts:
    print(f"- {contact.first_name} {contact.last_name} ({contact.email})")

# Get groups with nested user objects
groups = otter.list_groups_structured()
for group in groups.groups:
    print(f"Group: {group.name} - Owner: {group.owner.name}")

# Get speech with complex nested structures
speech = otter.get_speech_structured("your_speech_otid")
print(f"Speech: {speech.speech.title}")
print(f"Duration: {speech.speech.duration} seconds")
if speech.speech.chat_status:
    print(f"Chat enabled: {speech.speech.chat_status.show_chat}")

# Get available speeches with pagination
speeches = otter.get_available_speeches_structured(
    funnel="home_feed",
    page_size=10,
    source="home"
)
print(f"Found {len(speeches.speeches)} speeches")
```

#### Migration Guide

**From Raw Dictionary Responses to Structured Models:**

```python
# Old approach (still supported)
speeches_raw = otter.get_speeches()
title = speeches_raw['data']['speeches'][0]['title']  # Fragile

# New structured approach
speeches = otter.get_available_speeches_structured()
title = speeches.speeches[0].title  # Type-safe with IDE support
```

**Benefits of Structured Models:**

- **Type Safety**: Full IDE support with autocomplete and type checking
- **Validation**: Automatic validation of API responses
- **Documentation**: Built-in field descriptions and type hints
- **Backward Compatibility**: All existing methods continue to work
- **Error Prevention**: Catch API changes at runtime with clear error messages

**Available Structured Methods:**

All endpoints now have structured equivalents:

| Original Method | Structured Method | Response Model |
|----------------|-------------------|----------------|
| `get_contacts()` | `get_contacts_structured()` | `ContactsResponse` |
| `get_folders()` | `get_folders_structured()` | `FoldersResponse` |
| `list_groups()` | `list_groups_structured()` | `GroupsResponse` |
| `get_speakers()` | `get_speakers_structured()` | `SpeakersResponse` |
| `get_speech()` | `get_speech_structured()` | `SpeechResponse` |
| N/A | `get_available_speeches_structured()` | `AvailableSpeechesResponse` |
| N/A | `get_speech_templates_structured()` | `SpeechTemplatesResponse` |
| N/A | `get_speech_action_items_structured()` | `ActionItemsResponse` |
| N/A | `get_abstract_summary_structured()` | `AbstractSummaryResponse` |
| N/A | `get_speech_mention_candidates_structured()` | `MentionCandidatesResponse` |

## Interactive API Explorer

The project includes an interactive CLI tool for easily testing and exploring the OtterAI API endpoints:

```bash
./perform.sh
```

This will launch an interactive menu that allows you to:

- **Select APIs**: Choose from available endpoints like `abstract_summary`, `available_speeches`, `get_user`, etc.
- **Multi-selection**: Select multiple APIs by entering comma-separated numbers (e.g., "1,3,5")
- **Save responses**: Optionally save API responses to `./output/` directory as JSON files
- **Rate limiting**: Automatically adds delays between API calls to avoid 429 errors
- **Rich formatting**: Pretty-printed JSON responses with syntax highlighting
- **Auto-setup**: Handles virtual environment and dependency installation automatically

### Example Usage

```bash
$ ./perform.sh

🦦 OtterAI API Explorer
┌────────┬─────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────┐
│ Option │ API Name                                    │ Description                                                      │
├────────┼─────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┤
│ [1]    │ abstract_summary                            │ Get abstract summary (placeholder - not implemented in API)     │
│ [2]    │ applied_speech_template                     │ Get applied speech template (placeholder - not implemented in API)│
│ [3]    │ available_speeches                          │ Get all speeches (available_speeches)                           │
│ [4]    │ get_user                                    │ Get current user information                                     │
│ [5]    │ get_speakers                                │ Get all speakers                                                │
└────────┴─────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┘

Enter API numbers (comma-separated) or 'done' to continue [done]: 3,4,5
✅ Added: available_speeches
✅ Added: get_user  
✅ Added: get_speakers

Would you like to save the responses to './output'? [y/N]: y

🔐 Logging in to OtterAI...
✅ Login successful!

🚀 Starting API calls...
🔄 Calling available_speeches...
📡 API Response for available_speeches:
[JSON response with syntax highlighting]
💾 Saved response to ./output/available_speeches.json

⏱️ Waiting 2 seconds to avoid rate limits...
🔄 Calling get_user...
...
```

### Prerequisites

Create a `.env` file in the project root with your Otter.ai credentials:

```plaintext
OTTERAI_USERNAME=your_username
OTTERAI_PASSWORD=your_password
TEST_OTTERAI_SPEECH_OTID=your_test_speech_otid
```

The interactive runner will automatically install dependencies and handle authentication.

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

⚠️ **Important**: This project has three types of tests:

- **Unit tests**: Mock tests that don't hit the API (safe to run)
- **Mock API tests**: Comprehensive tests with mock data (safe to run)
- **Performance tests**: Memory and speed tests with large datasets (safe to run)
- **Integration tests**: Tests that make real API calls (can cause rate limits)

### Running Tests Safely

```bash
# Run only unit tests (recommended for development)
pytest tests/ -m 'not integration'

# Run comprehensive mock tests with full coverage
pytest tests/test_mock_api_responses.py -v

# Run performance tests
pytest tests/test_performance.py -v

# Run a single integration test
pytest tests/test_otterai.py::test_get_user -s

# See all available tests
pytest tests/ --collect-only
```

### Test Coverage

The test suite includes:

- **17 mock API tests** covering all structured endpoints
- **7 performance tests** with large datasets and memory efficiency
- **33 unit tests** covering all functionality
- **12 integration tests** for real API validation

### Mock Tests

The mock tests use generic, non-PII data and cover:

- All structured API endpoints
- Error handling scenarios
- Edge cases and optional field handling
- Network errors and JSON parsing errors
- Pydantic validation errors
- Empty lists and null values

### Performance Tests

Performance tests ensure:

- Large datasets (1000+ items) process within 1-2 seconds
- Complex nested structures are handled efficiently
- Memory usage remains reasonable with large objects
- Serialization performance is optimized

### Rate Limiting Warning

Running all integration tests together **will cause 429 rate limit errors** from the Otter.ai API. The test suite will warn you if you attempt this:

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
