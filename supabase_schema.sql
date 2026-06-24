-- ═══════════════════════════════════════════════════════════════
--  ZEM Hospital Management System — Supabase PostgreSQL Schema
--  Paste this entire script into the Supabase SQL Editor and run it.
--  Dashboard → SQL Editor → New Query → Paste → Run
-- ═══════════════════════════════════════════════════════════════

-- ── 1. Core Patient Records ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS pat_data (
    id          SERIAL PRIMARY KEY,
    cnic        VARCHAR(15)  NOT NULL,
    name        VARCHAR(100) NOT NULL,
    phone       VARCHAR(15),
    age         VARCHAR(10),
    city        VARCHAR(50),
    gender      VARCHAR(20),
    medicine    VARCHAR(100)
);

-- ── 2. Emergency Tokens ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS emergency_tokens (
    token_id    SERIAL PRIMARY KEY,
    cnic        VARCHAR(15),
    patient_id  INTEGER REFERENCES pat_data(id) ON DELETE CASCADE
);

-- ── 3. Admitted Patients ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS admited_patients (
    ward_id     SERIAL PRIMARY KEY,
    cnic        VARCHAR(15),
    patient_id  INTEGER REFERENCES pat_data(id) ON DELETE CASCADE,
    admitted_at TIMESTAMP DEFAULT NOW()
);

-- ── 4. Visitors ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS visitors (
    visitor_id      SERIAL PRIMARY KEY,
    visitor_name    VARCHAR(100),
    cnic            VARCHAR(15),
    contact_number  VARCHAR(15),
    patient_id      INTEGER,
    visited_at      TIMESTAMP DEFAULT NOW()
);

-- ── 5. Suggestions ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id   SERIAL PRIMARY KEY,
    suggestion_text VARCHAR(1000) NOT NULL,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ── Verification: list all created tables ────────────────────────
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type   = 'BASE TABLE'
ORDER BY table_name;
