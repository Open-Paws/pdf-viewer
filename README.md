# PDF Viewer Proxy

This project provides a simple API that takes a PDF URL and returns the PDF content as a viewer page, regardless of whether it's a direct download link or a viewer page.

## Features

- Fetches PDF content from given URLs
- Handles both direct PDF links and viewer pages
- Streams PDF content or redirects to the original URL if the PDF is not found
- Implements retry mechanism for improved reliability

## Prerequisites

- Python 3.7+
- uv (Python package installer and resolver) (or **pip is ok too**)

## Installation

1. Install uv:

   For macOS and Linux:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   For Windows (using PowerShell):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   For other installation methods or more details, visit the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-viewer-proxy.git
   cd pdf-viewer-proxy
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Application

To run the application, use the following command:

```
fastapi run main.py --reload
```

## Testing

```py
import requests
import logging
from urllib.parse import quote

def add_proxy(url):
    # Update this to match your actual proxy server address and port
    try:
        proxy_base_url = "http://localhost:8000/pdf"
        proxy_url = f"{proxy_base_url}?url={quote(url)}"
        return proxy_url
    except Exception as e:
        logging.error(
            f"Error adding proxy: {str(e)} | url: {url}"
        )
        return url
```

```py
url = "http://www.mdpi.com/2072-6643/6/6/2131/pdf"
proxy_url = add_proxy(url)
print(proxy_url)
```

### More Thorough Testing

Activate the **virtual environment** and run the test file:
```bash
python test_main.py # Note this is a simple test to see what kinds of responses the server will give for the provided links
```

If you want to check any of the proxy links provided in the test output manually, you need to run the main server first, using [Running the Application](#running-the-application).

## API Endpoints

### GET /pdf

Fetches and displays a PDF from a given URL.

Query Parameters:
- `url`: The URL of the PDF to fetch (required)

Example:
Curl

```bash
curl -X 'GET' \
  'http://localhost:8000/pdf?url=http%3A%2F%2Fwww.mdpi.com%2F2072-6643%2F6%2F6%2F2131%2Fpdf' \
  -H 'accept: application/json'
```

Request URL
http://localhost:8000/pdf?url=http%3A%2F%2Fwww.mdpi.com%2F2072-6643%2F6%2F6%2F2131%2Fpdf
