# Deploy on Render (Free Tier)

This guide deploys the FastAPI backend from this repo to Render.

## 1. Push this repo to GitHub

Render deploys directly from your GitHub repository.

## 2. Create a new Web Service

1. Log in to Render and connect your GitHub account.
2. Create a new Web Service.
3. Select this repo and the `main` branch.
4. Render should detect `render.yaml` automatically.

If needed, configure manually:
- Runtime: `Python`
- Build command: `pip install -e .`
- Start command: `uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/healthz`

## 3. Set environment variables

- `MDCHART_ALLOWED_ORIGINS`
  - Production: your blog origin, e.g. `https://blog.example.com`
  - Local dev + production: `https://blog.example.com,http://localhost:3000`

## 4. Verify deployment

Once deployed:
- `GET https://<your-service>.onrender.com/healthz`
- `GET https://<your-service>.onrender.com/docs`

## 5. Free-tier notes

Render free web services can spin down when idle, so the first request after idle may be slower.

## 6. Optional: custom domain

After deploy, map a custom domain/subdomain (e.g. `api.yourblog.com`) in Render settings and update DNS.
