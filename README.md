# OpenCV Face Filter REST API

FastAPI service for face detection and simple image filters using OpenCV.

## Features

- Face detection API using Haar cascade and DNN-based detection helpers
- Face filter API for overlaying masks from the `filters/` directory
- Interactive OpenAPI docs at `/docs`
- Docker and Docker Compose support

## Requirements

- Python 3.11+
- Docker and Docker Compose, if running in containers

## Run Locally

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn manage:app --host 0.0.0.0 --port 5000 --reload
```

Open:

- API root: `http://localhost:5000/`
- Interactive docs: `http://localhost:5000/docs`

## Run With Docker

Build the image:

```bash
docker build -t face-filter-api .
```

Run the container:

```bash
docker run --rm -p 5000:5000 -v face-filter-uploads:/app/uploads face-filter-api
```

Open `http://localhost:5000/docs`.

## Run With Docker Compose

```bash
docker compose up --build
```

The app is available at `http://localhost:5000/docs`.

Stop the stack:

```bash
docker compose down
```

Remove the persisted upload volume as well:

```bash
docker compose down -v
```

## API Endpoints

### Health and Metadata

```http
GET /
```

### Face Detection

```http
GET  /api/v1/facedetection/
POST /api/v1/facedetection/
GET  /api/v2/facedetection/
POST /api/v2/facedetection/
```

Upload a JPEG file with the form field name `image`.

Example:

```bash
curl -X POST "http://localhost:5000/api/v1/facedetection/" \
  -F "image=@assets/sample.jpg;type=image/jpeg"
```

### Face Filters

```http
GET  /api/v1/facefilter/
POST /api/v1/facefilter/
```

Upload a JPEG file with `image` and choose a filter with `mask_num`.

Example:

```bash
curl -X POST "http://localhost:5000/api/v1/facefilter/" \
  -F "image=@assets/sample.jpg;type=image/jpeg" \
  -F "mask_num=1"
```

### Uploaded Images

```http
GET /uploads/{image_name}/
GET /uploads/{image_name}/delete/
```

## Tests

Run the local test suite:

```bash
pytest
```

Some tests reference the configured remote `base_url` in `settings.py`; run the local tests selectively if the remote service is unavailable:

```bash
pytest tests/test_case1.py tests/test_case2.py
```

## Project Structure

```text
.
+-- assets/              # OpenCV model files and sample images
+-- filters/             # Filter overlay images
+-- tests/               # API tests
+-- uploads/             # Runtime upload/output directory
+-- utils/               # Detection and filter helpers
+-- main.py              # FastAPI routes
+-- manage.py            # ASGI app entrypoint
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
```
