# Movie Ticket Booking Application

A full-stack movie ticket booking application with React frontend and Python Flask backend.

## Tech Stack

- **Frontend**: React.js + Vite (Folder: `FN/`)
- **Backend**: Python Flask (Folder: `BN/`)
- **Database**: Supabase (PostgreSQL)

## Features

- Browse 100 movies with posters and details
- View detailed movie information (cast, director, showtime, etc.)
- Interactive seat selection in a theatre layout
- Dummy payment flow with card details
- Booking confirmation with transaction ID

## Project Structure

```
/
├── FN/                 # Frontend (React)
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── MovieDetails.jsx
│   │   │   ├── SeatBooking.jsx
│   │   │   └── Payment.jsx
│   │   ├── components/
│   │   │   └── MovieCard.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── BN/                 # Backend (Python Flask)
│   ├── app.py
│   ├── seed_data.py
│   ├── supabase_schema.sql
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

## Setup Instructions

### 1. Supabase Setup

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Once created, go to the SQL Editor
3. Copy and paste the contents of `BN/supabase_schema.sql` and run it
4. Go to Project Settings > API to get your `URL` and `anon public` key

### 2. Backend Setup

```bash
cd BN

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your Supabase credentials
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key

# Seed the database with 100 movies (optional - only if using Supabase)
python seed_data.py

# Run the backend
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd FN

# Install dependencies
npm install

# Run the frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

### 4. Deploying

- **Frontend (Vercel)**: Connect your GitHub repo to Vercel and deploy the `FN` folder
- **Backend (Railway)**: Push the `BN` folder to Railway with the Python environment
- **Database (Supabase)**: Already hosted on Supabase cloud

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/movies` | GET | Get all movies |
| `/api/movies/<id>` | GET | Get movie details |
| `/api/movies/<id>/seats` | GET | Get seats for a movie |
| `/api/book` | POST | Book seats |
| `/api/payment` | POST | Process payment |

## Note

If Supabase credentials are not provided, the backend will fallback to in-memory data for demo purposes.
