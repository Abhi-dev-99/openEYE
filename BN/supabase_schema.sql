connect-- Run this SQL in your Supabase SQL Editor to set up the database schema

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT,
    language TEXT,
    rating TEXT,
    duration TEXT,
    price INTEGER,
    show_date DATE,
    show_time TEXT,
    description TEXT,
    poster_url TEXT,
    director TEXT,
    cast TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    id TEXT PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
    row TEXT,
    number INTEGER,
    status TEXT DEFAULT 'available',
    price INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(id),
    seat_ids TEXT[],
    user_name TEXT,
    user_email TEXT,
    total_amount INTEGER,
    status TEXT DEFAULT 'pending_payment',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security (optional, configure as needed)
ALTER TABLE movies ENABLE ROW LEVEL SECURITY;
ALTER TABLE seats ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (for demo purposes)
CREATE POLICY "Allow public read" ON movies FOR SELECT USING (true);
CREATE POLICY "Allow public read" ON seats FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON bookings FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public update" ON bookings FOR UPDATE USING (true);
CREATE POLICY "Allow public read" ON bookings FOR SELECT USING (true);
