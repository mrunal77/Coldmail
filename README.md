# ColdMail Generator

A desktop application for generating personalized cold emails using local Ollama LLM.

## Running as Desktop App (Electron)

### Prerequisites

1. **Python 3.8+** - Download from https://www.python.org/
2. **Node.js** - Download from https://nodejs.org/
3. **Ollama** - Download from https://ollama.ai/ and install a model (e.g., `ollama pull llama2`)

### Installation

```bash
npm install
```

### Run the App

```bash
npm start
```

This will:
1. Start the Flask backend automatically
2. Launch the ColdMail desktop app

### Build Executable

```bash
npm run build
```

This will create an executable in the `dist` folder.

## Running as Web App (Flask only)

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

## Features

- Generate cold emails using local Ollama models
- Connect Gmail or Outlook accounts
- Send emails directly from the app
- Modern dark/light themed UI with glow effects
- Select from multiple Ollama models

## Email Setup

### Gmail
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password at https://myaccount.google.com/apppasswords

### Outlook
1. Enable 2-Factor Authentication on your Microsoft account
2. Generate an App Password at https://account.microsoft.com/security

## Tech Stack

- **Frontend**: Electron
- **Backend**: Flask (Python)
- **AI**: Ollama (local LLM)
- **UI**: HTML/CSS/JavaScript

## License

MIT License - see [LICENSE](LICENSE) file for details.
