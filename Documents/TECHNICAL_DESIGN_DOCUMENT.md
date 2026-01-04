# Technical Design Document
## Synthetic Radio Host - AI-Powered Audio Generation System

**Version:** 1.0  
**Date:** December 2025  
**Author:** Hemant S Rathore

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Track Selection](#2-track-selection)
3. [System Architecture](#3-system-architecture)
4. [Setup and Deployment Instructions](#4-setup-and-deployment-instructions)
5. [Code Explanations](#5-code-explanations)
6. [Assumptions and Constraints](#6-assumptions-and-constraints)
7. [Future Enhancements](#7-future-enhancements)

---

## 1. Project Overview

### 1.1 Purpose

The **Synthetic Radio Host** is an AI-powered system that automatically generates synthetic radio-style audio content from Wikipedia articles. The system transforms English text into natural Hinglish (Hindi-English) conversations between two speakers and converts them into high-quality audio files using advanced text-to-speech technology.

### 1.2 Key Features

- **Wikipedia Integration**: Automatically fetches article summaries from Wikipedia
- **AI-Powered Translation**: Converts English text to natural Hinglish dialogue using Large Language Models (LLM)
- **Multi-Voice Audio Generation**: Creates realistic conversations using alternating voices
- **Dual Interface Modes**: Supports both web-based (Streamlit) and command-line interfaces
- **Audio Processing**: Advanced audio sanitization and normalization
- **Natural Language Processing**: Sentence tokenization and intelligent text processing

### 1.3 Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM Framework** | Ollama (llama3:8b) |
| **LLM Integration** | LangChain Ollama |
| **Text-to-Speech** | ElevenLabs API |
| **Web Framework** | Streamlit (optional) |
| **NLP Library** | NLTK |
| **Audio Processing** | NumPy, SoundFile |
| **Data Source** | Wikipedia API |
| **Language** | Python 3.x |

### 1.4 Use Cases

- **Content Creation**: Generate podcast-style content from any Wikipedia topic
- **Educational Content**: Create audio lessons in Hinglish
- **Accessibility**: Convert text content to audio format
- **Multilingual Content**: Bridge English and Hindi languages naturally
- **Radio Production**: Automated radio show content generation

---

## 2. Track Selection

### 2.1 Selected Track

**AI/ML Innovation Track** - Natural Language Processing and Audio Synthesis

### 2.2 Track Justification

This project aligns with the AI/ML Innovation track because it:

1. **Leverages Advanced AI Models**: Utilizes state-of-the-art LLM (Ollama) for natural language understanding and generation
2. **NLP Innovation**: Implements sophisticated text processing, translation, and conversation generation
3. **Multimodal AI**: Combines NLP with audio synthesis for complete content generation pipeline
4. **Real-world Application**: Solves practical problems in content creation and accessibility
5. **Technical Complexity**: Integrates multiple AI services (LLM, TTS) with custom processing logic

### 2.3 Innovation Highlights

- **Hinglish Conversion**: Unique approach to converting English to natural Hinglish dialogue
- **Conversational AI**: Generates realistic two-speaker conversations from factual content
- **End-to-End Automation**: Complete pipeline from topic input to audio output
- **Intelligent Voice Alternation**: Creates natural dialogue flow with voice switching

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
├──────────────────────┬──────────────────────────────────────────┤
│   Streamlit Web UI   │         Command Line Interface           │
│   (stlit = True)     │         (stlit = False)                  │
└──────────┬───────────┴──────────────────┬──────────────────────┘
           │                               │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │    Input Validation Module     │
           │  (Topic: 3-70 characters)     │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   Wikipedia API Integration    │
           │  fetch_article_from_wiki()     │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   Text Processing Module      │
           │   sentence_token()            │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   LLM Service (Ollama)        │
           │   hinglish_converter()        │
           │   - Conversation_Prompt()     │
           │   - OllamaLLM Integration     │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   Text Post-Processing        │
           │   sentence_splitter()          │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   ElevenLabs TTS API          │
           │   generate_audio()            │
           │   - Voice Alternation         │
           │   - Audio Chunk Processing    │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │   Audio Processing Module    │
           │   sanitize_audio()            │
           │   - Stereo to Mono            │
           │   - Normalization             │
           └───────────────┬───────────────┘
                           │
           ┌───────────────▼───────────────┐
           │      Output Generation        │
           │   GeneratedAudio.wav          │
           └───────────────────────────────┘
```

### 3.2 Detailed System Flow Diagram

```
START
  │
  ├─► Check Ollama Status
  │   └─► [Ollama_Status()]
  │       ├─► Success → Continue
  │       └─► Fail → Exit
  │
  ├─► Get User Input (Topic)
  │   ├─► Streamlit: Text Input
  │   └─► CLI: --text argument
  │
  ├─► Validate Input
  │   └─► Length: 3-70 characters
  │
  ├─► Fetch Wikipedia Article
  │   └─► [fetch_article_from_wiki()]
  │       ├─► Extract first 500 chars
  │       └─► Return summary or None
  │
  ├─► Tokenize Sentences
  │   └─► [sentence_token()]
  │       └─► NLTK sent_tokenize()
  │
  ├─► Convert to Hinglish
  │   └─► [hinglish_converter()]
  │       ├─► Initialize OllamaLLM
  │       ├─► For each sentence:
  │       │   ├─► Get Conversation_Prompt()
  │       │   └─► LLM.invoke() → Hinglish
  │       └─► [sentence_splitter()]
  │
  ├─► Get API Credentials
  │   └─► [Get_Key_Env_varibles()]
  │       ├─► ELEVENLABS_API_KEY
  │       ├─► ELEVENLABS_voice_id_A
  │       └─► ELEVENLABS_voice_id_B
  │
  ├─► Generate Audio
  │   └─► [generate_audio()]
  │       ├─► Initialize ElevenLabs Client
  │       ├─► For each Hinglish line:
  │       │   ├─► Alternate Voice ID
  │       │   ├─► TTS.convert() → Audio Bytes
  │       │   ├─► Read Audio (SoundFile)
  │       │   └─► [sanitize_audio()]
  │       ├─► Concatenate Audio Chunks
  │       └─► Write WAV File
  │
  └─► END (GeneratedAudio.wav)
```

### 3.3 Component Interaction Diagram

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Wikipedia  │◄────────┤  fetch_      │         │   NLTK       │
│     API      │         │  article_    │         │  Tokenizer   │
└──────────────┘         │  from_wiki() │         └──────────────┘
                         └──────┬───────┘                ▲
                                │                        │
                                ▼                        │
                         ┌──────────────┐               │
                         │  sentence_   │───────────────┘
                         │  token()     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐         ┌──────────────┐
                         │  hinglish_   │◄────────┤   Ollama     │
                         │  converter() │         │   LLM        │
                         └──────┬───────┘         │  (llama3:8b) │
                                │                 └──────────────┘
                                ▼
                         ┌──────────────┐
                         │  sentence_   │
                         │  splitter()  │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐         ┌──────────────┐
                         │  generate_   │◄────────┤  ElevenLabs  │
                         │  audio()     │         │     API      │
                         └──────┬───────┘         └──────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  sanitize_   │
                         │  audio()     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Generated   │
                         │  Audio.wav   │
                         └──────────────┘
```

### 3.4 Data Flow Diagram

```
Input: Topic String
  │
  ├─► [Wikipedia] → English Text (500 chars)
  │
  ├─► [NLTK] → Sentence List
  │
  ├─► [Ollama LLM] → Hinglish Conversation
  │   └─► Prompt Engineering
  │   └─► Temperature: 0.35
  │   └─► Top-p: 0.9
  │   └─► Top-k: 40
  │
  ├─► [Text Processing] → Dialogue Lines
  │
  ├─► [ElevenLabs TTS] → Audio Chunks
  │   └─► Voice A (Line 1, 3, 5...)
  │   └─► Voice B (Line 2, 4, 6...)
  │   └─► Voice Settings:
  │       ├─► Stability: 0.5
  │       ├─► Similarity: 0.6
  │       ├─► Style: 0.4
  │       └─► Model: eleven_v3
  │
  ├─► [Audio Processing] → Normalized Audio
  │   └─► Stereo → Mono
  │   └─► Sample Rate: 44100 Hz
  │
  └─► Output: GeneratedAudio.wav (PCM_16)
```

---

## 4. Setup and Deployment Instructions

### 4.1 Prerequisites

#### 4.1.1 System Requirements

- **Operating System**: Windows 10/11, Linux, or macOS
- **Python Version**: Python 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for LLM)
- **Storage**: At least 5GB free space (for Ollama models)
- **Internet Connection**: Required for API calls and model downloads

#### 4.1.2 Software Dependencies

1. **Ollama** (Local LLM Service)
   - Download from: https://ollama.ai
   - Install and start the service
   - Pull the model: `ollama pull llama3:8b`

2. **Python Packages** (Install via pip)
   ```bash
   pip install nltk langchain-ollama wikipedia elevenlabs numpy soundfile streamlit requests
   ```

3. **NLTK Data** (Download after installation)
   ```python
   import nltk
   nltk.download('punkt')
   ```

### 4.2 Installation Steps

#### Step 1: Install Ollama

**Windows:**
```powershell
# Download installer from https://ollama.ai/download
# Run the installer
# Verify installation
ollama --version
```

**Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Step 2: Download LLM Model

```bash
ollama pull llama3:8b
```

Verify the model is available:
```bash
ollama list
```

#### Step 3: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install packages
pip install nltk langchain-ollama wikipedia elevenlabs numpy soundfile streamlit requests
```

#### Step 4: Download NLTK Data

```python
python -c "import nltk; nltk.download('punkt')"
```

#### Step 5: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:ELEVENLABS_API_KEY="your_api_key_here"
$env:ELEVENLABS_voice_id_A="your_voice_id_A_here"
$env:ELEVENLABS_voice_id_B="your_voice_id_B_here"
```

**Windows (Command Prompt):**
```cmd
set ELEVENLABS_API_KEY=your_api_key_here
set ELEVENLABS_voice_id_A=your_voice_id_A_here
set ELEVENLABS_voice_id_B=your_voice_id_B_here
```

**Linux/macOS:**
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
export ELEVENLABS_voice_id_B="your_voice_id_A_here"
export ELEVENLABS_voice_id_B="your_voice_id_B_here"
```

**Permanent Setup (Linux/macOS):**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
export ELEVENLABS_voice_id_A="your_voice_id_A_here"
export ELEVENLABS_voice_id_B="your_voice_id_B_here"
```

**Permanent Setup (Windows):**
1. Open System Properties → Environment Variables
2. Add User Variables:
   - `ELEVENLABS_API_KEY`
   - `ELEVENLABS_voice_id_A`
   - `ELEVENLABS_voice_id_B`

#### Step 6: Get ElevenLabs Credentials

1. Sign up at https://elevenlabs.io
2. Get API key from dashboard
3. Get Voice IDs:
   - Navigate to Voice Library
   - Select two voices
   - Copy Voice IDs from URL or API

### 4.3 Configuration

#### 4.3.1 Configure Script Mode

Edit `SyntheticRadioHost.py`:

```python
# Line 61: Set to True for Streamlit, False for CLI
stlit = False  # or True
```

#### 4.3.2 Configure LLM Model

```python
# Line 63: Change model if needed
LLM_Model = "llama3:8b"  # Options: llama3:8b, llama3:70b, mistral, etc.
```

### 4.4 Running the Application

#### 4.4.1 CLI Mode

```bash
# Ensure Ollama is running
ollama serve

# Run the script
python SyntheticRadioHost.py --text "Artificial Intelligence"
```

#### 4.4.2 Streamlit Mode

```bash
# Set stlit = True in script
# Run Streamlit
streamlit run SyntheticRadioHost.py
```

Access at: `http://localhost:8501`

### 4.5 Verification

#### 4.5.1 Verify Ollama

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test model
ollama run llama3:8b "Hello"
```

#### 4.5.2 Verify Environment Variables

**Windows (PowerShell):**
```powershell
echo $env:ELEVENLABS_API_KEY
```

**Linux/macOS:**
```bash
echo $ELEVENLABS_API_KEY
```

#### 4.5.3 Test Run

```bash
python SyntheticRadioHost.py --text "Python Programming"
# Check for GeneratedAudio.wav in current directory
```

### 4.6 Troubleshooting

#### Issue: Ollama Connection Failed

**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

#### Issue: Missing NLTK Data

**Solution:**
```python
python -c "import nltk; nltk.download('punkt')"
```

#### Issue: Environment Variables Not Found

**Solution:**
- Verify variables are set: `echo $ELEVENLABS_API_KEY`
- Restart terminal/IDE after setting variables
- Use absolute paths in system environment variables

#### Issue: Model Not Found

**Solution:**
```bash
ollama pull llama3:8b
ollama list  # Verify model exists
```

#### Issue: Audio Generation Fails

**Solution:**
- Verify ElevenLabs API key is valid
- Check API quota/limits
- Verify voice IDs are correct
- Check internet connection

---

## 5. Code Explanations

### 5.1 Core Modules

#### 5.1.1 Ollama Status Check (`Ollama_Status()`)

**Purpose**: Verifies Ollama service availability before processing.

**Implementation**:
```python
def Ollama_Status():
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=0.5)
        return True
    except Exception as e:
        print("Ollama connection fail" + str(e))
        return False
```

**Key Points**:
- Uses fast timeout (0.5s) for quick response
- Checks `/api/tags` endpoint (lightweight)
- Returns boolean for conditional execution

#### 5.1.2 Conversation Prompt (`Conversation_Prompt()`)

**Purpose**: Generates system prompt for LLM to convert English to Hinglish.

**Key Features**:
- **Role Definition**: Expert Hinglish Scriptwriter
- **Output Format**: Natural dialogue (50-100 words)
- **Language Rules**: Roman Hindi with English keywords
- **Audio Cues**: Includes expressions like [happy], [laugh], [pause]
- **Constraints**: No meta-tags, direct conversation only

**Prompt Engineering Strategy**:
- Clear role definition for consistent output
- Specific language guidelines for Hinglish
- Audio cue integration for TTS compatibility
- Length constraints for manageable audio chunks

#### 5.1.3 Wikipedia Article Fetching (`fetch_article_from_wiki()`)

**Purpose**: Retrieves article summaries from Wikipedia.

**Implementation Details**:
```python
def fetch_article_from_wiki(topic):
    wiki.set_lang('en')
    data = wiki.page(topic, auto_suggest=False)
    return data.summary[:500]
```

**Key Features**:
- Input sanitization (strip whitespace)
- Language setting (English)
- Auto-suggest disabled for exact matches
- Returns first 500 characters (optimal for processing)
- Error handling for missing articles

#### 5.1.4 Sentence Tokenization (`sentence_token()`)

**Purpose**: Splits text into individual sentences using NLTK.

**Implementation**:
```python
corpus_token = sent_tokenize(corpus, language='english')
```

**Why NLTK?**:
- Industry-standard sentence tokenization
- Handles complex punctuation
- Language-specific rules
- Reliable for English text

**Processing Flow**:
1. Input validation (non-empty string)
2. NLTK tokenization
3. Returns list of sentences
4. Error handling with empty list fallback

#### 5.1.5 Hinglish Conversion (`hinglish_converter()`)

**Purpose**: Converts English sentences to Hinglish dialogue using LLM.

**LLM Configuration**:
```python
llm = OllamaLLM(
    model=LLM_Model,
    temperature=0.35,      # Lower = more deterministic
    top_p=0.9,             # Nucleus sampling
    top_k=40,              # Top-k sampling
    repeat_penalty=1.18    # Reduce repetition
)
```

**Processing Loop**:
```python
for sentence in data:
    Conversation = llm.invoke([
        {"role": "system", "content": prompt},
        {"role": "user", "content": sentence}
    ])
    HinglishData.append(Conversation)
```

**Key Design Decisions**:
- **Temperature 0.35**: Balances creativity and consistency
- **System + User Messages**: Clear role separation
- **Per-sentence Processing**: Maintains context while processing chunks
- **Post-processing**: Splits output for audio generation

#### 5.1.6 Sentence Splitting (`sentence_splitter()`)

**Purpose**: Splits LLM output into individual dialogue lines.

**Implementation**:
```python
for line in HinglishData:
    Linesplit = line.split('\n\n')
    for line2 in Linesplit:
        sent_token.append(line2)
```

**Why Double Newline?**:
- LLM typically separates dialogue with `\n\n`
- Preserves natural conversation breaks
- Prepares for voice alternation

#### 5.1.7 Audio Sanitization (`sanitize_audio()`)

**Purpose**: Normalizes audio data for concatenation.

**Processing Steps**:
1. **Type Conversion**: `np.asarray(audio_np)`
2. **Scalar Rejection**: Rejects 0-dimensional arrays
3. **Stereo to Mono**: `audio_np.mean(axis=1)` if 2D
4. **Empty Check**: Rejects empty arrays
5. **Reshape**: Flattens to 1D array

**Why This Matters**:
- Ensures consistent audio format
- Prevents concatenation errors
- Handles different input formats gracefully

#### 5.1.8 Environment Variables (`Get_Key_Env_varibles()`)

**Purpose**: Retrieves API credentials securely.

**Security Best Practices**:
- Uses environment variables (not hardcoded)
- Validates all required variables
- Exits gracefully if missing
- Returns tuple for easy unpacking

**Required Variables**:
- `ELEVENLABS_API_KEY`: Authentication
- `ELEVENLABS_voice_id_A`: First speaker
- `ELEVENLABS_voice_id_B`: Second speaker

#### 5.1.9 Audio Generation (`generate_audio()`)

**Purpose**: Converts Hinglish text to audio using ElevenLabs TTS.

**Voice Alternation Logic**:
```python
VoiceID_Toggle = True
for audioLine in AudioData:
    if VoiceID_Toggle:
        voice = Keys[1]  # Voice A
    else:
        voice = Keys[2]  # Voice B
    VoiceID_Toggle = not VoiceID_Toggle
```

**Voice Settings**:
```python
voice_settings={
    "stability": 0.5,           # Voice consistency
    "similarity_boost": 0.6,     # Voice similarity
    "style": 0.4,                # Expression level
    "use_speaker_boost": True    # Enhanced clarity
}
```

**Audio Processing Pipeline**:
1. Initialize ElevenLabs client
2. For each line:
   - Select voice (alternating)
   - Convert text to speech
   - Read audio bytes
   - Sanitize audio
   - Append to chunks
3. Concatenate all chunks
4. Write WAV file (44100 Hz, PCM_16)

**Error Handling**:
- Skips empty chunks
- Continues on individual failures
- Validates final output before saving

### 5.2 Main Execution Flow

#### 5.2.1 Streamlit Mode

```python
if stlit:
    if not Ollama_Status():
        sys.exit(0)
    
    st.title("Synthetic Audio Generation tool")
    Name = st.text_input("Enter Article topic", max_chars=70)
    
    if st.button("Search"):
        # Validation → Fetch → Process → Generate
```

**Features**:
- Interactive web interface
- Real-time progress updates
- Error messages in UI
- Input validation with feedback

#### 5.2.2 CLI Mode

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    
    # Validation → Fetch → Process → Generate
```

**Features**:
- Command-line argument parsing
- Scriptable/automated execution
- Console output for progress
- Exit codes for error handling

### 5.3 Design Patterns

#### 5.3.1 Error Handling Strategy

- **Graceful Degradation**: Continues processing valid chunks
- **User Feedback**: Clear error messages (UI/console)
- **Validation**: Input validation at each stage
- **Fallback**: Returns None/empty list on errors

#### 5.3.2 Dual Mode Architecture

- **Configuration Flag**: `stlit` boolean
- **Conditional Execution**: Same logic, different I/O
- **Code Reusability**: Functions work in both modes
- **User Choice**: Web UI or CLI based on preference

#### 5.3.3 Modular Design

- **Single Responsibility**: Each function has one purpose
- **Separation of Concerns**: Data fetching, processing, generation
- **Reusability**: Functions can be used independently
- **Testability**: Each module can be tested separately

---

## 6. Assumptions and Constraints

### 6.1 Assumptions

1. **Ollama Service Availability**
   - Assumes Ollama is installed and running locally
   - Assumes model `llama3:8b` is available
   - Assumes service is accessible on `localhost:11434`

2. **Internet Connectivity**
   - Assumes stable internet for Wikipedia API
   - Assumes ElevenLabs API is accessible
   - Assumes no firewall blocking API calls

3. **Environment Variables**
   - Assumes user has ElevenLabs account
   - Assumes API key and voice IDs are valid
   - Assumes environment variables are properly set

4. **Input Quality**
   - Assumes Wikipedia article exists for topic
   - Assumes topic is in English
   - Assumes topic is 3-70 characters

5. **System Resources**
   - Assumes sufficient RAM for LLM (8GB+)
   - Assumes disk space for audio files
   - Assumes Python 3.8+ installed

6. **Language Support**
   - Assumes English Wikipedia articles
   - Assumes Hinglish output is acceptable
   - Assumes Roman Hindi script

### 6.2 Constraints

1. **Wikipedia Article Length**
   - **Constraint**: Only first 500 characters used
   - **Reason**: Optimal for LLM processing
   - **Impact**: Longer articles truncated

2. **Topic Length**
   - **Constraint**: 3-70 characters
   - **Reason**: Validation and API limits
   - **Impact**: Very long topics rejected

3. **Audio Format**
   - **Constraint**: Fixed WAV format (PCM_16, 44100 Hz)
   - **Reason**: Compatibility and quality
   - **Impact**: No format customization

4. **Voice Alternation**
   - **Constraint**: Strict A-B-A-B pattern
   - **Reason**: Simulates two speakers
   - **Impact**: No dynamic voice selection

5. **LLM Model**
   - **Constraint**: Fixed to `llama3:8b` (configurable)
   - **Reason**: Default model availability
   - **Impact**: Quality depends on model

6. **Processing Time**
   - **Constraint**: Sequential processing
   - **Reason**: Simplicity and API limits
   - **Impact**: Slower for long articles

7. **Error Recovery**
   - **Constraint**: Limited retry logic
   - **Reason**: Simplicity
   - **Impact**: Manual retry on failures

8. **Language Limitations**
   - **Constraint**: English → Hinglish only
   - **Reason**: Prompt engineering for specific pair
   - **Impact**: Other languages not supported

### 6.3 Known Limitations

1. **No Article Disambiguation**: Exact topic match required
2. **Fixed Audio Settings**: No user customization
3. **No Batch Processing**: One topic at a time
4. **No Audio Editing**: No post-processing options
5. **Limited Error Recovery**: Basic error handling
6. **No Caching**: Re-fetches on every run
7. **No Progress Persistence**: Can't resume interrupted runs

---

## 7. Future Enhancements

### 7.1 Short-term Improvements

1. **Enhanced Error Handling**
   - Retry logic for API failures
   - Better error messages
   - Graceful degradation

2. **Input Validation**
   - Article disambiguation
   - Topic suggestions
   - Input sanitization
---

## 8. Testing and Quality Assurance

### 8.1 Test Suite Overview

A comprehensive unit test suite has been developed to ensure code robustness, reliability, and proper error handling. The test suite covers all functions with various scenarios including edge cases, error conditions, and integration tests.

### 8.2 Test Coverage

**Total Test Cases**: 62+ comprehensive unit tests covering:

- **Function Unit Tests**: Individual function testing with mocks
- **Integration Tests**: End-to-end workflow validation
- **Edge Case Tests**: Boundary conditions and extreme inputs
- **Error Handling Tests**: Exception handling and recovery
- **Mock Coverage**: All external APIs properly mocked

### 8.3 Test Organization

Tests are organized into test classes:

1. **TestOllamaStatus** - Connection and status checks
2. **TestConversationPrompt** - Prompt generation validation
3. **TestFetchArticleFromWiki** - Wikipedia integration
4. **TestSentenceSplitter** - Text splitting logic
5. **TestSentenceToken** - Tokenization functionality
6. **TestHinglishConverter** - LLM conversion process
7. **TestSanitizeAudio** - Audio processing and normalization
8. **TestGetKeyEnvVariables** - Environment variable handling
9. **TestGenerateAudio** - Audio generation pipeline
10. **TestIntegrationScenarios** - Complete workflows
11. **TestEdgeCases** - Boundary conditions
12. **TestErrorHandling** - Error recovery mechanisms

### 8.4 Running Tests

**Install test dependencies:**
```bash
pip install pytest pytest-cov pytest-mock
```

**Run all tests:**
```bash
pytest test_synthetic_radio_host.py -v
```

**Run with coverage:**
```bash
pytest test_synthetic_radio_host.py --cov=SyntheticRadioHost --cov-report=html
```

**Run specific test class:**
```bash
pytest test_synthetic_radio_host.py::TestOllamaStatus -v
```

### 8.5 Test Features

- **Mocking Strategy**: All external dependencies (Ollama, Wikipedia, ElevenLabs) are mocked
- **Isolation**: Tests are independent and can run in any order
- **No External Services**: Tests run without requiring actual API connections
- **Comprehensive Coverage**: Tests cover success, failure, and edge cases
- **CI/CD Ready**: Tests can be integrated into continuous integration pipelines

### 8.6 Test Scenarios

#### Normal Operation
- ✅ Successful API connections
- ✅ Valid input processing
- ✅ Correct output generation
- ✅ Proper data transformations

#### Error Conditions
- ✅ Network failures
- ✅ API errors
- ✅ Invalid inputs
- ✅ Missing dependencies
- ✅ File I/O errors

#### Edge Cases
- ✅ Empty inputs
- ✅ Very large inputs
- ✅ Boundary values
- ✅ Type mismatches
- ✅ None/null values

### 8.7 Test Documentation

Detailed test documentation is available in `TEST_README.md` including:
- Test structure and organization
- Running instructions
- Mocking strategies
- Adding new tests
- Troubleshooting guide

### 8.8 Quality Metrics

- **Code Coverage Target**: >80%
- **Test Execution Time**: <5 seconds
- **Test Independence**: All tests can run independently
- **Mock Coverage**: 100% of external APIs mocked

---

## Appendix A: File Structure

```
Final-2/
├── SyntheticRadioHost.py           # Main application file
├── TECHNICAL_DESIGN_DOCUMENT.md    # This document
├── test_synthetic_radio_host.py    # Comprehensive unit test suite
├── TEST_README.md                   # Test documentation
├── requirements.txt                 # Python dependencies
├── SETUP_GUIDE.md                  # Quick setup guide
└── GeneratedAudio.wav             # Output file (generated)
```

## Appendix B: API Endpoints Used

1. **Ollama API**
   - Endpoint: `http://localhost:11434/api/tags`
   - Method: GET
   - Purpose: Service status check

2. **Wikipedia API**
   - Library: `wikipedia` (Python)
   - Method: `wiki.page()`
   - Purpose: Article fetching

3. **ElevenLabs API**
   - Endpoint: Text-to-Speech conversion
   - Method: `client.text_to_speech.convert()`
   - Purpose: Audio generation

## Appendix C: Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `ELEVENLABS_API_KEY` | API authentication key | `sk-...` |
| `ELEVENLABS_voice_id_A` | First voice ID | `21m00Tcm4TlvDq8ikWAM` |
| `ELEVENLABS_voice_id_B` | Second voice ID | `AZnzlk1XvdvUeBnXmlld` |

## Appendix D: Dependencies List

```
nltk>=3.8
langchain-ollama>=0.1.0
wikipedia>=1.4.0
elevenlabs>=0.2.0
numpy>=1.24.0
soundfile>=0.12.0
streamlit>=1.28.0
requests>=2.31.0
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
```

---

**Document End**