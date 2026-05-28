import os
import random
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

GENRES = ["Action", "Drama", "Comedy", "Thriller", "Horror", "Sci-Fi", "Romance", "Adventure", "Animation", "Crime"]
LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Malayalam", "Kannada"]
RATINGS = ["U", "U/A", "A"]
DURATIONS = ["1h 45m", "2h 10m", "2h 30m", "1h 55m", "2h 45m", "1h 35m"]

MOVIE_TITLES = [
    "The Dark Knight", "Inception", "Interstellar", "Avengers Endgame", "The Godfather",
    "Pulp Fiction", "Fight Club", "Forrest Gump", "The Matrix", "Goodfellas",
    "The Shawshank Redemption", "Schindler's List", "Parasite", "Joker", "Whiplash",
    "Dune", "Oppenheimer", "Barbie", "The Batman", "Spider-Man: No Way Home",
    "Top Gun: Maverick", "Everything Everywhere All at Once", "The Whale", "Elvis", "Black Panther",
    "Avatar: The Way of Water", "Doctor Strange", "Thor: Love and Thunder", "No Time to Die", "Tenet",
    "Ford v Ferrari", "Once Upon a Time in Hollywood", "1917", "Jojo Rabbit", "Knives Out",
    "Little Women", "Marriage Story", "The Irishman", "Joker", "Rocketman",
    "Bohemian Rhapsody", "A Star is Born", "Black Panther", "Get Out", "La La Land",
    "Moonlight", "The Shape of Water", "Three Billboards", "Dunkirk", "Lady Bird",
    "Call Me by Your Name", "The Post", "Phantom Thread", "Darkest Hour", "Blade Runner 2049",
    "Logan", "Coco", "Get Out", "Baby Driver", "The Big Sick",
    "Wonder Woman", "Dunkirk", "War for the Planet of the Apes", "Logan Lucky", "Thor: Ragnarok",
    "Spider-Man: Homecoming", "Guardians of the Galaxy 2", "Get Out", "Split", "John Wick 2",
    "La La Land", "Arrival", "Hacksaw Ridge", "Manchester by the Sea", "Moonlight",
    "Hell or High Water", "The Jungle Book", "Zootopia", "Deadpool", "Captain America: Civil War",
    "Rogue One", "Fantastic Beasts", "Doctor Strange", "Arrival", "Hidden Figures",
    "Lion", "Moonlight", "Hacksaw Ridge", "Manchester by the Sea", "Hell or High Water",
    "La La Land", "Fences", "Loving", "Jackie", "Nocturnal Animals",
    "Silence", "Live by Night", "Gold", "The Founder", "Patriots Day"
]

def generate_movies():
    movies = []
    for i in range(1, 101):
        title = MOVIE_TITLES[i - 1] if i <= len(MOVIE_TITLES) else f"Movie {i}"
        show_date = (datetime.now() + timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        show_time = f"{random.randint(10, 22)}:{random.choice(['00', '15', '30', '45'])}"
        
        movies.append({
            "id": i,
            "title": title,
            "genre": random.choice(GENRES),
            "language": random.choice(LANGUAGES),
            "rating": random.choice(RATINGS),
            "duration": random.choice(DURATIONS),
            "price": random.randint(150, 500),
            "show_date": show_date,
            "show_time": show_time,
            "description": f"{title} is a captivating {random.choice(GENRES).lower()} film that takes you on an unforgettable journey. Featuring stunning visuals and powerful performances, this movie promises to keep you on the edge of your seat from start to finish.",
            "poster_url": f"https://picsum.photos/seed/movie{i}/300/450",
            "director": f"Director {i}",
            "cast": f"Actor {i}a, Actor {i}b, Actor {i}c"
        })
    return movies

def generate_seats(movie_id):
    seats = []
    rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for row in rows:
        for num in range(1, 11):
            seat_id = f"{movie_id}_{row}{num}"
            seats.append({
                "id": seat_id,
                "movie_id": movie_id,
                "row": row,
                "number": num,
                "status": random.choice(["available", "available", "available", "booked"]),
                "price": random.choice([150, 200, 250, 300])
            })
    return seats

def seed_data():
    print("Generating 100 movies...")
    movies = generate_movies()
    
    # Insert movies in batches
    batch_size = 50
    for i in range(0, len(movies), batch_size):
        batch = movies[i:i + batch_size]
        supabase.table("movies").upsert(batch).execute()
        print(f"Inserted movies {i + 1} to {i + len(batch)}")
    
    print("Generating seats for all movies...")
    all_seats = []
    for movie in movies:
        movie_seats = generate_seats(movie["id"])
        all_seats.extend(movie_seats)
    
    # Insert seats in batches
    for i in range(0, len(all_seats), batch_size):
        batch = all_seats[i:i + batch_size]
        supabase.table("seats").upsert(batch).execute()
        print(f"Inserted seats batch {i // batch_size + 1}")
    
    print("Seeding complete! 100 movies and their seats have been inserted.")

if __name__ == "__main__":
    seed_data()
