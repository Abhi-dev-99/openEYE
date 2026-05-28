from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("Warning: Supabase credentials not found. Using in-memory data.")

# In-memory fallback data
movies_data = []
bookings_data = []
seats_data = {}

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
        genre = random.choice(GENRES)
        language = random.choice(LANGUAGES)
        rating = random.choice(RATINGS)
        duration = random.choice(DURATIONS)
        price = random.randint(150, 500)
        show_date = (datetime.now() + timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        show_time = f"{random.randint(10, 22)}:{random.choice(['00', '15', '30', '45'])}"
        
        movies.append({
            "id": i,
            "title": title,
            "genre": genre,
            "language": language,
            "rating": rating,
            "duration": duration,
            "price": price,
            "show_date": show_date,
            "show_time": show_time,
            "description": f"{title} is a captivating {genre.lower()} film that takes you on an unforgettable journey. Featuring stunning visuals and powerful performances, this {language} movie promises to keep you on the edge of your seat from start to finish.",
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

def init_data():
    global movies_data, seats_data
    movies_data = generate_movies()
    for movie in movies_data:
        seats_data[movie["id"]] = generate_seats(movie["id"])

init_data()

@app.route("/api/movies", methods=["GET"])
def get_movies():
    if supabase:
        try:
            response = supabase.table("movies").select("*").execute()
            return jsonify(response.data)
        except Exception as e:
            print(f"Supabase error: {e}")
    return jsonify(movies_data)

@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    if supabase:
        try:
            response = supabase.table("movies").select("*").eq("id", movie_id).execute()
            if response.data:
                return jsonify(response.data[0])
        except Exception as e:
            print(f"Supabase error: {e}")
    
    movie = next((m for m in movies_data if m["id"] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route("/api/movies/<int:movie_id>/seats", methods=["GET"])
def get_seats(movie_id):
    if supabase:
        try:
            response = supabase.table("seats").select("*").eq("movie_id", movie_id).execute()
            return jsonify(response.data)
        except Exception as e:
            print(f"Supabase error: {e}")
    
    if movie_id in seats_data:
        return jsonify(seats_data[movie_id])
    return jsonify({"error": "Movie not found"}), 404

@app.route("/api/book", methods=["POST"])
def book_seats():
    data = request.json
    movie_id = data.get("movie_id")
    seat_ids = data.get("seat_ids", [])
    user_name = data.get("user_name", "Guest")
    user_email = data.get("user_email", "guest@example.com")
    
    if not movie_id or not seat_ids:
        return jsonify({"error": "Movie ID and seat IDs are required"}), 400
    
    if supabase:
        try:
            # Check if seats are available
            response = supabase.table("seats").select("*").in_("id", seat_ids).eq("movie_id", movie_id).execute()
            seats = response.data
            
            if len(seats) != len(seat_ids):
                return jsonify({"error": "Some seats not found"}), 400
            
            for seat in seats:
                if seat["status"] != "available":
                    return jsonify({"error": f"Seat {seat['row']}{seat['number']} is already booked"}), 400
            
            # Update seats status
            supabase.table("seats").update({"status": "booked"}).in_("id", seat_ids).execute()
            
            # Create booking
            total_amount = sum(seat["price"] for seat in seats)
            booking = {
                "movie_id": movie_id,
                "seat_ids": seat_ids,
                "user_name": user_name,
                "user_email": user_email,
                "total_amount": total_amount,
                "status": "pending_payment"
            }
            response = supabase.table("bookings").insert(booking).execute()
            
            return jsonify({
                "booking_id": response.data[0]["id"],
                "total_amount": total_amount,
                "message": "Seats reserved successfully. Please proceed to payment."
            })
        except Exception as e:
            print(f"Supabase error: {e}")
            return jsonify({"error": str(e)}), 500
    
    # In-memory fallback
    movie_seats = seats_data.get(movie_id, [])
    booked_seats = []
    for seat_id in seat_ids:
        seat = next((s for s in movie_seats if s["id"] == seat_id), None)
        if not seat:
            return jsonify({"error": f"Seat {seat_id} not found"}), 400
        if seat["status"] != "available":
            return jsonify({"error": f"Seat {seat['row']}{seat['number']} is already booked"}), 400
        booked_seats.append(seat)
    
    for seat_id in seat_ids:
        for s in movie_seats:
            if s["id"] == seat_id:
                s["status"] = "booked"
    
    total_amount = sum(seat["price"] for seat in booked_seats)
    booking_id = len(bookings_data) + 1
    booking = {
        "id": booking_id,
        "movie_id": movie_id,
        "seat_ids": seat_ids,
        "user_name": user_name,
        "user_email": user_email,
        "total_amount": total_amount,
        "status": "pending_payment"
    }
    bookings_data.append(booking)
    
    return jsonify({
        "booking_id": booking_id,
        "total_amount": total_amount,
        "message": "Seats reserved successfully. Please proceed to payment."
    })

@app.route("/api/payment", methods=["POST"])
def process_payment():
    data = request.json
    booking_id = data.get("booking_id")
    amount = data.get("amount")
    payment_method = data.get("payment_method", "card")
    
    if not booking_id or not amount:
        return jsonify({"error": "Booking ID and amount are required"}), 400
    
    if supabase:
        try:
            response = supabase.table("bookings").select("*").eq("id", booking_id).execute()
            if not response.data:
                return jsonify({"error": "Booking not found"}), 404
            
            booking = response.data[0]
            if booking["status"] == "paid":
                return jsonify({"error": "Payment already completed"}), 400
            
            if float(amount) != float(booking["total_amount"]):
                return jsonify({"error": f"Amount mismatch. Expected: {booking['total_amount']}"}), 400
            
            # Update booking status
            supabase.table("bookings").update({"status": "paid"}).eq("id", booking_id).execute()
            
            return jsonify({
                "message": "Payment successful!",
                "booking_id": booking_id,
                "amount": amount,
                "payment_method": payment_method,
                "status": "confirmed",
                "transaction_id": f"TXN{random.randint(100000, 999999)}"
            })
        except Exception as e:
            print(f"Supabase error: {e}")
            return jsonify({"error": str(e)}), 500
    
    # In-memory fallback
    booking = next((b for b in bookings_data if b["id"] == booking_id), None)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    
    if booking["status"] == "paid":
        return jsonify({"error": "Payment already completed"}), 400
    
    if float(amount) != float(booking["total_amount"]):
        return jsonify({"error": f"Amount mismatch. Expected: {booking['total_amount']}"}), 400
    
    booking["status"] = "paid"
    
    return jsonify({
        "message": "Payment successful!",
        "booking_id": booking_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "confirmed",
        "transaction_id": f"TXN{random.randint(100000, 999999)}"
    })

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "supabase_connected": supabase is not None})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
