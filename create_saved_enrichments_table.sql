-- Create saved_enrichments table
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/hqxxapqukrzawrvdlwmu/sql

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
