-- Article Enrichment Schema
-- Adds support for sub-articles/news items within main articles
-- Run this AFTER database-schema.sql

-- Article enrichments table (sub-articles within a main article)
CREATE TABLE IF NOT EXISTS article_enrichments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  summary TEXT,
  image_url TEXT,
  content TEXT,
  position INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(article_id, position)
);

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_enrichments_article_id ON article_enrichments(article_id);
CREATE INDEX IF NOT EXISTS idx_enrichments_position ON article_enrichments(article_id, position);

-- Enable Row Level Security (RLS)
ALTER TABLE article_enrichments ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access
CREATE POLICY "Allow public read access to enrichments"
  ON article_enrichments FOR SELECT
  USING (true);

-- Create policy for service role to insert enrichments
CREATE POLICY "Allow service role to insert enrichments"
  ON article_enrichments FOR INSERT
  WITH CHECK (true);

-- Create policy for service role to update enrichments
CREATE POLICY "Allow service role to update enrichments"
  ON article_enrichments FOR UPDATE
  USING (true);

-- Comments for documentation
COMMENT ON TABLE article_enrichments IS 'Stores individual news items extracted from within main articles (e.g., The Rundown contains multiple news stories per article)';
COMMENT ON COLUMN article_enrichments.position IS 'Order of the enrichment within the parent article (0-indexed)';
COMMENT ON COLUMN article_enrichments.content IS 'Full text content of the news item';
