-- ============================================================
-- migration.sql - AgriLens AI Disease Repository
-- Run in the Supabase SQL editor (or via CLI migration).
-- ============================================================

-- 1) Core table (create if it doesn't already exist).
--    If you already created `diagnoses` manually, run only the
--    ALTER TABLE block in section (2) to add the new columns.
create table if not exists public.diagnoses (
    id                   uuid primary key default gen_random_uuid(),
    image_url            text,
    prediction            text not null,
    confidence            numeric not null,
    language              text not null,
    diagnosis_status       text,
    model_version          text,
    verification_status   text not null default 'pending',
    created_at            timestamptz not null default now(),

    -- Future-proofing metadata (all nullable)
    latitude              double precision,
    longitude             double precision,
    state                  text,
    lga                    text,
    farmer_id              text,
    device_info            text,
    consent_given          boolean
);

-- 2) If the table already existed before this migration, add any
--    missing columns safely (no-op if they already exist).
alter table public.diagnoses add column if not exists image_url text;
alter table public.diagnoses add column if not exists prediction text;
alter table public.diagnoses add column if not exists confidence numeric;
alter table public.diagnoses add column if not exists language text;
alter table public.diagnoses add column if not exists diagnosis_status text;
alter table public.diagnoses add column if not exists model_version text;
alter table public.diagnoses add column if not exists verification_status text default 'pending';
alter table public.diagnoses add column if not exists created_at timestamptz default now();
alter table public.diagnoses add column if not exists latitude double precision;
alter table public.diagnoses add column if not exists longitude double precision;
alter table public.diagnoses add column if not exists state text;
alter table public.diagnoses add column if not exists lga text;
alter table public.diagnoses add column if not exists farmer_id text;
alter table public.diagnoses add column if not exists device_info text;
alter table public.diagnoses add column if not exists consent_given boolean;

-- 3) Constrain verification_status to a known set of values.
--    This is the HUMAN REVIEW status: pending / verified / rejected.
alter table public.diagnoses drop constraint if exists diagnoses_verification_status_check;
alter table public.diagnoses
    add constraint diagnoses_verification_status_check
    check (verification_status in ('pending', 'verified', 'rejected'));

-- 3b) Constrain diagnosis_status to a known set of values.
--     This is the MODEL'S OWN confidence assessment computed by the
--     /diagnose endpoint: confirmed / likely / uncertain. It is
--     distinct from verification_status above (human review), and
--     both columns exist independently.
alter table public.diagnoses drop constraint if exists diagnoses_diagnosis_status_check;
alter table public.diagnoses
    add constraint diagnoses_diagnosis_status_check
    check (diagnosis_status is null or diagnosis_status in ('confirmed', 'likely', 'uncertain'));

-- 4) Indexes to support upcoming features (heatmaps, outbreak
--    detection, verification queue, model monitoring) without
--    needing another migration later.
create index if not exists idx_diagnoses_created_at on public.diagnoses (created_at desc);
create index if not exists idx_diagnoses_verification_status on public.diagnoses (verification_status);
create index if not exists idx_diagnoses_diagnosis_status on public.diagnoses (diagnosis_status);
create index if not exists idx_diagnoses_model_version on public.diagnoses (model_version);
create index if not exists idx_diagnoses_prediction on public.diagnoses (prediction);
create index if not exists idx_diagnoses_state_lga on public.diagnoses (state, lga);

-- 5) Row Level Security.
--    The backend writes using the SERVICE ROLE key, which bypasses
--    RLS entirely — so enabling RLS here does not block the
--    gateway. It DOES block any client using the anon/public key
--    from reading or writing this table directly, which is what
--    we want for a farmer-data repository. Adjust/add policies
--    later when you build admin or verification-officer access.
alter table public.diagnoses enable row level security;

-- No policies are added for the anon role on purpose: this table
-- is intended to be accessed only via the backend service role
-- until an authenticated admin/verification role is introduced.

-- 6) Storage bucket.
--    Create the 'leaf-images' bucket as PRIVATE via the Supabase
--    Dashboard (Storage -> New bucket -> uncheck "Public bucket"),
--    or via the CLI/SQL below.
insert into storage.buckets (id, name, public)
values ('leaf-images', 'leaf-images', false)
on conflict (id) do nothing;

-- No storage.objects policies are added for the anon role, since
-- all uploads/reads happen through the backend using the service
-- role key, which also bypasses storage RLS.
