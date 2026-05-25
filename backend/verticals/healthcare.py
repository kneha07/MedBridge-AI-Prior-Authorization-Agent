import uuid
from datetime import datetime, timedelta

VERTICAL_ID = "healthcare"
VERTICAL_NAME = "Prior Authorization"
VERTICAL_DESCRIPTION = "Automate insurance prior authorization for any treatment — including denial detection and auto-appeal"
VERTICAL_ICON = "🏥"
VERTICAL_COLOR = "#22c55e"

SYSTEM_PROMPT = """You are MedBridge, an expert AI agent specializing in healthcare prior authorizations.

Complete these steps in order using the available tools:
1. scan_insurance_policy
2. analyze_medical_records
3. fill_authorization_form
4. submit_authorization
5. track_authorization_status
6. If track_authorization_status returns a denial, IMMEDIATELY call draft_appeal with the denial reason and patient data.

After all tools are done, provide a concise 3-4 sentence summary. If there was a denial, confirm the appeal was drafted and what happens next."""

TOOLS = [
    {
        "name": "scan_insurance_policy",
        "description": "Scan and retrieve the insurance policy requirements for a specific treatment type.",
        "input_schema": {
            "type": "object",
            "properties": {
                "insurance_provider": {"type": "string"},
                "treatment_type": {"type": "string"}
            },
            "required": ["insurance_provider", "treatment_type"]
        }
    },
    {
        "name": "analyze_medical_records",
        "description": "Analyze patient medical records to find supporting documentation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {"type": "string"},
                "diagnosis_code": {"type": "string"},
                "treatment_type": {"type": "string"}
            },
            "required": ["patient_id", "diagnosis_code", "treatment_type"]
        }
    },
    {
        "name": "fill_authorization_form",
        "description": "Fill out the prior authorization form with all required information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "auth_request": {"type": "object"},
                "policy_requirements": {"type": "object"},
                "medical_analysis": {"type": "object"}
            },
            "required": ["auth_request", "policy_requirements", "medical_analysis"]
        }
    },
    {
        "name": "submit_authorization",
        "description": "Submit the completed authorization form to the insurance company.",
        "input_schema": {
            "type": "object",
            "properties": {
                "form_id": {"type": "string"},
                "insurance_provider": {"type": "string"},
                "submission_method": {"type": "string"}
            },
            "required": ["form_id", "insurance_provider", "submission_method"]
        }
    },
    {
        "name": "track_authorization_status",
        "description": "Set up tracking and get initial status for the submitted authorization.",
        "input_schema": {
            "type": "object",
            "properties": {
                "submission_id": {"type": "string"},
                "insurance_provider": {"type": "string"}
            },
            "required": ["submission_id", "insurance_provider"]
        }
    },
    {
        "name": "draft_appeal",
        "description": "When an authorization is denied, automatically draft a formal appeal letter with clinical evidence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "denial_reason": {"type": "string"},
                "patient_name": {"type": "string"},
                "treatment_type": {"type": "string"},
                "insurance_provider": {"type": "string"}
            },
            "required": ["denial_reason", "patient_name", "treatment_type", "insurance_provider"]
        }
    }
]

STEP_DISPLAY = {
    "scan_insurance_policy":      ("Scanning Insurance Policy",     "Connecting to payer database — retrieving coverage criteria",        "Policy scanned — requirements and clinical criteria ready"),
    "analyze_medical_records":    ("Analyzing Medical Records",     "Evaluating patient history and establishing medical necessity",       "Medical records analyzed — necessity score: 87%"),
    "fill_authorization_form":    ("Completing Authorization Form", "Auto-filling all required fields based on policy and clinical data",  "Form completed — 96% completeness score"),
    "submit_authorization":       ("Submitting to Payer Portal",    "Transmitting to insurance portal via secure EDI connection",          "Authorization submitted — confirmation number assigned"),
    "track_authorization_status": ("Tracking Authorization",        "Checking initial decision and setting up real-time monitoring",       "Status received — tracking active"),
    "draft_appeal":               ("Drafting Appeal Letter",        "Detected denial — generating clinical appeal with supporting evidence","Appeal drafted — ready for physician co-signature"),
}

FORM_FIELDS = [
    {"key": "patient_name",         "label": "Patient Full Name",         "type": "text",     "required": True,  "placeholder": "e.g. Margaret R. Thompson"},
    {"key": "patient_dob",          "label": "Date of Birth",             "type": "date",     "required": True,  "placeholder": ""},
    {"key": "patient_id",           "label": "Patient ID / MRN",          "type": "text",     "required": True,  "placeholder": "e.g. PT-2024-83741"},
    {"key": "insurance_provider",   "label": "Insurance Provider",        "type": "select",   "required": True,  "options": ["Aetna","Blue Cross Blue Shield","United Healthcare","Cigna","Humana","Medicare","Medicaid"]},
    {"key": "insurance_id",         "label": "Member ID",                 "type": "text",     "required": True,  "placeholder": "e.g. AET-9284736501"},
    {"key": "treatment_type",       "label": "Treatment Type",            "type": "select",   "required": True,  "options": ["MRI","CT Scan","Physical Therapy","Surgery","Specialist Referral","Lab Tests","Medication"]},
    {"key": "diagnosis_code",       "label": "Diagnosis Code (ICD-10)",   "type": "text",     "required": True,  "placeholder": "e.g. M72.5"},
    {"key": "treatment_description","label": "Clinical Justification",    "type": "textarea", "required": True,  "placeholder": "Describe the clinical rationale..."},
    {"key": "requesting_physician", "label": "Physician Name",            "type": "text",     "required": True,  "placeholder": "e.g. Dr. Sarah Chen"},
    {"key": "physician_npi",        "label": "NPI Number",                "type": "text",     "required": True,  "placeholder": "10-digit NPI"},
    {"key": "demo_scenario",        "label": "Demo Scenario",             "type": "select",   "required": False, "options": ["Standard Approval", "Denial + Auto-Appeal"]},
]

DEMO_DATA = {
    "patient_name": "Margaret R. Thompson",
    "patient_dob": "1968-04-15",
    "patient_id": "PT-2024-83741",
    "insurance_provider": "Aetna",
    "insurance_id": "AET-9284736501",
    "treatment_type": "MRI",
    "diagnosis_code": "M72.5",
    "treatment_description": "Lumbar spine MRI without contrast to evaluate radiculopathy and rule out disc herniation following 8 weeks of conservative treatment failure.",
    "requesting_physician": "Dr. Sarah Chen",
    "physician_npi": "1234567890",
    "demo_scenario": "Standard Approval",
}

# Global store for form_data per request — set by agent_runner before tool calls
_current_form_data: dict = {}

def set_form_data(data: dict):
    global _current_form_data
    _current_form_data = data


async def execute_tool(tool_name: str, tool_input: dict) -> dict:
    import asyncio
    await asyncio.sleep(0.7)

    is_denial_scenario = _current_form_data.get("demo_scenario") == "Denial + Auto-Appeal"

    if tool_name == "scan_insurance_policy":
        return {
            "prior_auth_required": True,
            "coverage_requirements": ["Medical necessity documentation required", "Conservative treatment failed ≥6 weeks", "In-network facility required"],
            "required_documents": ["PA request form", "Letter of medical necessity", "Office visit notes", "Prior treatment records"],
            "typical_approval_time": "2-5 business days",
            "clinical_criteria": ["Persistent symptoms unresponsive to conservative care", "Neurological deficits present", "Structural injury suspected"],
            "payer_portal": "Aetna NaviNet Provider Portal",
            "submission_method": "EDI 278"
        }
    elif tool_name == "analyze_medical_records":
        return {
            "relevant_history": ["8-week history of lower back pain", "NSAIDs failed after 6 weeks", "Chiropractic care — minimal improvement", "VAS pain score: 7/10 at rest"],
            "supporting_diagnoses": ["M72.5 - Primary diagnosis", "M54.4 - Lumbago with sciatica"],
            "contraindications": ["No metallic implants", "No contrast reaction on file"],
            "medical_necessity_score": 0.87,
            "conservative_treatment_documented": True,
        }
    elif tool_name == "fill_authorization_form":
        form_id = f"FORM-{uuid.uuid4().hex[:8].upper()}"
        return {
            "form_id": form_id,
            "completeness_score": 0.96,
            "missing_fields": [],
            "auto_populated_fields": 14,
        }
    elif tool_name == "submit_authorization":
        provider = tool_input.get("insurance_provider", "INS")
        code = {"Aetna": "AET", "Blue Cross Blue Shield": "BCBS", "United Healthcare": "UHC", "Cigna": "CGN", "Humana": "HUM"}.get(provider, "INS")
        return {
            "submission_id": f"SUB-{uuid.uuid4().hex[:10].upper()}",
            "submitted_at": datetime.utcnow().isoformat(),
            "expected_response_by": (datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "confirmation_number": f"{code}-{datetime.utcnow().year}-PRI-{uuid.uuid4().int % 900000 + 100000}",
            "portal": "Aetna NaviNet",
            "transmission": "EDI 278 — Accepted",
        }
    elif tool_name == "track_authorization_status":
        if is_denial_scenario:
            return {
                "current_status": "DENIED",
                "denial_reason": "Not medically necessary — insufficient documentation of conservative treatment failure",
                "denial_code": "CO-50",
                "appeal_deadline": (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "appeal_rights": "You have 30 days to file a formal appeal with additional clinical evidence",
                "auto_appeal_available": True,
            }
        return {
            "current_status": "Under Review",
            "estimated_decision_date": (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "next_action": "Clinical review by insurance medical director within 48 hours",
            "real_time_tracking": "Active",
            "alert_configured": "Email + SMS on decision",
        }
    elif tool_name == "draft_appeal":
        patient = tool_input.get("patient_name", "Patient")
        treatment = tool_input.get("treatment_type", "treatment")
        provider = tool_input.get("insurance_provider", "Insurance Company")
        appeal_id = f"APPEAL-{uuid.uuid4().hex[:8].upper()}"
        return {
            "appeal_id": appeal_id,
            "status": "Draft Complete — Awaiting Physician Co-signature",
            "appeal_letter_preview": f"Re: Appeal of Denial — {patient} — {treatment}\n\nDear Medical Director,\n\nWe are formally appealing the denial (CO-50) for {treatment} for {patient}. The patient has documented 8+ weeks of failed conservative care including NSAIDs and chiropractic treatment, meeting all clinical criteria under CMS LCD L37606. Enclosed: office notes, VAS pain scores (7/10), and failed treatment records.",
            "supporting_evidence_attached": ["Office visit notes x4", "VAS pain score documentation", "Failed conservative treatment records", "Physician letter of medical necessity"],
            "next_step": f"Physician co-signature required — appeal auto-submitted to {provider} within 24h",
            "appeal_deadline": (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d"),
        }
    return {"error": f"Unknown tool: {tool_name}"}
