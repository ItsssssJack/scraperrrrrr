#!/usr/bin/env python3
"""
Run database migration to create saved_enrichments table
"""
import requests
import json

SUPABASE_URL = "https://hqxxapqukrzawrvdlwmu.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhxeHhhcHF1a3J6YXdydmRsd211Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkyNzU5MTMsImV4cCI6MjA4NDg1MTkxM30.eGrFJ7HgXdhjfiyq7G8rEb0gitp0pF2pq9ZLzbnGB_4"

def run_migration():
    """
    Create the saved_enrichments table via Supabase REST API
    Note: This requires service_role key for DDL operations
    """
    print("🔧 Running migration to create saved_enrichments table...")
    print()
    print("⚠️  IMPORTANT: The anon key doesn't have permissions to run DDL operations.")
    print("   You need to run this SQL in the Supabase SQL Editor:")
    print()
    print("=" * 80)
    print("""
-- Create saved_enrichments table
CREATE TABLE IF NOT EXISTS saved_enrichments (
    id BIGSERIAL PRIMARY KEY,
    enrichment_id BIGINT NOT NULL REFERENCES article_enrichments(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(enrichment_id)
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_saved_enrichments_enrichment_id
    ON saved_enrichments(enrichment_id);

-- Enable Row Level Security
ALTER TABLE saved_enrichments ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations
DROP POLICY IF EXISTS "Allow all operations on saved_enrichments" ON saved_enrichments;
CREATE POLICY "Allow all operations on saved_enrichments" ON saved_enrichments
    FOR ALL
    USING (true)
    WITH CHECK (true);
    """)
    print("=" * 80)
    print()
    print("📋 Steps:")
    print("   1. Go to https://supabase.com/dashboard/project/hqxxapqukrzawrvdlwmu/sql")
    print("   2. Copy the SQL above")
    print("   3. Paste it into the SQL Editor")
    print("   4. Click 'Run'")
    print()
    print("   OR run: cat migrations/003_create_saved_enrichments.sql | supabase db execute")
    print()

if __name__ == "__main__":
    run_migration()
