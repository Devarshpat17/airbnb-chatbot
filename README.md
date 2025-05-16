
# Info Retrieval Project

## Project Structure

```

info\_retrieval\_project/
│
├── venv/                         # Python virtual environment
│
├── data/
│   └── raw\_data.json             # Original JSON input
│
├── processed/
│   └── cleaned\_text.txt          # Output from preprocessing
│
├── models/
│   ├── **init**.py
│   ├── preprocessing.py          # Module 1: JSON → cleaned text
│   ├── search.py                 # Module 2: Search with context
│   ├── response\_generator.py     # Module 3: Chatbot summarization
│   └── mongo\_connector.py        # NEW: MongoDB connection and operations
│
├── sessions/
│   └── memory.pkl                # Session context memory
│
├── utils/
│   └── helpers.py                # Helper functions
│
├── chatbot.py                    # Main driver script
│
└── README.md                     # Project overview

````

## Overview

This project is designed to implement an information retrieval system with three main modules:

1. **Preprocessing**: Converts raw JSON data into cleaned text.
2. **Search**: Context-aware search module.
3. **Response Generation**: Generates chatbot-like summarized responses.

Additional features include MongoDB integration to store and retrieve data efficiently and session management for context persistence.

## Setup

- Python 3.13+
- Create and activate a virtual environment:
  ```bash
  python3.13 -m venv venv
  source venv/bin/activate       # Linux/MacOS
  venv\Scripts\activate          # Windows
````

* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

Run the main chatbot driver:

```bash
python chatbot.py
```

## License

MIT License


```
