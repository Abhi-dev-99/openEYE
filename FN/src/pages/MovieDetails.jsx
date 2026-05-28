import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

function MovieDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchMovieDetails()
  }, [id])

  const fetchMovieDetails = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_URL}/movies/${id}`)
      setMovie(response.data)
      setError(null)
    } catch (err) {
      setError('Failed to load movie details. Please try again later.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleBookTickets = () => {
    navigate(`/movie/${id}/seats`)
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading movie details...</div>
      </div>
    )
  }

  if (error || !movie) {
    return (
      <div className="container">
        <div className="error">{error || 'Movie not found'}</div>
        <button className="btn btn-secondary" onClick={() => navigate(-1)}>
          Go Back
        </button>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="movie-details">
        <div className="movie-details-header">
          <div className="movie-details-poster">
            <img src={movie.poster_url} alt={movie.title} />
          </div>
          <div className="movie-details-info">
            <h1 className="movie-details-title">{movie.title}</h1>
            <div className="movie-details-meta">
              <div className="meta-item">
                <div className="meta-label">Genre</div>
                <div className="meta-value">{movie.genre}</div>
              </div>
              <div className="meta-item">
                <div className="meta-label">Language</div>
                <div className="meta-value">{movie.language}</div>
              </div>
              <div className="meta-item">
                <div className="meta-label">Duration</div>
                <div className="meta-value">{movie.duration}</div>
              </div>
              <div className="meta-item">
                <div className="meta-label">Rating</div>
                <div className="meta-value">{movie.rating}</div>
              </div>
              <div className="meta-item">
                <div className="meta-label">Show Date</div>
                <div className="meta-value">{movie.show_date}</div>
              </div>
              <div className="meta-item">
                <div className="meta-label">Show Time</div>
                <div className="meta-value">{movie.show_time}</div>
              </div>
            </div>
            <div className="movie-details-description">
              <p><strong>Director:</strong> {movie.director}</p>
              <p><strong>Cast:</strong> {movie.cast}</p>
              <p style={{ marginTop: '1rem' }}>{movie.description}</p>
            </div>
            <div>
              <button className="btn btn-primary" onClick={handleBookTickets}>
                Book Tickets (₹{movie.price})
              </button>
              <button className="btn btn-secondary" onClick={() => navigate(-1)}>
                Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MovieDetails
