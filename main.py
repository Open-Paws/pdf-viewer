import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, RedirectResponse
from io import BytesIO
import time

app = FastAPI()


@app.get("/pdf")
async def serve_pdf(url: str):
    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    # Set up retry parameters
    max_retries = 3
    retry_delay = 2

    # Attempt to fetch the content with retries
    for attempt in range(max_retries + 1):
        try:
            # Send GET request to the URL
            response = requests.get(url, headers=headers, allow_redirects=True)
            response.raise_for_status()

            # Check if the content type is PDF
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" in content_type:
                # If it's a PDF, return it as a streaming response
                pdf_content = BytesIO(response.content)
                return StreamingResponse(pdf_content, media_type="application/pdf")
            else:
                # If not a PDF, redirect to the original URL
                return RedirectResponse(url=url)
        except requests.RequestException as e:
            if attempt < max_retries:
                # If not the last attempt, wait before retrying
                time.sleep(retry_delay)
            else:
                # If all retries failed, raise an HTTP exception
                raise HTTPException(
                    status_code=500,
                    detail=f"Error fetching content after {max_retries + 1} attempts: {str(e)}",
                )


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
