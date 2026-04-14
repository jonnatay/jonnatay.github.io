create extension if not exists pgcrypto;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'manim-renders',
  'manim-renders',
  false,
  52428800,
  array['video/mp4']
)
on conflict (id) do update
set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

create table if not exists public.manim_jobs (
  id uuid primary key default gen_random_uuid(),
  access_token_hash text not null,
  status text not null check (status in ('queued', 'running', 'completed', 'failed', 'expired')),
  format text not null check (format in ('custom_harness')),
  source_code text not null,
  submitter_hash text not null,
  message text,
  error_message text,
  storage_path text,
  stdout_log text,
  stderr_log text,
  runtime_ms integer,
  output_bytes bigint,
  created_at timestamptz not null default timezone('utc', now()),
  started_at timestamptz,
  completed_at timestamptz,
  expires_at timestamptz not null
);

create index if not exists manim_jobs_status_created_at_idx
  on public.manim_jobs (status, created_at desc);

create index if not exists manim_jobs_expires_at_idx
  on public.manim_jobs (expires_at);

create index if not exists manim_jobs_submitter_hash_created_at_idx
  on public.manim_jobs (submitter_hash, created_at desc);

alter table public.manim_jobs enable row level security;

revoke all on public.manim_jobs from anon, authenticated;

do $$
begin
  if exists (select 1 from pg_roles where rolname = 'service_role') then
    grant all privileges on table public.manim_jobs to service_role;
  end if;
end
$$;

comment on table public.manim_jobs is
  'Async render jobs for the Manim Visualizer. Browser clients should never access this table directly; only the backend service role should.';
