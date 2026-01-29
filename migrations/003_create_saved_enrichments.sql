-- Migration: Create saved_enrichments table
-- This table stores which enrichments users have saved

CREATE TABLE IF NOT EXISTS saved_enrichments (
    id BIGSERIAL PRIMARY KEY,
    enrichment_id BIGINT NOT NULL REFERENCES article_enrichments(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(enrichment_id)
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_saved_enrichments_enrichment_id ON saved_enrichments(enrichment_id);

-- Enable Row Level Security
ALTER TABLE saved_enrichments ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust based on your auth needs)
CREATE POLICY "Allow all operations on saved_enrichments" ON saved_enrichments
    FOR ALL
    USING (true)
    WITH CHECK (true);
