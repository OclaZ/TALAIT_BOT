/*
  # Create Ticket-Based Submissions System

  1. New Tables
    - `submissions`
      - `id` (uuid, primary key)
      - `challenge_id` (integer, references challenge)
      - `user_id` (text, Discord user ID)
      - `username` (text, Discord username)
      - `code` (text, submitted code)
      - `language` (text, programming language)
      - `notes` (text, optional submission notes)
      - `thread_id` (text, Discord thread ID for private communication)
      - `status` (text, submission status: pending, reviewed, winner)
      - `created_at` (timestamptz, submission timestamp)
      - `updated_at` (timestamptz, last update timestamp)
  
  2. Security
    - Enable RLS on `submissions` table
    - Trainers can view all submissions
    - Users can only view their own submissions
    
  3. Notes
    - Submissions are private by default
    - Each submission creates a private thread/ticket
    - Trainers can review submissions without public visibility
*/

CREATE TABLE IF NOT EXISTS submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  challenge_id integer NOT NULL,
  user_id text NOT NULL,
  username text NOT NULL,
  code text NOT NULL,
  language text DEFAULT 'python',
  notes text,
  thread_id text,
  status text DEFAULT 'pending',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;

-- Note: Since this is a Discord bot without Supabase auth, 
-- we'll manage permissions in the application layer
-- Create a permissive policy for the service role to manage all data
CREATE POLICY "Service role has full access"
  ON submissions
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_submissions_challenge_id ON submissions(challenge_id);
CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);