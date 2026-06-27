# ZEM_HMS

A lightweight Python Hospital Management System (ZEM Hospital). It provides a patient-facing kiosk for registration, emergency token generation and OPD selection, a visitor/suggestion interface, and a secured doctor/admin panel for searching, adding, updating, admitting and managing patient records.

## Key features

- Patient kiosk: registration form, emergency token generation, OPD token selection, and simple navigation.
- Doctor/admin panel: login-protected UI to view/search/add/update/delete patients, admit patients, and process the next patient.
- Visitor & suggestion forms: save visitor details and patient suggestions to the database.
- Persistent backend: Supabase/Postgres access via psycopg2 with schema creation and validation helpers.
- Utilities: data migration script (MySQL → Supabase) and compatibility shim for existing imports.
- Validation: CNIC, phone number, and age validation routines; defensive DB error handling and safe UI interactions.

## Tech stack

- **Language:** Python
- **GUI:** customtkinter + Pillow
- **Database:** Supabase (Postgres) accessed with psycopg2-binary
- **Config:** python-dotenv for environment variables

## Getting started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Supabase credentials (or set `SUPABASE_DB_URL`):

```
SUPABASE_DB_URL="your_supabase_connection_string"
# Optional admin credentials
ADMIN_USER=admin
ADMIN_PASS_HASH=<sha256-of-password>
```

3. Run the app (patient kiosk):

```bash
python ZEM_HMS.py
```

4. Run the doctor/admin panel:

```bash
python doctor_screen.py
```

5. If migrating from a legacy MySQL database, run the one-time migration:

```bash
python migrate_to_supabase.py
```

## Files of interest

- `ZEM_HMS.py` — patient-facing kiosk / main navigation
- `doctor_screen.py` — doctor/admin interface and core CRUD operations
- `admin_hms.py` — admin login screen
- `supabase_db.py` — database connection, schema creation, and CRUD functions
- `patient_db.py` — compatibility shim exporting supabase_db functions
- `migrate_to_supabase.py` — MySQL → Supabase migration tool
- `requirements.txt` — project dependencies

## License

MIT
