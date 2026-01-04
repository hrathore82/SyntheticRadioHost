# Unit Test Suite Documentation
## Synthetic Radio Host - Test Coverage

## Overview

This test suite provides comprehensive unit testing for all functions in the SyntheticRadioHost application. The tests ensure robustness, reliability, and proper error handling across all components.

## Test Coverage

### Functions Tested

1. **Ollama_Status()** - 4 test cases
   - Successful connection
   - Connection errors
   - Timeout handling
   - HTTP errors

2. **Conversation_Prompt()** - 3 test cases
   - Return value validation
   - Content verification
   - Consistency checks

3. **fetch_article_from_wiki()** - 7 test cases
   - Successful fetch
   - Article not found
   - Empty/whitespace topics
   - Truncation to 500 chars
   - Whitespace stripping

4. **sentence_splitter()** - 5 test cases
   - Normal splitting
   - Empty lists
   - No double newlines
   - Multiple newlines
   - Empty strings

5. **sentence_token()** - 6 test cases
   - Normal tokenization
   - Empty strings
   - Whitespace-only
   - None input
   - Non-string input
   - Exception handling

6. **hinglish_converter()** - 3 test cases
   - Successful conversion
   - Multiple sentences
   - LLM configuration

7. **sanitize_audio()** - 8 test cases
   - Mono 1D audio
   - Stereo to mono conversion
   - None input
   - Scalar input
   - Empty arrays
   - List input
   - 2D mono
   - Exception handling

8. **Get_Key_Env_varibles()** - 5 test cases
   - Successful retrieval
   - Missing API key
   - Missing voice A
   - Missing voice B
   - Empty API key

9. **generate_audio()** - 8 test cases
   - Successful generation
   - Empty list
   - Client initialization error
   - Voice alternation
   - Empty chunks skipped
   - Invalid chunks skipped
   - Voice settings verification
   - No valid chunks

10. **Integration Tests** - 2 test cases
    - Complete workflow
    - Ollama unavailable

11. **Edge Cases** - 4 test cases
    - Very long text
    - Very long lists
    - Very large arrays
    - Very wide stereo

12. **Error Handling** - 3 test cases
    - Network errors
    - LLM errors
    - File write errors

**Total: 62+ test cases**

## Running the Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-cov pytest-mock
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Running All Tests

**Using pytest (recommended):**
```bash
pytest test_synthetic_radio_host.py -v
```

**Using unittest:**
```bash
python -m pytest test_synthetic_radio_host.py -v
```

**Or directly:**
```bash
python test_synthetic_radio_host.py
```

### Running Specific Test Classes

```bash
# Test only Ollama status
pytest test_synthetic_radio_host.py::TestOllamaStatus -v

# Test only audio functions
pytest test_synthetic_radio_host.py::TestSanitizeAudio -v
pytest test_synthetic_radio_host.py::TestGenerateAudio -v
```

### Running with Coverage

```bash
# Generate coverage report
pytest test_synthetic_radio_host.py --cov=SyntheticRadioHost --cov-report=html

# View coverage in terminal
pytest test_synthetic_radio_host.py --cov=SyntheticRadioHost --cov-report=term
```

Coverage report will be generated in `htmlcov/index.html`

### Running with Verbose Output

```bash
pytest test_synthetic_radio_host.py -v -s
```

## Test Structure

### Test Organization

Tests are organized into classes by function/module:

- `TestOllamaStatus` - Ollama connection tests
- `TestConversationPrompt` - Prompt generation tests
- `TestFetchArticleFromWiki` - Wikipedia integration tests
- `TestSentenceSplitter` - Text splitting tests
- `TestSentenceToken` - Tokenization tests
- `TestHinglishConverter` - LLM conversion tests
- `TestSanitizeAudio` - Audio processing tests
- `TestGetKeyEnvVariables` - Environment variable tests
- `TestGenerateAudio` - Audio generation tests
- `TestIntegrationScenarios` - End-to-end workflow tests
- `TestEdgeCases` - Boundary condition tests
- `TestErrorHandling` - Error recovery tests

### Mocking Strategy

The test suite uses `unittest.mock` to mock external dependencies:

- **Ollama API**: Mocked `requests.get` for connection tests
- **Wikipedia API**: Mocked `wikipedia.page` for article fetching
- **ElevenLabs API**: Mocked `ElevenLabs` client for audio generation
- **NLTK**: Uses real NLTK (no mocking needed for tokenization)
- **File I/O**: Mocked `soundfile` operations
- **Environment Variables**: Mocked `os.environ` for credential tests
- **Streamlit**: Mocked `stlit` flag to avoid UI dependencies

## Test Scenarios Covered

### Normal Operation
- ✅ Successful API connections
- ✅ Valid input processing
- ✅ Correct output generation
- ✅ Proper data transformations

### Error Conditions
- ✅ Network failures
- ✅ API errors
- ✅ Invalid inputs
- ✅ Missing dependencies
- ✅ File I/O errors

### Edge Cases
- ✅ Empty inputs
- ✅ Very large inputs
- ✅ Boundary values
- ✅ Type mismatches
- ✅ None/null values

### Integration
- ✅ Complete workflows
- ✅ Function interactions
- ✅ Data flow validation

## Expected Test Results

When all tests pass, you should see:
```
test_synthetic_radio_host.py::TestOllamaStatus::test_ollama_status_success PASSED
test_synthetic_radio_host.py::TestOllamaStatus::test_ollama_status_connection_error PASSED
...
[62 tests passed]
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - run: pip install -r requirements.txt
      - run: pytest test_synthetic_radio_host.py --cov=SyntheticRadioHost
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `SyntheticRadioHost.py` is in the same directory
   - Check Python path

2. **Mock Errors**
   - Verify mock patches match actual import paths
   - Check for typos in function names

3. **NLTK Data Missing**
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Coverage Not Working**
   - Install pytest-cov: `pip install pytest-cov`
   - Use `--cov` flag correctly

## Best Practices

1. **Run tests before committing code**
2. **Add tests for new features**
3. **Maintain >80% code coverage**
4. **Test edge cases and error conditions**
5. **Keep tests independent and isolated**
6. **Use descriptive test names**
7. **Mock external dependencies**

## Adding New Tests

When adding new functionality:

1. Create a new test class or add to existing
2. Follow naming convention: `test_function_name_scenario`
3. Mock external dependencies
4. Test both success and failure cases
5. Include edge cases
6. Update this README

Example:
```python
class TestNewFunction(unittest.TestCase):
    def test_new_function_success(self):
        """Test successful execution"""
        # Arrange
        input_data = "test"
        
        # Act
        result = srh.new_function(input_data)
        
        # Assert
        self.assertIsNotNone(result)
```

## Test Metrics

- **Total Test Cases**: 62+
- **Code Coverage Target**: >80%
- **Test Execution Time**: <5 seconds
- **Mock Coverage**: All external APIs mocked

## Notes

- Tests are designed to run without external services (Ollama, ElevenLabs)
- All external API calls are mocked
- Tests can run in CI/CD pipelines
- No actual audio files are created during testing
- Environment variables are mocked for testing

