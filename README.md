# OpenAI Server Utils

A Python utility to wait for OpenAI-compatible API servers to become ready before proceeding with tasks.

## Overview

When working with local or self-hosted OpenAI-compatible servers, it's often necessary to wait until the server is fully initialized before sending requests. This utility provides a simple command-line tool and Python function to wait for a server to become ready, with configurable timeout and retry options.

## Installation

### From source

```bash
pip install git+https://github.com/yourusername/openai-server-utils.git
```

### Development installation

```bash
git clone https://github.com/yourusername/openai-server-utils.git
cd openai-server-utils
pip install -e .
```

## Usage

### Command-line usage

```bash
# Basic usage - wait for server to be ready
wait_openai http://localhost:9090/v1

# With custom timeout (in seconds)
wait_openai http://localhost:9090/v1 --timeout 600

# With custom check interval (in seconds)
wait_openai http://localhost:9090/v1 --check-interval 2.0

# Silent mode (no status messages)
wait_openai http://localhost:9090/v1 --quiet
```

### Python API usage

```python
from openai_server_utils import wait_for_openai_server

# Wait for server to be ready with default parameters
is_ready = wait_for_openai_server("http://localhost:9090/v1")

# With custom parameters
is_ready = wait_for_openai_server(
    url="http://localhost:9090/v1",
    timeout=600,           # Maximum wait time in seconds
    check_interval=2.0,    # Initial interval between checks
    verbose=True           # Print status messages
)

if is_ready:
    # Server is ready, proceed with requests
    print("Server is ready!")
else:
    print("Server failed to become ready within the timeout period")
```

### Example workflow

This utility is designed to work in automation scripts and workflows:

```bash
# Start OpenAI-compatible server in the background
run_openai_server_in_background localhost:9090

# Wait for the server to become ready
wait_openai http://localhost:9090/v1

# Start using the server for predictions
start_prediction
```

## Features

- Checks both health endpoints (`/health/ready`) and standard OpenAI endpoints (`/models`) for compatibility with different server implementations
- Uses exponential backoff with jitter to avoid overwhelming the server during initialization
- Configurable timeout and check intervals
- Can be used both as a command-line tool and as a Python library
- Returns appropriate exit codes for use in scripts (0 for success, 1 for failure)

## How It Works

The utility attempts to connect to the server using two different endpoints:

1. First, it tries the `/health/ready` endpoint (common in NVIDIA NIM and other implementations)
2. If that fails, it tries the `/models` endpoint (standard OpenAI API)

It continues trying until either:
- One of the endpoints returns a successful status code (200)
- The specified timeout period is reached

## Dependencies

- Python 3.6+
- requests library

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

---
Perplexity로부터의 답변: pplx.ai/share