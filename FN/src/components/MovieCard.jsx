import { useNavigate } from 'react-router-dom'

function MovieCard({ movie }) {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(`/movie/${movie.id}`)
  }

  return (
    <div className="movie-card" onClick={handleClick}>
      <img src={movie.poster_url} alt={movie.title} loading="lazy" />
      <div className="movie-card-info">
        <div className="movie-card-title">{movie.title}</div>
        <div className="movie-card-meta">
          <span>{movie.genre}</span>
          <span>₹{movie.price}</span>
        </div>
      </div>
    </div>
  )
}

export default MovieCard
