# UdharPay AI

Digital khata and respectful collections for independent retailers. Backend integrations require your own Sarvam and Cashfree credentials; until supplied, their status is clearly shown as demo/unconfigured.

## Run locally

Backend (Python 3.11+):

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (Node 20+):

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:3000. The API docs are at http://localhost:8000/docs. Registration creates the first merchant. Set credentials in `backend/.env` to enable live Sarvam/Cashfree workflows; never place them in frontend variables. Demo mode supports sample data and simulated collection conversations, not simulated payment success.

## Integrations

Sarvam requests use the official `api-subscription-key` header and documented speech-to-text/chat/text-to-speech APIs. Handwriting extraction currently uses the Sarvam Vision/document-intelligence API when configured; see its API guide for the provider's current supported file contract. Cashfree uses server-side order creation and webhook HMAC validation against the original request body. Do not mark a payment paid from the browser return URL.

Database: SQLite at `backend/data/udharpay.db`; tables initialize on startup. Alembic configuration is included for future migrations. Set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL for future migration.

## First run and demo workflow

With `DEMO_MODE=true`, a clearly labelled Sharma General Store account and sample customer ledger are created on backend startup. Sign in with phone `9999999999` and password `Demo@UdharPay2026`. Keep demo mode off for production. Sessions use an HttpOnly cookie.

1. Sign in to the demo shop or register your own merchant account.
2. Add customers, then add credit entries in Digital Khata.
3. Upload a clear JPG/PNG/PDF khata page or add a voice note. Sarvam proposals are editable and require explicit approval before entering the ledger.
4. Use **Preview** in AI Collections for an in-app simulated reminder. **Call +91 test line** places a real Sarvam Voice Agents call to the configured test phone using that row's customer details; configure the `SARVAM_VOICE_*` identifiers in `backend/.env` first.
5. Create a payment order for a full or partial balance. In demo mode it remains pending. With Cashfree credentials, checkout opens in the selected environment; only a valid signed webhook updates the customer ledger.

Useful API groups include `/api/auth`, `/api/customers`, `/api/khata`, `/api/collections`, `/api/payments`, `/api/sarvam`, and `/api/dashboard`. Swagger documentation is served at `/docs`.

For schema changes, from `backend/` run `python -m alembic upgrade head`. Initial migration files are in `backend/migrations/versions/`.

### Windows Application Control and SQLAlchemy

If Windows blocks SQLAlchemy's `_collections_cy` extension with an Application Control error, reinstall SQLAlchemy from source without its optional C extensions in the active backend venv:

```powershell
$env:DISABLE_SQLALCHEMY_CEXT = "1"
python -m pip install --force-reinstall --no-binary=SQLAlchemy --no-cache-dir "SQLAlchemy>=2.0"
Remove-Item Env:DISABLE_SQLALCHEMY_CEXT
```
