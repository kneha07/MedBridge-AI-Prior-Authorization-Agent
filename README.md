# MedBridge — AI Prior Authorization Agent

> Prior auth handled in minutes. Not days.

MedBridge is an AI agent platform that automates healthcare prior authorization end-to-end — scanning payer policies, analyzing medical records, submitting via EDI 278, and automatically drafting appeals when denied. Built for the $19.7B administrative burden the U.S. healthcare system carries every year (AMA, 2023).

---

## The Problem

Every time a physician orders an MRI, surgery, or specialist referral, insurance companies require **prior authorization** before they'll pay. Today that process looks like this:

- Staff manually fills out 10+ page forms
- Faxes them to insurance portals (yes, still fax)
- Waits 3–5 business days for a response
- 1 in 5 requests gets **denied** — triggering hours more of manual appeal work
- Meanwhile the patient waits, untreated

**$19.7 billion** is lost annually to this administrative burden — not because the process is complex, but because humans are doing work that shouldn't require humans.

---

## The Solution

MedBridge is the **agent layer on top of your existing payer portals and EHR systems.** You fill out one form. The AI agent handles everything else autonomously.

### What the agent does

| Step | Tool | What happens |
|------|------|-------------|
| 1 | `scan_insurance_policy` | Pulls coverage criteria and clinical requirements from the payer database |
| 2 | `analyze_medical_records` | Evaluates patient history and establishes medical necessity |
| 3 | `fill_authorization_form` | Auto-populates all required fields — 96% completeness |
| 4 | `submit_authorization` | Transmits via EDI 278 to the payer portal |
| 5 | `track_authorization_status` | Checks initial decision and sets up real-time monitoring |
| 6 | `draft_appeal` *(if denied)* | Detects denial code, generates clinical appeal letter with supporting evidence |

### The key differentiator — Denial Auto-Appeal

When an authorization is denied, MedBridge doesn't stop. It:
1. Reads the denial reason and denial code (e.g. CO-50)
2. Pulls supporting clinical evidence from the patient record
3. Generates a formal appeal letter citing CMS guidelines
4. Attaches documentation (office notes, VAS scores, failed treatment records)
5. Queues it for physician co-signature and auto-submission

This is the workflow that currently takes staff 2–3 additional days. MedBridge does it in seconds.

---

## Demo

**Try Demo Scenarios:**
- **Standard Approval** — Full prior auth submitted and confirmed
- **Denial + Auto-Appeal** — Auth denied, appeal drafted automatically in the same run

**Demo patient:** Margaret R. Thompson — Lumbar MRI, Aetna, ICD-10 M72.5

Click **"✨ Try Demo"** on the form to auto-fill all fields.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│         (Vite · Inline styles · Real-time polling)   │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP + 1.5s polling
┌──────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                     │
│              POST /api/workflow/submit               │
│              GET  /api/workflow/{id}/status          │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Agent Runner                        │
│   Agentic loop: LLM → tool_use → observe → repeat   │
│   Provider: Groq (LLaMA 3.3 70B) · free tier        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Healthcare Vertical                     │
│   6 tools · HIPAA-aware · EDI 278 submission         │
│   Payers: Aetna · BCBS · UHC · Cigna · Humana       │
└─────────────────────────────────────────────────────┘
```

**Backend:** FastAPI · Python 3.11  
**AI:** Groq API (LLaMA 3.3-70b-versatile) — real agentic tool-use loop, not a chatbot  
**Frontend:** React · Vite  
**State:** In-memory (demo) — plugs into any database for production  
**Compliance:** HIPAA-aware design · CMS compliant 2026 · EDI 278 format  

---

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
ANTHROPIC_API_KEY=           # optional, for MedBridge Standard mode
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
GROQ_API_KEY=your_key uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/verticals` | List available workflow types |
| `POST` | `/api/workflow/submit` | Submit a new prior auth request |
| `GET` | `/api/workflow/{id}/status` | Poll for real-time status and step updates |
| `GET` | `/api/workflow/history/all` | List all past requests |
| `POST` | `/api/demo/reset` | Clear all in-memory state |
| `GET` | `/health` | Service health check |

### Submit Request Body

```json
{
  "vertical_id": "healthcare",
  "ai_provider": "groq",
  "form_data": {
    "patient_name": "Margaret R. Thompson",
    "patient_dob": "1968-04-15",
    "patient_id": "PT-2024-83741",
    "insurance_provider": "Aetna",
    "insurance_id": "AET-9284736501",
    "treatment_type": "MRI",
    "diagnosis_code": "M72.5",
    "treatment_description": "Lumbar spine MRI...",
    "requesting_physician": "Dr. Sarah Chen",
    "physician_npi": "1234567890",
    "demo_scenario": "Standard Approval"
  }
}
```

---

## Roadmap

MedBridge is architected as a vertical platform. Adding a new workflow requires one Python module — the agent loop, frontend, and polling are fully generic.

**Next healthcare workflows:**
- 🔄 Step Therapy Exceptions — override fail-first requirements with clinical evidence
- 📋 Specialist Referrals — automate HMO referral submissions and approvals
- 💊 Medication Appeals — dispute formulary denials for non-covered drugs

---

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) — async Python backend
- [Groq](https://groq.com/) — LLaMA 3.3 70B inference, free tier
- [React](https://react.dev/) + [Vite](https://vitejs.dev/) — frontend
- [Anthropic SDK](https://docs.anthropic.com/) — Claude integration (optional)
