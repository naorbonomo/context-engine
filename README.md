# Context Engine

A powerful context-aware search and retrieval system built with FastAPI and React.


## 🚧 Project Status & Progress 🚧
- ✅ Basic FastAPI backend structure
- ✅ API - Hello World endpoint
- ✅ API - Ollama Chat API endpoint
- 🔄 API - Ollama Embedding API endpoint
- ⏳ React frontend setup
- ⏳ Frontend components development
- ⏳ Database integration pending
- ⏳ Authentication system pending
- ⏳ Search functionality pending


## Requirements

- [Python 3.10](https://www.python.org/downloads/release/python-3100/) 
-  [Node.js 22+](https://nodejs.org/en/download/current)
- [Git](https://git-scm.com/downloads)

## Quick Setup Guide

<details>
<summary><b>🔹 Backend Setup</b></summary>

1. Clone the repository:
```bash
git clone https://github.com/naorbonomo/context-engine
cd context-engine
```

2. Create a virtual environment:
```bash
py -3.10 -m venv .venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\.venv\Scripts\activate
```
- Linux/MacOS:
```bash
source .venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend root directory by copying the example:
```bash
cp .env.example .env
```


### Starting the Backend

Start the FastAPI backend with:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Available Endpoints
The API will be available at:
- API: http://localhost:8000/api/v1
- [Detailed API Documentation](docs/API.md)




</details>
<details>
<summary><b>🔹 Frontend Setup</b></summary>

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000
</details>
<details>
<summary><b>🔹 Project Structure</b></summary>

```
project-root/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── deps.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   └── endpoints/
│   │   │   └── deps.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── scripts/
│       └── start.sh
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── utils/
    └── scripts/
        └── start.sh
```
</details>

### Common Issues

1. If Python is not recognized as a command:
   - Verify Python installation: `python --version`
   - Make sure Python is added to your PATH
   - Windows users might need to use `py` instead of `python`

2. Virtual environment not activating:
   - Check that you're in the correct directory
   - On Windows, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

[MIT](LICENSE)

## Troubleshooting

If you encounter any issues:

1. Ensure Python 3.10+ is properly installed
2. Verify your virtual environment is activated (you should see `(.venv)` in your terminal)
3. Check that all requirements are installed: `pip list`
4. Make sure ports 8000 (backend) and 3000 (frontend) are available

For more help, please [create an issue](https://github.com/naorbonomo/context-engine/issues).

## Logging

The application implements comprehensive logging throughout its endpoints. Each API endpoint includes:
- INFO level logging for request processing
- DEBUG level logging for response details
- ERROR level logging for exception handling

Logs are created using Python's built-in logging module and can be configured through the application's logging configuration.