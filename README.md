# 🎙️ Synthetic Radio Host
## AI-Powered Audio Generation System

Transform Wikipedia articles into natural Hinglish conversations and generate high-quality audio files using AI! This innovative system combines Large Language Models (LLM), Natural Language Processing (NLP), and Text-to-Speech (TTS) technology to create an end-to-end content generation pipeline.

---

## ✨ Features

- 🔍 **Wikipedia Integration**: Automatically fetches article summaries from Wikipedia
- 🤖 **AI-Powered Translation**: Converts English text to natural Hinglish dialogue using Ollama LLM
- 🎭 **Multi-Voice Audio**: Creates realistic conversations using alternating voices via ElevenLabs TTS
- 💻 **Dual Interface**: Supports both command-line (CLI) and web-based (Streamlit) interfaces
- 🎵 **Audio Processing**: Advanced audio sanitization and normalization
- 📝 **NLP Processing**: Intelligent sentence tokenization and text processing
- 🛡️ **Error Handling**: Comprehensive error handling and validation
- ✅ **Well Tested**: 57+ unit test cases ensuring reliability

---

## 🎯 Use Cases

- **Content Creation**: Generate podcast-style content from any Wikipedia topic
- **Educational Content**: Create audio lessons in Hinglish
- **Accessibility**: Convert text content to audio format
- **Multilingual Content**: Bridge English and Hindi languages naturally
- **Radio Production**: Automated radio show content generation

---

## 🏗️ System Architecture

```
User Input (Topic)
    ↓
Wikipedia API → English Text
    ↓
NLTK Tokenization → Sentence List
    ↓
Ollama LLM → Hinglish Conversation
    ↓
Text Processing → Dialogue Lines
    ↓
ElevenLabs TTS → Audio Chunks (Alternating Voices)
    ↓
Audio Processing → Normalized Audio
    ↓
Output: GeneratedAudio.wav
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Ollama** installed and running ([Download](https://ollama.ai))
- **ElevenLabs API** account ([Sign up](https://elevenlabs.io))
- **Internet connection** for API calls

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/synthetic-radio-host.git
   cd synthetic-radio-host
   ```

2. **Install Ollama and download model**
   ```bash
   # Install Ollama (visit https://ollama.ai for your OS)
   # Then pull the model
   ollama pull llama3:8b
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Set environment variables**
   
   **Windows (PowerShell):**
   ```powershell
   $env:ELEVENLABS_API_KEY="your_api_key_here"
   $env:ELEVENLABS_voice_id_A="your_voice_id_A_here"
   $env:ELEVENLABS_voice_id_B="your_voice_id_B_here"
   ```
   
   **Linux/macOS:**
   ```bash
   export ELEVENLABS_API_KEY="your_api_key_here"
   export ELEVENLABS_voice_id_A="your_voice_id_A_here"
   export ELEVENLABS_voice_id_B="your_voice_id_B_here"
   ```
   
   **Permanent Setup (Windows):**
   - System Properties → Environment Variables → Add User Variables
   
   **Permanent Setup (Linux/macOS):**
   - Add to `~/.bashrc` or `~/.zshrc`

5. **Get ElevenLabs credentials**
   - Sign up at [ElevenLabs](https://elevenlabs.io)
   - Get API key from dashboard
   - Get Voice IDs from Voice Library

---

## 📖 Usage

### Command-Line Interface (CLI)

1. **Configure script mode** (if needed)
   ```python
   # Edit SyntheticRadioHost.py, line 61
   stlit = False  # Set to False for CLI mode
   ```

2. **Run the script**
   ```bash
   python SyntheticRadioHost.py --text "Artificial Intelligence"
   ```

3. **Output**
   - Generated audio file: `GeneratedAudio.wav`
   - Console output with progress updates

### Streamlit Web Interface

1. **Configure script mode**
   ```python
   # Edit SyntheticRadioHost.py, line 61
   stlit = True  # Set to True for Streamlit mode
   ```

2. **Run Streamlit**
   ```bash
   streamlit run SyntheticRadioHost.py
   ```

3. **Access the interface**
   - Open browser at `http://localhost:8501`
   - Enter topic in text input
   - Click "Search" button
   - View progress and download audio

### Example Usage

```bash
# Generate audio about Python programming
python SyntheticRadioHost.py --text "Python Programming"

# Generate audio about Machine Learning
python SyntheticRadioHost.py --text "Machine Learning"

# Generate audio about Space Exploration
python SyntheticRadioHost.py --text "Space Exploration"
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM Framework** | Ollama (llama3:8b) |
| **LLM Integration** | LangChain Ollama |
| **Text-to-Speech** | ElevenLabs API |
| **Web Framework** | Streamlit |
| **NLP Library** | NLTK |
| **Audio Processing** | NumPy, SoundFile |
| **Data Source** | Wikipedia API |
| **Language** | Python 3.x |

---

## 📁 Project Structure

```
synthetic-radio-host/
├── SyntheticRadioHost.py          # Main application file
├── test_synthetic_radio_host.py   # Unit test suite
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── TECHNICAL_DESIGN_DOCUMENT.md    # Technical documentation
├── UNIT_TEST_CASE_DOCUMENT.md      # Test case specifications
├── TEST_README.md                  # Test documentation
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── YOUTUBE_DEMO_SCRIPT.md          # Video demo script
├── VIDEO_PRODUCTION_GUIDE.md      # Video production guide
└── GeneratedAudio.wav             # Output file (generated)
```

---

## 🧪 Testing

The project includes comprehensive unit tests with 57+ test cases covering all functions, edge cases, and error handling.

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
pytest test_synthetic_radio_host.py -v

# Run with coverage
pytest test_synthetic_radio_host.py --cov=SyntheticRadioHost --cov-report=html

# Run specific test class
pytest test_synthetic_radio_host.py::TestOllamaStatus -v
```

### Test Coverage

- **Function Coverage**: 100% (9/9 functions)
- **Line Coverage**: >85%
- **Branch Coverage**: >80%

See [TEST_README.md](TEST_README.md) for detailed test documentation.

---

## 📚 Documentation

- **[Technical Design Document](TECHNICAL_DESIGN_DOCUMENT.md)**: Complete system architecture and design
- **[Unit Test Cases](UNIT_TEST_CASE_DOCUMENT.md)**: Detailed test specifications
- **[Setup Guide](SETUP_GUIDE.md)**: Step-by-step installation instructions
- **[Test Documentation](TEST_README.md)**: Testing guide and coverage

---

## 🔧 Configuration

### LLM Model

Change the LLM model in `SyntheticRadioHost.py`:

```python
# Line 63
LLM_Model = "llama3:8b"  # Options: llama3:8b, llama3:70b, mistral, etc.
```

### Interface Mode

Switch between CLI and Streamlit:

```python
# Line 61
stlit = False  # False for CLI, True for Streamlit
```

---

## 🐛 Troubleshooting

### Ollama Connection Failed

```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Missing NLTK Data

```bash
python -c "import nltk; nltk.download('punkt')"
```

### Environment Variables Not Found

- Verify variables are set: `echo $ELEVENLABS_API_KEY` (Linux/macOS) or `echo $env:ELEVENLABS_API_KEY` (Windows PowerShell)
- Restart terminal/IDE after setting variables
- Use system environment variables for permanent setup

### Model Not Found

```bash
ollama pull llama3:8b
ollama list  # Verify model exists
```

### Audio Generation Fails

- Verify ElevenLabs API key is valid
- Check API quota/limits
- Verify voice IDs are correct
- Check internet connection

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Hemant S Rathore**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for providing the LLM framework
- [ElevenLabs](https://elevenlabs.io) for the text-to-speech API
- [Wikipedia](https://www.wikipedia.org) for the content source
- [NLTK](https://www.nltk.org) for natural language processing
- [Streamlit](https://streamlit.io) for the web framework

---

## 📊 Project Status

- ✅ Core functionality implemented
- ✅ Unit tests (57+ test cases)
- ✅ Documentation complete
- ✅ CLI and Web interfaces
- ✅ Error handling and validation
- 🔄 Continuous improvements

---

## 🎥 Demo Video

Watch the demo video: [YouTube Link]()

---

## ⭐ Show Your Support

If you find this project useful, please give it a ⭐ on GitHub!

---

## 📧 Contact

For questions, suggestions, or collaborations, please open an issue or contact the author.

---

**Made with ❤️ for the AI/ML Innovation Track**
