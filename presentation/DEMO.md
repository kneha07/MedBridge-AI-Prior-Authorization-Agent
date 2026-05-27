# MedBridge — Demo & Presentation

## Demo Link

https://drive.google.com/file/d/1zcWHF-TiFEgXtzC-WMWpZdro0z7MHHWp/view?usp=drive_link

## Slides

[MedBridge_Presentation_Deck.pdf](MedBridge_Presentation_Deck.pdf)

## Video Walkthrough

> Add your video link here

---

## Video Demo Script (3–5 min)

---

### INTRO — 30 sec
*(show the homepage)*

"Hi, my name is Neha Kumari. I'm a student at Northeastern University, and today I'm presenting MedBridge — an AI agent that automates healthcare prior authorization end to end.

Prior authorization is the process where a doctor orders a treatment — an MRI, a surgery, a specialist referral — and the insurance company has to approve it before they'll pay. Today that process takes 3 to 5 business days, still runs on fax machines, and costs the U.S. healthcare system $19.7 billion a year in administrative burden alone.

MedBridge fixes that. Let me show you."

---

### DEMO SETUP — 20 sec
*(point to the form)*

"What you're looking at is a prior authorization request form. In the real world, a physician's office staff would fill this out manually — multiple pages, lots of codes, lots of waiting.

I'm going to click Try Demo to auto-fill a real patient scenario."

*(click Try Demo)*

"This is Margaret Thompson — she needs a lumbar spine MRI, she's insured through Aetna, and her diagnosis code is M72.5."

---

### SCENARIO 1 — STANDARD APPROVAL — 60–75 sec
*(select Standard Approval, hit Submit)*

"I'll run the Standard Approval scenario first. I hit Submit — and now watch what happens."

*(as steps appear, narrate each one)*

- **Step 1 — Policy scan:** "The agent is pulling Aetna's coverage criteria for lumbar MRIs — what clinical requirements they need, what documentation they want."
- **Step 2 — Records analysis:** "Now it's analyzing Margaret's patient history — establishing medical necessity based on her records."
- **Step 3 — Form fill:** "It's auto-populating the authorization form. 96% completeness — no missing fields, no back-and-forth."
- **Step 4 — Submission:** "Submitting via EDI 278 — the standard electronic format payers actually accept. No fax."
- **Step 5 — Status tracking:** "Checking the initial decision and setting up real-time monitoring."

*(result appears)*

"Authorization confirmed. That entire workflow — what normally takes hours across multiple days — done in seconds."

---

### SCENARIO 2 — DENIAL + AUTO-APPEAL — 90 sec
*(click Try Demo again, select Denial + Auto-Appeal, hit Submit)*

"Now let me show you the part that makes MedBridge different. This is the denial scenario."

*(as steps run)*

"Same workflow — but this time Aetna comes back with a denial. Denial code CO-50 — medical necessity not established.

In the real world, this is where staff spends the next 2 to 3 days drafting an appeal letter, pulling clinical notes, citing guidelines, getting physician sign-off.

Watch what MedBridge does."

*(appeal step runs)*

"The agent reads the denial code, pulls supporting clinical evidence from Margaret's record — her VAS pain scores, failed conservative treatments, office notes — and generates a formal CMS-compliant appeal letter. Queued for physician co-signature and ready to submit.

That 2-to-3-day workflow — done in seconds, automatically."

---

### CLOSE — 20 sec

"MedBridge is the agent layer on top of existing payer portals. No infrastructure replacement. Just AI doing the work that humans shouldn't have to do.

$19.7 billion problem. Six tools. Seconds — not days.

Thank you."

---

### Setup
1. Start the backend and frontend (see [README](../README.md#setup))
2. Open [http://localhost:5173](http://localhost:5173)

### Scenario 1 — Standard Approval
1. Click **"✨ Try Demo"** to auto-fill Margaret R. Thompson's info
2. Select **Standard Approval** scenario
3. Hit **Submit** and watch the agent work through all 6 steps in real time
4. Result: Authorization confirmed

### Scenario 2 — Denial + Auto-Appeal
1. Click **"✨ Try Demo"** again
2. Select **Denial + Auto-Appeal** scenario
3. Submit — agent hits a denial (CO-50), then immediately drafts a clinical appeal
4. Result: Appeal letter generated with supporting evidence, ready for physician sign-off

---

## Key Talking Points

- **Real agentic loop** — LLM chooses tools dynamically, not a hardcoded script
- **Denial auto-appeal** — 2–3 day staff workflow done in seconds
- **$19.7B problem** — AMA 2023, administrative burden on U.S. healthcare
- **Vertical platform** — adding a new workflow = one Python module
