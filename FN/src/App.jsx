import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import MovieDetails from './pages/MovieDetails'
import SeatBooking from './pages/SeatBooking'
import Payment from './pages/Payment'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <a href="/">🎬 MovieBook</a>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/movie/:id" element={<MovieDetails />} />
        <Route path="/movie/:id/seats" element={<SeatBooking />} />
        <Route path="/payment/:bookingId" element={<Payment />} />
      </Routes>
    </div>
  )
}

export default App
