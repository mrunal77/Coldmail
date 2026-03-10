# ColdMail Generator

A web application for generating personalized cold emails using local Ollama LLM.

## Features

- Generate cold emails using local Ollama models
- Connect Gmail or Outlook accounts
- Send emails directly from the app
- Modern dark/light themed UI with glow effects
- Select from multiple Ollama models

## Prerequisites

1. **Python 3.8+** - Download from https://www.python.org/
2. **Ollama** - Download from https://ollama.ai/ and install a model (e.g., `ollama pull llama2`)

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## Email Setup

### Gmail
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password at https://myaccount.google.com/apppasswords

### Outlook
1. Enable 2-Factor Authentication on your Microsoft account
2. Generate an App Password at https://account.microsoft.com/security

## Tech Stack

- **Backend**: Flask (Python)
- **AI**: Ollama (local LLM)
- **Frontend**: HTML/CSS/JavaScript

## License

MIT License - see [LICENSE](LICENSE) file for details.
