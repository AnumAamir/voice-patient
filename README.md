# Voice Patient Registration System

A voice-based patient registration system that uses a conversational AI agent to collect patient information over the phone, confirm the information with the caller, and save the registration to a persistent database through a FastAPI REST API.

## Architecture

```text
Caller
  ↓
Vapi Voice AI Agent
  ↓
save_patient_registration tool
  ↓
FastAPI REST API
  ↓
PostgreSQL Database
```

## Tech Stack

* **Vapi** — voice AI and phone interface
* **Python / FastAPI** — REST API
* **SQLAlchemy** — database ORM
* **Pydantic** — request validation
* **PostgreSQL** — persistent production database
* **SQLite** — local development fallback
* **Render** — API and database deployment

## Features

* Natural conversational patient registration over the phone
* Collects required patient demographics
* Handles corrections and incomplete/invalid information
* Confirms the collected information before saving
* Persists registrations to PostgreSQL
* REST API for creating, retrieving, updating, and soft-deleting patients
* Server-side validation
* UUID patient IDs
* Automatic `created_at` and `updated_at` timestamps
* Soft deletion using `deleted_at`
* Patient search/filtering by last name, date of birth, and phone number

## Patient Information

### Required

* First name
* Last name
* Date of birth
* Sex
* US phone number
* Address line 1
* City
* US state
* ZIP code

### Optional

* Email
* Address line 2
* Insurance provider
* Insurance member ID
* Preferred language
* Emergency contact name
* Emergency contact phone

## REST API

### GET `/patients`

Returns all active patients.

Optional query parameters:

* `last_name`
* `date_of_birth`
* `phone_number`

### GET `/patients/{patient_id}`

Returns a single active patient by UUID.

### POST `/patients`

Creates a new patient after validating the submitted information.

Returns `201 Created` on success.

### PUT `/patients/{patient_id}`

Partially updates an existing patient.

### DELETE `/patients/{patient_id}`

Soft-deletes a patient by setting `deleted_at`.

### Response Format

Successful responses use the following structure:

```json
{
  "data": {},
  "error": null
}
```

Errors use the same envelope structure with an error message.

## Voice Registration Flow

1. Caller dials the Vapi phone number.
2. The AI agent naturally asks for the patient's registration information.
3. The agent handles corrections and missing/invalid information conversationally.
4. The agent reads the collected information back to the caller for confirmation.
5. After confirmation, the `save_patient_registration` tool is called.
6. Vapi sends the patient data to the FastAPI API.
7. FastAPI validates and saves the patient to PostgreSQL.
8. The agent informs the caller that the registration was successfully completed.

## Environment Variables

The application uses environment variables for database configuration.

```text
DATABASE_URL
```

The production PostgreSQL connection string is configured through Render environment variables and is not hardcoded in the source code.

For local development, the application falls back to:

```text
sqlite:///./patients.db
```

## Running Locally

Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Deployment

The FastAPI application is deployed on Render.

The production application uses PostgreSQL through the `DATABASE_URL` environment variable.

The Vapi voice agent communicates with the deployed FastAPI API to save completed patient registrations.

## Security Considerations

* Database credentials are stored in environment variables rather than source code.
* Local virtual-environment files are excluded from version control.
* The local SQLite database is excluded from version control.
* API input is validated server-side before database operations.

### Known Limitation

The current assessment implementation does not include authentication or authorization for the REST API. This was intentionally kept simple for the take-home assessment and would need to be addressed before using the system in a production healthcare environment.

## Project Structure

```text
voice-patient/
│
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Status

The complete voice-to-database registration flow has been tested successfully:

**Phone call → Vapi → FastAPI → PostgreSQL → Patient record**

The REST API endpoints and voice registration flow are operational.

## Limitations and Improvements
- The REST API currently does not implement authentication or authorization. For a production deployment, appropriate access controls, role-based permissions, and secure authentication would be required to protect patient data.
- Patient data can currently be retrieved, created, updated, and soft-deleted through the REST API. A dedicated web-based interface could provide a more user-friendly way for authorized staff to manage patient records.
- Adding unit and integration tests would help verify individual components, catch regressions early, and make future changes safer and more reliable.
- A production version could include structured logging, audit trails for patient-data changes, monitoring, and alerting to make system behavior easier to track and troubleshoot.
- Additional validation and duplicate-patient detection could be introduced to reduce data-entry errors and prevent accidental creation of duplicate records.
- A real healthcare deployment would require additional security and privacy controls, including encryption, stricter access controls, secure secret management, data-retention policies, and compliance with applicable healthcare and privacy regulations.
- The application could be further improved with database indexing, connection-pool tuning, rate limiting, centralized error handling, and production-oriented backup and recovery strategies.
