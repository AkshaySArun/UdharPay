# MASTER PROJECT PROMPT — UDHARPAY AI

## 1. YOUR ROLE

Act as a Senior Full-Stack Software Engineer, Agentic AI Architect, Fintech Developer, UI/UX Designer, Database Architect and Application Security Engineer.

Your task is to independently build a complete, functional, secure and professionally designed application from scratch called:

**UdharPay AI**

Tagline: Your kirana's money, collected without the awkwardness.

You must build the entire application, including:
- Frontend
- Backend
- SQLite database
- AI integrations
- Agentic AI system
- Cashfree payment integration
- Authentication and authorization
- API security
- Testing
- Documentation

Do not stop after creating the UI or folder structure. Implement the complete working application.

Do not use fake API responses when actual API credentials are configured.

Where external services are unavailable, provide a clearly labelled demo mode.

---

# 2. PROJECT VISION

UdharPay AI is an AI-powered digital Khata and automated payment collection platform designed for Indian Kirana stores and small businesses.

Millions of Indian shopkeepers maintain handwritten credit notebooks called Udhar Khata.

Customers purchase products on credit and promise to pay later. Shopkeepers often hesitate to ask customers for outstanding payments because of personal relationships.

UdharPay AI solves this problem using Agentic AI.

The merchant can:
1. Upload a photograph of a handwritten Khata notebook.
2. Extract customer information using Sarvam AI.
3. Add new credit entries using voice commands.
4. Maintain digital customer accounts.
5. Identify customers with outstanding balances.
6. Automatically prioritize collection tasks.
7. Communicate with customers in their preferred language.
8. Generate payment links using Cashfree.
9. Receive payment confirmation through Cashfree webhooks.
10. Automatically update the customer's outstanding balance.

The application must feel like a real fintech SaaS product, not a college project prototype.

---

# 3. TECHNOLOGY STACK

Use the following stack.

## Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide React icons
- Recharts
- React Hook Form
- Zod

## Backend
- Python 3
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- SQLite
- JWT authentication

## AI Integration
- Sarvam AI APIs
- Sarvam Speech-to-Text
- Sarvam LLM
- Sarvam Vision, if supported by the available API
- Sarvam Text-to-Speech

## Payment Integration
- Cashfree Payments
- Cashfree Payment Links or supported hosted payment flow
- Cashfree Webhooks

## Database
Use SQLite for the complete initial development and hackathon testing.

Database location:

backend/data/udharpay.db

Use SQLAlchemy ORM for all database operations.

Design database models to allow future PostgreSQL migration by changing the database configuration.

Do not require PostgreSQL installation.

---

# 4. CREATE THE PROJECT FROM SCRATCH

Start with an empty project directory.

Create this folder structure:

udharpay-ai/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── dashboard/
│   │   │   ├── khata/
│   │   │   ├── customers/
│   │   │   ├── collections/
│   │   │   ├── transactions/
│   │   │   ├── voice-assistant/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── dashboard/
│   │   │   ├── khata/
│   │   │   ├── customers/
│   │   │   ├── collections/
│   │   │   ├── payments/
│   │   │   └── ui/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── context/
│   │   ├── types/
│   │   └── lib/
│   ├── .env.local
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── dependencies.py
│   │   ├── api/
│   │   │   ├── router.py
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── customers.py
│   │   │       ├── khata.py
│   │   │       ├── sarvam.py
│   │   │       ├── collections.py
│   │   │       ├── payments.py
│   │   │       ├── webhooks.py
│   │   │       └── dashboard.py
│   │   ├── agents/
│   │   │   ├── orchestrator.py
│   │   │   ├── khata_agent.py
│   │   │   ├── collection_agent.py
│   │   │   ├── conversation_agent.py
│   │   │   ├── payment_agent.py
│   │   │   └── decision_engine.py
│   │   ├── services/
│   │   │   ├── sarvam_service.py
│   │   │   ├── cashfree_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── voice_service.py
│   │   │   └── notification_service.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   └── utils/
│   ├── data/
│   │   └── udharpay.db
│   ├── uploads/
│   ├── tests/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── docs/
├── .gitignore
├── README.md
└── docker-compose.yml

Create all necessary files.

Do not place the entire backend into one Python file.

Keep each service, agent, API route and database model modular.

---

# 5. ENVIRONMENT VARIABLES AND SECRET MANAGEMENT

All API credentials must be stored securely in the backend environment.

Create backend/.env:

DATABASE_URL=sqlite:///./data/udharpay.db

SARVAM_API_KEY=
SARVAM_BASE_URL=

CASHFREE_CLIENT_ID=
CASHFREE_CLIENT_SECRET=
CASHFREE_ENVIRONMENT=sandbox
CASHFREE_API_VERSION=

JWT_SECRET_KEY=

FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

UPLOAD_DIRECTORY=uploads
MAX_UPLOAD_SIZE_MB=10

Create backend/.env.example with empty placeholder values.

Create frontend/.env.local:

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

SECURITY RULES:

1. Never expose Sarvam API keys in frontend code.
2. Never expose Cashfree client secrets in frontend code.
3. Never put secret credentials in NEXT_PUBLIC variables.
4. Load environment variables using Pydantic Settings.
5. Never hardcode credentials.
6. Never print API credentials in terminal logs.
7. Add all .env files to .gitignore.
8. Validate required credentials at application startup or before the relevant integration is used.
9. Support sandbox and production configurations.
10. Keep secret values out of error messages and API responses.

The frontend must communicate with third-party APIs only through the secured backend.

---

# 6. DATABASE DESIGN — SQLITE

Create the following SQLAlchemy models.

## Merchants
- id
- shop_name
- owner_name
- phone
- email
- password_hash
- preferred_language
- created_at

## Customers
- id
- merchant_id
- name
- phone
- preferred_language
- outstanding_balance
- created_at

## KhataTransactions
- id
- merchant_id
- customer_id
- transaction_type
- amount
- description
- transaction_date
- due_date
- status
- created_at

Transaction types:
- CREDIT
- PAYMENT
- ADJUSTMENT

## Payments
- id
- merchant_id
- customer_id
- cashfree_order_id
- payment_link_id
- amount
- payment_status
- payment_method
- paid_at
- created_at

## CollectionTasks
- id
- merchant_id
- customer_id
- priority
- status
- scheduled_at
- completed_at

## Conversations
- id
- merchant_id
- customer_id
- language
- message
- sender
- intent
- created_at

## AuditLogs
- id
- merchant_id
- action
- entity_type
- entity_id
- created_at

Requirements:
- Proper foreign keys.
- Database indexes.
- Unique constraints where appropriate.
- SQLite foreign-key enforcement.
- Proper transaction handling.
- Merchant-level data isolation.
- Alembic migrations.
- Automatic database initialization.

Never allow one merchant to access another merchant's data.

Store money using Decimal/Numeric or integer paise, never floating-point arithmetic.

Outstanding balances must be derived or reconciled from verified ledger entries.

---

# 7. AUTHENTICATION AND SECURITY

Build a complete authentication system.

Features:
- Merchant registration.
- Merchant login.
- Logout.
- JWT access tokens.
- Password hashing using Argon2 or bcrypt.
- Protected API endpoints.
- Authenticated frontend routes.
- Merchant ownership validation.

Additional protections:
- Strict CORS configuration.
- Input validation.
- Upload validation.
- File size limits.
- Rate limiting.
- SQL injection protection.
- Secure error handling.
- Audit logging.
- Request timeouts.
- Webhook signature verification.
- Idempotent payment processing.

Use secure cookie-based authentication where practical, or implement a carefully protected token strategy.

Never trust merchant_id supplied by the frontend. Derive the authenticated merchant identity from the verified token.

---

# 8. SARVAM AI INTEGRATION

Create a dedicated SarvamService.

Read official Sarvam documentation and identify the currently supported models, endpoints, authentication headers and request schemas before implementation.

Do not invent API endpoints.

## A. Handwritten Khata Image Processing

Merchant uploads an image of a handwritten notebook.

Workflow:

Image Upload
    ↓
Backend File Validation
    ↓
Sarvam Vision / Supported Document Processing
    ↓
Text Extraction
    ↓
Sarvam LLM Structured Extraction
    ↓
Pydantic Validation
    ↓
Confidence and Ambiguity Check
    ↓
Merchant Approval
    ↓
SQLite Database

Extract:
- Customer name.
- Phone number, if present.
- Outstanding amount.
- Transaction date.
- Description.

Expected internal output:

{
  "customers": [
    {
      "name": "Ramesh",
      "phone": "9876500000",
      "amount": 847,
      "date": "2026-11-18",
      "confidence": 0.94
    }
  ]
}

This is an internal application schema, not an assumed Sarvam response schema.

If Sarvam Vision does not support the exact required image-processing operation, implement a documented supported extraction alternative and clearly report the limitation.

Never automatically commit uncertain OCR entries without merchant approval.

## B. Voice-Based Khata Entry

Allow the merchant to record audio using the browser microphone.

Example:

"Sunita ne teen din pehle 1200 rupaye ka udhar liya."

Workflow:

Audio
  ↓
Sarvam Speech-to-Text
  ↓
Sarvam LLM
  ↓
Structured JSON
  ↓
Validation
  ↓
Merchant Confirmation
  ↓
Database Entry

Extract:
- Customer name.
- Amount.
- Phone number, if provided.
- Transaction date.
- Description.

## C. Language Support

Prioritize:
- Kannada.
- Hindi.
- Tamil.
- Telugu.
- Marathi.
- English.

Use only languages supported by the selected Sarvam models.

## D. Text-to-Speech

Generate spoken confirmations.

Example:

"Ramesh avara 847 rupayigala balance add agide."

Use Sarvam TTS to generate audio where supported.

Provide audio playback on the frontend.

---

# 9. AGENTIC AI ARCHITECTURE

This is the most important part of the application.

Do not create a simple chatbot and call it Agentic AI.

Implement independent agents with defined responsibilities, tools, decisions, execution boundaries and logs.

## AGENT 1: KHATA INTELLIGENCE AGENT

Responsibilities:
- Process extracted Khata records.
- Identify existing customers.
- Detect duplicate records.
- Validate extracted amounts.
- Identify uncertain entries.
- Prepare transaction previews.
- Request merchant approval.

## AGENT 2: COLLECTION AGENT

Responsibilities:
- Identify customers with outstanding balances.
- Identify overdue transactions.
- Calculate collection priority.
- Rank customers.
- Create collection tasks.
- Prevent repeated contact attempts.
- Respect customer communication preferences and opt-outs.

Priority scoring can consider:
- Outstanding amount.
- Days overdue.
- Previous payment history.
- Merchant-defined priority.

Keep the scoring explainable.

## AGENT 3: CONVERSATION AGENT

Responsibilities:
- Understand customer responses.
- Recognize payment intent.
- Process regional-language conversations.
- Handle different customer situations.

Supported intents:

1. REQUEST_PAYMENT_LINK
2. PAY_PARTIALLY
3. PAY_LATER
4. ALREADY_PAID
5. DISPUTE_AMOUNT
6. REQUEST_HUMAN_HELP
7. OPT_OUT

Example conversation:

Agent:
"Namaste Ramesh ji. Sharma General Store mein aapka 847 rupaye ka balance baaki hai. Kya aap payment karna chahenge?"

Customer:
"Haan, payment link bhejo."

Agent:
"Bilkul. Main payment link taiyar kar raha hoon."

The agent must never pressure, threaten or harass customers.

## AGENT 4: PAYMENT AGENT

Responsibilities:
- Generate Cashfree payment links.
- Support full and partial payments.
- Associate payment links with customer accounts.
- Verify payments.
- Process payment status updates.
- Reconcile the ledger.

Never assume that opening or generating a payment link means money has been received.

## AGENT 5: ORCHESTRATOR

Create orchestrator.py.

Responsibilities:
- Coordinate the agents.
- Maintain workflow state.
- Decide which agent should execute next.
- Validate agent outputs.
- Record actions.
- Handle failures.
- Prevent unauthorized financial actions.

Example:

Merchant starts collection
       ↓
Collection Agent selects customer
       ↓
Conversation Agent generates localized conversation
       ↓
Customer confirms payment intent
       ↓
Payment Agent creates Cashfree link
       ↓
Payment webhook received
       ↓
Payment verified
       ↓
Khata updated
       ↓
Dashboard refreshed

Important:
- LLMs cannot directly write to financial tables.
- Every financial operation must go through validated backend services.
- Merchant approval is mandatory for uncertain records and sensitive actions.
- Collection execution must be controlled by explicit merchant authorization.

---

# 10. CASHFREE PAYMENT INTEGRATION

Create a separate CashfreeService.

Read the current official Cashfree documentation before implementation.

Implement the currently supported payment workflow.

Features:
1. Generate unique order IDs.
2. Create Cashfree payment orders or payment links.
3. Support configurable payment amounts.
4. Support partial payments.
5. Associate payment records with customer accounts.
6. Return hosted checkout URLs.
7. Verify payment status server-side.
8. Process payment webhooks.
9. Verify webhook signatures using the original raw request body and documented method.
10. Prevent duplicate webhook processing.
11. Update ledger balances only after successful verified payments.
12. Record payment history.

Use Cashfree sandbox mode.

Payment lifecycle:

Pending
   ↓
Payment Initiated
   ↓
Cashfree Checkout
   ↓
Webhook Received
   ↓
Signature Verified
   ↓
Payment Status Verified
   ↓
Database Transaction
   ↓
Ledger Updated
   ↓
Dashboard Refreshed

Never trust a payment success response coming from the browser alone.

Never allow payment amounts to exceed the customer's outstanding balance.

For partial payments, create a payment entry for the exact verified amount and recalculate the outstanding balance.

---

# 11. CUSTOMER COMMUNICATION SYSTEM

Build a modular communication layer.

Important distinction:

Sarvam provides speech and language intelligence, not necessarily telephone connectivity.

For the hackathon MVP:

- Build an interactive voice conversation simulator.
- Use Sarvam STT for customer audio input.
- Use Sarvam LLM for intent recognition.
- Use Sarvam TTS for agent audio output.
- Display the complete conversation transcript.
- Allow the customer to request a Cashfree payment link.
- Provide copy/share functionality.

Design a TelephonyProvider interface so an actual phone-call provider can be integrated later.

Do not claim that an actual phone call happened when using the simulator.

---

# 12. FRONTEND — PREMIUM FINTECH UI

Build a modern, premium, responsive fintech SaaS dashboard.

Design inspiration:
- Modern fintech applications.
- Professional SaaS dashboards.
- Clean banking interfaces.

Visual style:
- White and light gray surfaces.
- Deep navy typography.
- Emerald green for successful payments.
- Soft shadows.
- Rounded cards.
- Subtle animations.
- Professional spacing.
- Clear data visualizations.

Avoid excessive gradients, unnecessary decoration and crowded screens.

Use responsive layouts for mobile and desktop.

## A. AUTHENTICATION

Create:
- Login page.
- Registration page.
- Password visibility toggle.
- Form validation.
- Loading states.
- Error messages.
- Protected dashboard routes.

## B. MAIN DASHBOARD

Display:

- Total outstanding.
- Total collected this month.
- Total customers.
- Overdue accounts.
- Collection success rate.
- Recent transactions.
- Collection performance chart.
- Highest outstanding customers.
- AI-generated recommendations.

Use live backend data.

## C. DIGITAL KHATA

Features:
- Customer ledger.
- Search and filters.
- Add credit.
- Record payment.
- Upload handwritten Khata.
- Voice entry.
- OCR preview.
- Merchant approval.
- Customer transaction history.

## D. CUSTOMER MANAGEMENT

Display:
- Customer name.
- Phone.
- Preferred language.
- Outstanding balance.
- Last transaction.
- Due date.
- Payment history.

Allow merchant to add, edit and view customers.

## E. AI COLLECTIONS

Display:
- Priority collection queue.
- Customer name.
- Outstanding amount.
- Overdue days.
- Priority reason.
- Collection status.
- Start collection.
- Pause collection.
- Stop collection.

Show AI-generated collection recommendations.

## F. VOICE ASSISTANT

Build an interactive voice assistant interface.

Features:
- Microphone input.
- Recording state.
- Audio playback.
- Transcription.
- Conversation transcript.
- Language selection.
- Intent recognition.
- Payment link generation.

## G. TRANSACTIONS

Display:
- Transaction ID.
- Customer.
- Amount.
- Type.
- Payment status.
- Date.
- Payment method.

Provide filtering and search.

## H. ANALYTICS

Display:
- Daily collections.
- Monthly collections.
- Outstanding balances.
- Collection success rate.
- Customer payment patterns.

Use Recharts.

## I. SETTINGS

Provide:
- Shop profile.
- Merchant information.
- Preferred language.
- Payment integration status.
- AI integration status.
- Security settings.

---

# 13. BACKEND API ENDPOINTS

Implement clean REST APIs.

AUTH:
POST /api/auth/register
POST /api/auth/login
GET /api/auth/me

CUSTOMERS:
GET /api/customers
POST /api/customers
GET /api/customers/{id}
PUT /api/customers/{id}
DELETE /api/customers/{id}

KHATA:
GET /api/khata
POST /api/khata/transactions
POST /api/khata/upload
POST /api/khata/voice-entry
POST /api/khata/approve-import

SARVAM:
POST /api/sarvam/transcribe
POST /api/sarvam/extract
POST /api/sarvam/synthesize

COLLECTIONS:
GET /api/collections/tasks
POST /api/collections/start
POST /api/collections/pause
POST /api/collections/stop
POST /api/collections/customer-response

PAYMENTS:
POST /api/payments/create-link
GET /api/payments/{id}
GET /api/payments/history

WEBHOOKS:
POST /api/webhooks/cashfree

DASHBOARD:
GET /api/dashboard/summary
GET /api/dashboard/analytics

Use Pydantic schemas for every request and response.

Implement pagination where appropriate.

---

# 14. DEMO MODE

Create an initial demo merchant and realistic sample data.

Shop name: Sharma General Store.

Sample customers:

Ramesh — ₹847
Sunita — ₹1,240
Mahesh — ₹340
Priya — ₹2,500
Arun — ₹650

Include realistic transaction history and different payment statuses.

Demo mode must:
- Be clearly labelled.
- Never represent simulated payments as real payments.
- Allow testing the collection workflow.
- Allow simulated customer responses.
- Allow the UI to demonstrate the complete agent workflow.

Real Cashfree sandbox payments must be distinguishable from simulated transactions.

Do not silently switch from a failed real integration to fake success.

---

# 15. TESTING

Create backend tests using pytest.

Test:
- Merchant registration.
- Authentication.
- Customer creation.
- Customer isolation.
- Credit transactions.
- Balance calculation.
- Payment creation.
- Partial payments.
- Duplicate webhook processing.
- Invalid webhook signatures.
- Invalid API requests.
- Agent intent recognition.
- Collection prioritization.

Create frontend tests for critical interactions where practical.

Test all integrations independently.

---

# 16. IMPLEMENTATION PLAN

Follow this sequence.

PHASE 1 — PROJECT FOUNDATION
- Inspect environment.
- Initialize Next.js.
- Initialize FastAPI.
- Install dependencies.
- Create folder structure.
- Configure environment variables.
- Configure SQLite.
- Establish frontend-backend connection.

PHASE 2 — DATABASE AND AUTHENTICATION
- Build SQLAlchemy models.
- Configure Alembic.
- Implement registration and login.
- Implement merchant isolation.
- Implement customer management.
- Implement digital Khata.

PHASE 3 — SARVAM INTEGRATION
- Integrate Sarvam API.
- Implement image extraction.
- Implement voice transcription.
- Implement structured data extraction.
- Implement TTS.
- Test with actual API credentials.

PHASE 4 — AGENTIC AI
- Implement Khata Intelligence Agent.
- Implement Collection Agent.
- Implement Conversation Agent.
- Implement Payment Agent.
- Implement Orchestrator.
- Implement agent action logging.

PHASE 5 — CASHFREE INTEGRATION
- Configure sandbox credentials.
- Implement payment creation.
- Implement payment-link workflow.
- Implement webhook verification.
- Implement payment reconciliation.
- Test successful and failed payments.

PHASE 6 — FRONTEND
- Build login and registration.
- Build dashboard.
- Build customer pages.
- Build Khata pages.
- Build AI collections.
- Build voice assistant.
- Build transaction history.
- Build analytics.
- Connect every page to backend APIs.

PHASE 7 — TESTING AND FINALIZATION
- Run backend.
- Run frontend.
- Run all tests.
- Fix errors.
- Verify database operations.
- Verify API integrations.
- Verify payment workflows.
- Update README.
- Prepare demo instructions.

---

# 17. CODING AGENT BEHAVIOUR

Work autonomously.

Before writing code:
1. Inspect the available environment.
2. Check installed Python and Node.js versions.
3. Check available package managers.
4. Create the project structure.
5. Create a task checklist.

While developing:
- Write production-quality modular code.
- Follow consistent naming conventions.
- Avoid unnecessary dependencies.
- Do not duplicate code.
- Use reusable components.
- Use centralized API clients.
- Handle all loading and error states.
- Never leave important buttons non-functional.
- Do not use placeholder data when real backend data is available.
- Do not claim external API integration works until tested.
- Never invent undocumented third-party endpoints.

After every phase:
1. Run relevant tests.
2. Inspect errors.
3. Fix errors.
4. Update the task checklist.
5. Continue to the next phase.

Do not repeatedly ask for permission to continue ordinary development tasks.

If credentials are unavailable, build the integration and report which environment variables are required.

Do not expose actual secrets in generated documentation.

---

# 18. FINAL DELIVERABLES

At completion, provide:

1. Complete frontend application.
2. Complete backend application.
3. SQLite database initialization.
4. Database migration setup.
5. Sarvam AI integration.
6. Cashfree sandbox integration.
7. Agentic AI orchestration.
8. Secure authentication.
9. Working dashboard.
10. API documentation.
11. .env.example files.
12. .gitignore.
13. README.md.
14. Installation instructions.
15. Testing results.
16. Hackathon demo workflow.

Provide exact terminal commands to start both applications.

Frontend:

cd frontend
npm install
npm run dev

Backend:

cd backend
python -m venv venv

Windows:
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload

Backend API documentation:
http://localhost:8000/docs

Frontend:
http://localhost:3000

IMPORTANT FINAL OBJECTIVE:

Build a fully working UdharPay AI application from an empty folder.

Prioritize the complete customer journey:

Handwritten Khata
→ Sarvam AI Extraction
→ Merchant Approval
→ Digital Ledger
→ Agentic Collection
→ Regional Language Conversation
→ Cashfree Payment Link
→ Verified Payment Webhook
→ Automatic Balance Update
→ Live Dashboard.

This end-to-end workflow is the core hackathon demonstration.

Start building now.