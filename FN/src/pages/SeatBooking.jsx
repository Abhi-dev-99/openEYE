import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

function SeatBooking() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [seats, setSeats] = useState([])
  const [selectedSeats, setSelectedSeats] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [userName, setUserName] = useState('')
  const [userEmail, setUserEmail] = useState('')
  const [booking, setBooking] = useState(false)

  useEffect(() => {
    fetchMovieAndSeats()
  }, [id])

  const fetchMovieAndSeats = async () => {
    try {
      setLoading(true)
      const [movieRes, seatsRes] = await Promise.all([
        axios.get(`${API_URL}/movies/${id}`),
        axios.get(`${API_URL}/movies/${id}/seats`)
      ])
      setMovie(movieRes.data)
      setSeats(seatsRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to load seat information. Please try again later.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSeatClick = (seat) => {
    if (seat.status === 'booked') return

    setSelectedSeats((prev) => {
      if (prev.find((s) => s.id === seat.id)) {
        return prev.filter((s) => s.id !== seat.id)
      }
      return [...prev, seat]
    })
  }

  const getSeatClass = (seat) => {
    if (seat.status === 'booked') return 'seat booked'
    if (selectedSeats.find((s) => s.id === seat.id)) return 'seat selected'
    return 'seat available'
  }

  const totalAmount = selectedSeats.reduce((sum, seat) => sum + seat.price, 0)

  const handleBooking = async () => {
    if (selectedSeats.length === 0) {
      alert('Please select at least one seat')
      return
    }
    if (!userName.trim() || !userEmail.trim()) {
      alert('Please enter your name and email')
      return
    }

    try {
      setBooking(true)
      const response = await axios.post(`${API_URL}/book`, {
        movie_id: parseInt(id),
        seat_ids: selectedSeats.map((s) => s.id),
        user_name: userName,
        user_email: userEmail
      })
      navigate(`/payment/${response.data.booking_id}`, {
        state: {
          totalAmount: response.data.total_amount,
          movie: movie,
          seats: selectedSeats
        }
      })
    } catch (err) {
      alert(err.response?.data?.error || 'Booking failed. Please try again.')
      console.error(err)
    } finally {
      setBooking(false)
    }
  }

  const groupedSeats = seats.reduce((acc, seat) => {
    if (!acc[seat.row]) acc[seat.row] = []
    acc[seat.row].push(seat)
    return acc
  }, {})

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading seats...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="seat-booking">
        <h1 className="page-title">{movie?.title} - Select Seats</h1>
        <p style={{ marginBottom: '1rem', color: '#a0a0a0' }}>
          {movie?.show_date} | {movie?.show_time}
        </p>

        <div className="screen">SCREEN</div>

        <div className="seats-container">
          {Object.entries(groupedSeats).map(([row, rowSeats]) => (
            <div key={row} className="seat-row">
              <span className="row-label">{row}</span>
              {rowSeats.map((seat) => (
                <div
                  key={seat.id}
                  className={getSeatClass(seat)}
                  onClick={() => handleSeatClick(seat)}
                  title={`${seat.row}${seat.number} - ₹${seat.price}`}
                >
                  {seat.number}
                </div>
              ))}
            </div>
          ))}
        </div>

        <div className="seat-legend">
          <div className="legend-item">
            <div className="legend-box available"></div>
            <span>Available</span>
          </div>
          <div className="legend-item">
            <div className="legend-box booked"></div>
            <span>Booked</span>
          </div>
          <div className="legend-item">
            <div className="legend-box selected"></div>
            <span>Selected</span>
          </div>
        </div>

        {selectedSeats.length > 0 && (
          <div className="booking-summary">
            <h3>Booking Summary</h3>
            {selectedSeats.map((seat) => (
              <div key={seat.id} className="summary-row">
                <span>
                  Seat {seat.row}
                  {seat.number}
                </span>
                <span>₹{seat.price}</span>
              </div>
            ))}
            <div className="summary-row total">
              <span>Total</span>
              <span>₹{totalAmount}</span>
            </div>
          </div>
        )}

        <div style={{ maxWidth: '400px', margin: '0 auto 1.5rem' }}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Enter your name"
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={userEmail}
              onChange={(e) => setUserEmail(e.target.value)}
              placeholder="Enter your email"
            />
          </div>
        </div>

        <button
          className="btn btn-primary"
          onClick={handleBooking}
          disabled={booking || selectedSeats.length === 0}
        >
          {booking ? 'Processing...' : `Proceed to Payment (₹${totalAmount})`}
        </button>
        <button className="btn btn-secondary" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>
    </div>
  )
}

export default SeatBooking
