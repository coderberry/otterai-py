# OtterAI Python Client - Structured Data Implementation Spec

## Overview
This specification outlines the implementation of structured data models and API endpoints for the OtterAI Python client. The implementation should be done incrementally to ensure stability and maintainability.

## Project Goals
- Add structured data models using Pydantic for better type safety and validation
- Implement all missing API endpoints found in TEMP.md
- Maintain backward compatibility with existing methods
- Provide comprehensive test coverage for all new functionality

## Technology Stack
- **Pydantic**: For data models and validation
- **Python 3.9+**: Minimum supported version
- **Existing dependencies**: requests, tenacity, requests-toolbelt, python-dotenv

## Implementation Phases

### Phase 1: Foundation Setup
**Priority**: HIGH
**Estimated effort**: 1-2 hours

#### Tasks:
1. **Add Pydantic Dependency**
   - Update `pyproject.toml` to include `pydantic>=2.0.0`
   - Update development dependencies if needed

2. **Create Base Models Module**
   - Create `otterai/models.py` file
   - Implement core base models that are reused across endpoints:
     - `User` - Basic user information (id, name, email, first_name, last_name, avatar_url)
     - `Workspace` - Workspace information (id, name)
     - `Permission` - Generic permission structure
     - `BaseResponse` - Common response wrapper

3. **Update Package Exports**
   - Update `otterai/__init__.py` to export new models
   - Maintain backward compatibility

#### Success Criteria:
- Pydantic is properly installed and importable
- Base models are created and can be instantiated
- All tests pass

### Phase 2: Simple Models Implementation ✅ **COMPLETED**
**Priority**: HIGH
**Estimated effort**: 2-3 hours
**Status**: ✅ **COMPLETED** - 2025-01-08
**Branch**: `phase-2-simple-models`

#### Tasks:
1. **Implement Simple Models** ✅
   - `Contact` - Contact information model with validation for user contact information
   - `Folder` - Folder structure model with creation timestamps and speech counts
   - `MentionCandidate` - Simple user reference model for speech mention functionality

2. **Add Corresponding API Methods** ✅
   - `get_contacts_structured()` - Returns ContactsResponse with list of Contact objects
   - `get_folders_structured()` - Returns FoldersResponse with list of Folder objects
   - `get_speech_mention_candidates_structured()` - Returns MentionCandidatesResponse with list of MentionCandidate objects

3. **Create Basic Tests** ✅
   - Test model creation and validation with real API data structures
   - Test API method responses with integration tests
   - Test error handling for invalid userid cases

#### API Endpoints Implemented:
- ✅ `GET /api/v1/contacts?userid={userid}`
- ✅ `GET /api/v1/folders?userid={userid}`
- ✅ `GET /api/v1/speech_mention_candidates?otid={otid}`

#### Success Criteria:
- ✅ Models validate correctly with real API data
- ✅ New methods return structured objects
- ✅ All tests pass (22 unit tests, 3 integration tests)

#### Additional Accomplishments:
- **Response Wrappers**: Created ContactsResponse, FoldersResponse, and MentionCandidatesResponse models
- **Comprehensive Testing**: Added both unit and integration tests for all new functionality
- **Type Safety**: Full Pydantic validation with proper error handling
- **Documentation**: Complete docstrings with type annotations for all new methods

### Phase 3: Complex Models - Groups and Speakers ✅ **COMPLETED**
**Priority**: MEDIUM
**Estimated effort**: 3-4 hours
**Status**: ✅ **COMPLETED** - 2025-01-08
**Branch**: `phase-3-complex-models`

#### Tasks:
1. **Implement Complex Models** ✅
   - `Group` - Group information with nested user objects (29 fields including complex nested structures)
   - `Speaker` - Speaker information with owner details (8 fields with User object nesting)

2. **Add API Methods** ✅
   - `list_groups_structured()` - Returns GroupsResponse with list of Group objects
   - `get_speakers_structured()` - Returns SpeakersResponse with list of Speaker objects

3. **Enhanced Testing** ✅
   - Test nested object validation with complex Group and Speaker structures
   - Test optional field handling (avatar_url, workspace_id, speaker_email, etc.)
   - Test complex data structures with real API data validation

#### API Endpoints Implemented:
- ✅ `GET /api/v1/list_groups?simple_group=true`
- ✅ `GET /api/v1/speakers?userid={userid}`

#### Success Criteria:
- ✅ Complex nested structures validate correctly
- ✅ Optional fields are handled properly (workspace_id, cover_photo_url, speaker_email, etc.)
- ✅ All existing functionality remains intact

#### Additional Accomplishments:
- **Complex Nested Models**: Successfully implemented Group model with nested User objects (owner, first_member)
- **Optional Field Handling**: Proper validation of optional fields across all models
- **Comprehensive Testing**: Added unit tests for model validation and integration tests for API methods
- **Type Safety**: Full Pydantic validation with proper error handling for complex structures
- **Documentation**: Complete docstrings with detailed field descriptions for all new models
- **PII Security**: Implemented generic test data approach to prevent exposure of personal information

### Phase 4: Speech Templates and Action Items 🚀 **NEXT PHASE**
**Priority**: MEDIUM
**Estimated effort**: 2-3 hours
**Status**: 🚀 **READY TO BEGIN**
**Assigned**: Next implementation phase

#### Tasks:
1. **Implement Models**
   - `SpeechTemplate` - Template structure with permissions
   - `ActionItem` - Action item with assignee/assigner information
   - `AbstractSummary` - Summary data structure

2. **Add API Methods**
   - `get_speech_templates_structured()` - Returns template data
   - `get_speech_action_items_structured()` - Returns action items
   - `get_abstract_summary_structured()` - Returns summary information

3. **Permission Handling**
   - Implement permission validation
   - Handle complex permission structures

#### API Endpoints to Implement:
- `GET /api/v1/speech_templates`
- `GET /api/v1/speech_action_items?otid={otid}`
- `GET /api/v1/abstract_summary?otid={otid}`

#### Success Criteria:
- Permission structures are properly modeled
- Action items with assignee data work correctly
- Summary processing is accurate

### Phase 5: Speech Model - Most Complex
**Priority**: HIGH
**Estimated effort**: 4-5 hours

#### Tasks:
1. **Implement Speech Model**
   - `Speech` - Full speech object with all nested structures
   - `SpeechOutline` - Outline structure with segments
   - `SpeechMetadata` - Metadata structure
   - `ChatStatus` - Chat status information
   - `LinkShare` - Link sharing configuration

2. **Add API Methods**
   - `get_speech_structured()` - Returns structured Speech object
   - `get_available_speeches_structured()` - Returns list of Speech objects

3. **Complex Validation**
   - Handle deeply nested structures
   - Validate timestamps and durations
   - Handle optional complex objects

#### API Endpoints to Implement:
- `GET /api/v1/speech?userid={userid}&otid={otid}`
- `GET /api/v1/available_speeches?funnel={funnel}&page_size={size}&use_serializer={serializer}&source={source}&speech_metadata={metadata}`

#### Success Criteria:
- Full speech object validates correctly
- All nested structures work properly
- Performance is acceptable for large objects

### Phase 6: Migration and Backward Compatibility
**Priority**: MEDIUM
**Estimated effort**: 2-3 hours

#### Tasks:
1. **Update Existing Methods**
   - Add structured response option to existing methods
   - Maintain backward compatibility
   - Add deprecation warnings where appropriate

2. **Enhanced Error Handling**
   - Better error messages for validation failures
   - Graceful handling of API changes

3. **Documentation Updates**
   - Update method docstrings
   - Add type hints throughout
   - Update examples

#### Success Criteria:
- All existing code continues to work
- New structured options are available
- Clear migration path is documented

### Phase 7: Comprehensive Testing and Documentation
**Priority**: HIGH
**Estimated effort**: 3-4 hours

#### Tasks:
1. **Complete Test Suite**
   - Test all models with real API data
   - Test error conditions
   - Test edge cases and optional fields
   - Mock tests for CI/CD

2. **Documentation**
   - Update README with new examples
   - Create migration guide
   - Add type annotation documentation

3. **Performance Testing**
   - Validate performance with large datasets
   - Memory usage testing
   - Optimization where needed

#### Success Criteria:
- 100% test coverage for new functionality
- All documentation is up to date
- Performance meets requirements

## Implementation Guidelines

### Code Quality Standards
- Follow existing code style (Black formatting, line length 88)
- Use type hints throughout
- Comprehensive docstrings for all public methods
- Proper error handling and validation

### Testing Requirements
- Unit tests for all models
- Integration tests for API methods
- Mock tests for offline testing
- Maintain existing test coverage

### Backward Compatibility
- All existing methods must continue to work
- New structured methods should be suffixed with `_structured`
- Deprecation warnings for methods that will be replaced

### Performance Considerations
- Pydantic models should not significantly impact performance
- Large responses should be handled efficiently
- Optional lazy loading for complex nested structures

## Risk Assessment

### High Risk
- **Phase 5 (Speech Model)**: Most complex, potential for performance issues
- **Phase 6 (Migration)**: Risk of breaking existing functionality

### Medium Risk
- **Phase 3 (Complex Models)**: Nested validation complexity
- **Phase 4 (Templates)**: Permission modeling complexity

### Low Risk
- **Phase 1 (Foundation)**: Well-defined scope
- **Phase 2 (Simple Models)**: Straightforward implementation

## Dependencies Between Phases
- Phase 1 must be completed before any other phase
- Phase 2 provides foundation for testing patterns
- Phases 3-5 can be done in parallel after Phase 2
- Phase 6 depends on completion of Phases 3-5
- Phase 7 should be ongoing throughout implementation

## Success Metrics
- All API endpoints from TEMP.md are implemented
- 100% backward compatibility maintained
- Test coverage remains above 90%
- Performance impact is minimal (<10% overhead)
- Documentation is complete and accurate

## Implementation Status

### ✅ Completed Phases
- **Phase 1: Foundation Setup** (2025-01-08)
  - Branch: `phase-1-foundation-setup`
  - Status: Fully completed with additional enhancements
  
- **Phase 2: Simple Models Implementation** (2025-01-08)
  - Branch: `phase-2-simple-models`
  - Status: Fully completed with comprehensive testing

- **Phase 3: Complex Models - Groups and Speakers** (2025-01-08)
  - Branch: `phase-3-complex-models`
  - Status: Fully completed with PII security enhancements

### 🚀 Next Phase
- **Phase 4: Speech Templates and Action Items**
  - Priority: MEDIUM
  - Estimated effort: 2-3 hours
  - Ready to begin immediately

### 📋 Implementation Timeline
- **Phase 1**: ✅ Completed (2025-01-08)
- **Phase 2**: ✅ Completed (2025-01-08)
- **Phase 3**: ✅ Completed (2025-01-08)
- **Phase 4**: 🚀 Ready to start
- **Phase 5**: ⏳ Awaiting Phase 4 completion
- **Phase 6**: ⏳ Awaiting Phases 4-5 completion
- **Phase 7**: ⏳ Ongoing throughout implementation

## Next Steps
1. ✅ ~~Review and approve this specification~~ - COMPLETED
2. ✅ ~~Begin with Phase 1 implementation~~ - COMPLETED
3. ✅ ~~Complete Phase 2 implementation~~ - COMPLETED
4. ✅ ~~Complete Phase 3 implementation~~ - COMPLETED
5. 🚀 **BEGIN PHASE 4**: Speech Templates and Action Items
6. Continue with phases incrementally
7. Regular code reviews after each phase
8. Update specification as needed based on implementation learnings

## Notes for Implementers
- Keep each phase small and focused
- Always work within a branch and not directly on the main branch
- Run full test suite after each phase
- Always format code using black
- Document any deviations from this spec
- Consider creating feature flags for new functionality
- Maintain detailed commit messages for each phase