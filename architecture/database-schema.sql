-- AI News Aggregator Database Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Articles table
CREATE TABLE IF NOT EXISTS articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL,
  published_date TIMESTAMPTZ NOT NULL,
  summary TEXT,
  author TEXT,
  image_url TEXT,
  tags TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Saved articles table
CREATE TABLE IF NOT EXISTS saved_articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
  saved_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(article_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles(published_date DESC);
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url);
CREATE INDEX IF NOT EXISTS idx_saved_articles_saved_at ON saved_articles(saved_at DESC);
CREATE INDEX IF NOT EXISTS idx_saved_articles_article_id ON saved_articles(article_id);

-- Enable Row Level Security (RLS)
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_articles ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access
CREATE POLICY "Allow public read access to articles"
  ON articles FOR SELECT
  USING (true);

CREATE POLICY "Allow public read access to saved articles"
  ON saved_articles FOR SELECT
  USING (true);

-- Create policies for public insert/delete on saved_articles
CREATE POLICY "Allow public insert to saved articles"
  ON saved_articles FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public delete from saved articles"
  ON saved_articles FOR DELETE
  USING (true);

-- Create policy for service role to insert articles
CREATE POLICY "Allow service role to insert articles"
  ON articles FOR INSERT
  WITH CHECK (true);

-- Create policy for service role to update articles
CREATE POLICY "Allow service role to update articles"
  ON articles FOR UPDATE
  USING (true);

-- Comments for documentation
COMMENT ON TABLE articles IS 'Stores all scraped AI news articles from various sources';
COMMENT ON TABLE saved_articles IS 'Stores user-saved articles with references to the articles table';
COMMENT ON COLUMN articles.source IS 'Source of the article (bensbites, rundown, reddit)';
COMMENT ON COLUMN articles.published_date IS 'Original publication date from the source';
COMMENT ON COLUMN articles.tags IS 'Array of tags/categories for the article';
