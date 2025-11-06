# GRC Platform

A full-stack Governance, Risk, and Compliance platform designed to be developer-friendly, QA-friendly, infra-friendly, security-conscious, performant, low-cost, and scalable.

## Overview

- Frontend: `React + Vite + TailwindCSS + shadcn/ui + React Router`
- Backend: `FastAPI (Python) + Supabase (PostgreSQL + Auth + Storage)`
- Auth: `JWT` with RBAC (Admin, Risk Manager, Compliance Officer, Auditor, Viewer)
- Infra: Backend on Render, Frontend on Vercel
- Testing: `Jest` (frontend), `Pytest` (backend)
- Storage: Supabase for DB and file uploads
- CI/CD: GitHub Actions
- Docs: Swagger auto-generated from FastAPI

## Quick Start (No Docker)

1. Clone the repository and set environment variables

```
cd grc-platform
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Configure `.env` files

- `backend/.env`
  - `DEMO_MODE=true` (optional, enables local demo without Supabase)
  - `SUPABASE_URL=...`
  - `SUPABASE_ANON_KEY=...`
  - `SUPABASE_JWT_SECRET=...` (for JWT verification)
  - `CORS_ORIGINS=http://localhost:5173`

- `frontend/.env`
  - `VITE_API_URL=http://localhost:8000`

3. Run locally (no Docker)

Backend (FastAPI):

```
cd backend
python -m venv .venv && .venv\\Scripts\\activate
pip install -r requirements.txt
set DEMO_MODE=true
uvicorn main:app --reload --port 8000
```

Frontend (Vite):

```
cd ../frontend
npm install
npm run dev -- --host
```

Open `http://localhost:5173`. Login with demo role (e.g., admin).

## Project Structure

```
grc-platform
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── policies.py
│   │   ├── risks.py
│   │   ├── compliance.py
│   │   └── workflows.py
│   ├── schemas/
│   │   ├── common.py
│   │   ├── user.py
│   │   ├── policy.py
│   │   ├── risk.py
│   │   ├── compliance.py
│   │   └── workflow.py
│   ├── utils/
│   │   ├── auth.py
│   │   ├── db.py
│   │   ├── demo_store.py
│   │   ├── rbac.py
│   │   └── rate_limit.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_policies.py
│   │   └── test_risks.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Policies.jsx
│   │   │   ├── Risks.jsx
│   │   │   ├── Compliance.jsx
│   │   │   ├── WorkflowConfig.jsx
│   │   │   └── Login.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── ui/
│   │   │       ├── Button.jsx
│   │   │       ├── Input.jsx
│   │   │       └── Card.jsx
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── jest.config.js
│   ├── Dockerfile
│   ├── tailwind.config.js
│   └── postcss.config.js
├── .github/workflows/deploy.yml
├── docker-compose.yml
└── docs/
    └── wireframes.md
```

## Auth & Roles

- Backend validates JWT in protected routes.
- RBAC is enforced via role checks in dependencies.
- DEMO mode provides demo tokens: `demo-admin`, `demo-manager`, `demo-compliance`, `demo-auditor`, `demo-viewer`.

## API

- All endpoints are under `/api/v1`.
- CRUD endpoints for Policies, Risks, Compliance, Workflows.
- Pagination and search supported via query params.
- Rate limiting on sensitive endpoints using `slowapi`.

## Testing

- Backend: `pytest`
- Frontend: `jest` + `@testing-library/react`

Run locally (outside Docker):

```
cd backend && pip install -r requirements.txt && pytest
cd ../frontend && npm install && npm test
```

## Deployment (Render + Vercel + Supabase)

Follow these steps to deploy without Docker:

1) Create Supabase project
- Go to supabase.com and create a project.
- Copy `Project URL`, `anon public key`, and find `JWT secret` in Settings → API.
- In Storage, create a bucket named `policy_files`.
 - Create tables using SQL (SQL Editor):
   - Policies
     ```sql
     create table if not exists policies (
       id bigserial primary key,
       title text not null,
       description text,
       status text default 'Draft',
       file_url text,
       created_at timestamp default now()
     );
     ```
   - Risks
     ```sql
     create table if not exists risks (
       id bigserial primary key,
       title text not null,
       impact int default 1,
       likelihood int default 1,
       score int default 1,
       created_at timestamp default now()
     );
     ```
   - Frameworks
     ```sql
     create table if not exists frameworks (
       id bigserial primary key,
       name text not null,
       description text,
       controls jsonb default '[]'::jsonb,
       control_mappings jsonb default '{}'::jsonb,
       created_at timestamp default now()
     );
     ```

2) Configure backend on Render
- Create a new Web Service.
- Repository: connect your GitHub repo.
- Root directory: `grc-platform/backend`.
- Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`.
- Environment: `Python`. Build uses `requirements.txt` automatically.
- Environment Variables:
  - `DEMO_MODE=false`
  - `SUPABASE_URL=<your supabase project url>`
  - `SUPABASE_ANON_KEY=<your supabase anon key>`
  - `SUPABASE_JWT_SECRET=<your supabase jwt secret>`
  - `SUPABASE_STORAGE_BUCKET=policy_files`
  - `DEFAULT_ROLE=admin` (temporary until you set real roles)
  - `CORS_ORIGINS=https://<your-vercel-domain>`
- After deploy, take the Render URL, e.g., `https://grc-backend.onrender.com`.

3) Configure frontend on Vercel
- Import the repo and select `grc-platform/frontend` as the root.
- Framework preset: `Vite`.
- Build command: `npm run build`. Output directory: `dist`.
- Environment Variables:
  - `VITE_API_URL=https://grc-backend.onrender.com`
  - `VITE_DEMO_MODE=false`
  - `VITE_SUPABASE_URL=<your supabase project url>`
  - `VITE_SUPABASE_ANON_KEY=<your supabase anon key>`
- Deploy. Note the Vercel domain, e.g., `https://grc-frontend.vercel.app`.

4) Update backend CORS
- In Render backend service, set `CORS_ORIGINS` to your Vercel domain if not already.
- Restart the backend service.

5) Test login
- Visit your Vercel URL.
- On Login page, enter a Supabase user email and password.
- If you kept `DEFAULT_ROLE=admin`, you can use admin-only features immediately.
- Later, remove `DEFAULT_ROLE` and add a `role` claim to JWT or gate by email.

Add a role claim (advanced):
```sql
-- Example function to add a default role claim for all users
create or replace function jwt_custom_claim() returns jsonb language sql as $$
  select jsonb_build_object('role', 'viewer');
$$;

-- Then configure Supabase to include the custom claim in JWT (Auth → Policies or via config)
```

6) Optional: Add roles in Supabase
- Initially, backend defaults role using `DEFAULT_ROLE`.
- For proper RBAC, add a `role` claim to Supabase JWT via a Postgres function that sets `app.jwt_claims()`, or store roles per user and fetch on the backend.

Troubleshooting:
- 401 Unauthorized: ensure the frontend sends `Authorization: Bearer <supabase access_token>`; our frontend stores it automatically after login.
- 403 Forbidden: your user lacks the role required; set `DEFAULT_ROLE=admin` during setup or add role claim.
- CORS errors: update `CORS_ORIGINS` to include your Vercel domain.
- Upload errors: ensure Supabase Storage bucket `policy_files` exists and your anon key has access with appropriate policies.
   - In Supabase Storage Policies, allow authenticated users to insert and read:
     ```sql
     -- Storage policies (example, adjust to your bucket)
     -- Read for all
     create policy "Public read" on storage.objects for select to public using (bucket_id = 'policy_files');
     -- Upload by authenticated
     create policy "Authenticated upload" on storage.objects for insert to authenticated using (bucket_id = 'policy_files');
     ```

## Dummy Data

- DEMO mode uses in-memory stores with sample policies, risks, and frameworks.

## Wireframes

See `docs/wireframes.md` for UI sketches.

## Future Scalability Roadmap

- Extract modules to microservices (Policies, Risks, Compliance, Workflow)
- Use message queue for workflow transitions (e.g., RabbitMQ/CloudAMQP free tier)
- Add background workers for report generation
- Integrate role/permission management UI
- Add caching layer (Redis) for read-heavy endpoints
- Enhance AI assistant with embeddings stored in Supabase

## License

Open-source; customize and extend as needed.