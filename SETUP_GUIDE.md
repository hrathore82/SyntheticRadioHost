# Quick Setup Guide
## Synthetic Radio Host

### Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Ollama installed and running
- [ ] Internet connection
- [ ] ElevenLabs account with API key

### Quick Start (5 Minutes)

#### 1. Install Ollama
```bash
# Visit https://ollama.ai and download for your OS
# Or use:
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Download LLM Model
```bash
ollama pull llama3:8b
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

#### 4. Set Environment Variables

**Windows:**
```powershell
$env:ELEVENLABS_API_KEY="your_key"
$env:ELEVENLABS_voice_id_A="voice_id_1"
$env:ELEVENLABS_voice_id_B="voice_id_2"
```

**Linux/macOS:**
```bash
export ELEVENLABS_API_KEY="your_key"
export ELEVENLABS_voice_id_A="voice_id_1"
export ELEVENLABS_voice_id_B="voice_id_2"
```

#### 5. Run the Application

**CLI Mode:**
```bash
python SyntheticRadioHost.py --text "Artificial Intelligence"
```

**Streamlit Mode:**
```bash
# Edit line 61: stlit = True
streamlit run SyntheticRadioHost.py
```

### Verify Installation

```bash
# Check Ollama
ollama list

# Test Python packages
python -c "import nltk, langchain_ollama, wikipedia, elevenlabs; print('OK')"

# Test environment variables
echo $ELEVENLABS_API_KEY  # Linux/macOS
echo $env:ELEVENLABS_API_KEY  # Windows PowerShell
```

### Troubleshooting

**Ollama not found:**
```bash
ollama serve  # Start Ollama service
```

**Missing packages:**
```bash
pip install --upgrade -r requirements.txt
```

**Environment variables not working:**
- Restart terminal after setting
- Use system environment variables for permanent setup

### Next Steps

See `TECHNICAL_DESIGN_DOCUMENT.md` for detailed documentation.