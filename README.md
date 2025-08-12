## Astrology Compatibility Tool

Compute and explore astrological compatibility using birth details. Includes a Streamlit UI and CLI tools, detailed charts via `kerykeion`, CSV persistence, and optional S3 uploads.

### Features
- **Detailed charts**: Sun, Moon, Ascendant, personal/social/outer planets, houses
- **Advanced compatibility score**: multi-factor scoring with explanations
- **Streamlit UI**: point-and-click interface with saved CSV and optional S3 upload
- **CSV log**: results appended to `data/matches.csv`
- **S3 upload (optional)**: send CSV to your S3 bucket

## Requirements
- Python 3.9+
- pip

## Installation

### 1) Create and activate a virtual environment
- Windows (PowerShell):
```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
```
- macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root for optional integrations:
```env
# AWS S3 (optional)
AWS_ACCESS_KEY=...
AWS_SECRET_KEY=...
S3_BUCKET=...
REGION=...

# Google Geocoding API (optional, not required by Streamlit app)
GOOGLE_API_KEY=...

# Geonames username used by kerykeion (can also be set in Streamlit sidebar)
GEONAMES_USERNAME=your_geonames_username
```

Notes:
- If Geonames lookup fails, the app falls back to default coordinates (Varanasi, India).
- S3 upload requires valid AWS credentials and `S3_BUCKET`/`REGION`.

## Usage

### Streamlit UI (recommended)
```bash
streamlit run streamlit_app.py
```
- Enter names, birth dates, times, and places for both people.
- Set Geonames username in the sidebar if needed.
- Adjust the save threshold; enable S3 upload if desired.
- Results are saved to `data/matches.csv` when the score ≥ threshold.

### CLI – Basic
Runs a simple 3-factor score (Sun, Moon, Ascendant) and saves matches ≥ 50%.
```bash
python main.py
```

### CLI – Enhanced
Runs the detailed chart view and multi-factor score; saves and optionally uploads to S3.
```bash
python enhanced_compatibility.py
```

## Data & Storage
- **CSV file**: `data/matches.csv`
- **Geonames cache** (from `kerykeion`): `cache/kerykeion_geonames_cache.sqlite`
- **S3 path** (when enabled): keys like `astrology-matches/enhanced_matches_<timestamp>.csv`

## Project Structure
- `streamlit_app.py`: Streamlit UI
- `enhanced_compatibility.py`: detailed charts and advanced scoring (interactive CLI)
- `main.py`: basic compatibility scoring (interactive CLI)
- `csv_handler.py`: append results to CSV
- `s3_upload.py`: upload CSV to S3
- `config.py`: loads env vars
- `api_client.py`: Google Geocoding helper (optional)
- `data/matches.csv`: output CSV (created on first save)
- `cache/`: geonames cache used by `kerykeion`

## Deployment

### Streamlit Community Cloud (free)
1. Push this repo to GitHub.
2. In Streamlit Cloud, create a new app pointing to your repo.
3. Set the entrypoint to `streamlit_app.py`.
4. Add secrets in the app settings (copy from `.streamlit/secrets.toml.example`). At minimum set `GEONAMES_USERNAME`.
5. Deploy. The app will install from `requirements.txt` automatically.

### Render (free tier)
1. Push this repo to GitHub.
2. Create a new Web Service.
3. Environment: Python 3.x
4. Build Command:
```bash
pip install -r requirements.txt
```
5. Start Command:
```bash
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```
6. Add environment variables or mount a `secrets` file (values from `.streamlit/secrets.toml.example`). At minimum set `GEONAMES_USERNAME`.

### Docker (optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "${PORT}", "--server.address", "0.0.0.0"]
```
Build & run:
```bash
docker build -t astro-compat .
docker run -p 8501:8501 -e GEONAMES_USERNAME=yourname astro-compat
```

### Secrets
- Streamlit Cloud: use App Settings → Secrets. Paste TOML from `.streamlit/secrets.toml.example` and fill values.
- Render/other: set env vars directly or manage a secrets file and export at runtime.

## Troubleshooting
- **Module not found (streamlit/kerykeion)**: run `pip install -r requirements.txt` inside your virtual environment.
- **Geonames errors or slow lookups**: set a valid `GEONAMES_USERNAME` (sidebar or `.env`). The app will fall back to default coordinates if lookup fails.
- **S3 upload failed**: verify `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `S3_BUCKET`, and `REGION` in `.env`; ensure your IAM permissions allow `s3:PutObject`.
- **Timezone issues**: provide accurate birth time; `kerykeion` will resolve timezone using the city when available.

## Acknowledgements
- Built with `kerykeion` for astrology calculations
- UI powered by `streamlit`

