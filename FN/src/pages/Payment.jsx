import { useState } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

function Payment() {
  const { bookingId } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
  const { totalAmount, movie, seats } = location.state || {}

  const [cardNumber, setCardNumber] = useState('')
  const [cardName, setCardName] = useState('')
  const [expiry, setExpiry] = useState('')
  const [cvv, setCvv] = useState('')
  const [processing, setProcessing] = useState(false)
  const [success, setSuccess] = useState(false)
  const [paymentDetails, setPaymentDetails] = useState(null)

  const handlePayment = async (e) => {
    e.preventDefault()

    if (!cardNumber || !cardName || !expiry || !cvv) {
      alert('Please fill in all payment details')
      return
    }

    try {
      setProcessing(true)
      const response = await axios.post(`${API_URL}/payment`, {
        booking_id: parseInt(bookingId),
        amount: totalAmount,
        payment_method: 'card'
      })
      setPaymentDetails(response.data)
      setSuccess(true)
    } catch (err) {
      alert(err.response?.data?.error || 'Payment failed. Please try again.')
      console.error(err)
    } finally {
      setProcessing(false)
    }
  }

  if (success) {
    return (
      <div className="container">
        <div className="payment-page">
          <div className="success-message">
            <div className="success-icon">✅</div>
            <h2>Payment Successful!</h2>
            <p>Your booking has been confirmed.</p>

            <div className="ticket-info">
              <p>
                <strong>Transaction ID:</strong> {paymentDetails?.transaction_id}
              </p>
              <p>
                <strong>Movie:</strong> {movie?.title}
              </p>
              <p>
                <strong>Date:</strong> {movie?.show_date}
              </p>
              <p>
                <strong>Time:</strong> {movie?.show_time}
              </p>
              <p>
                <strong>Seats:</strong>{' '}
                {seats?.map((s) => `${s.row}${s.number}`).join(', ')}
              </p>
              <p>
                <strong>Amount Paid:</strong> ₹{totalAmount}
              </p>
            </div>

            <button className="btn btn-primary" onClick={() => navigate('/')}
            >
              Back to Home
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="payment-page">
        <h1 className="page-title">Payment</h1>

        <div className="booking-summary" style={{ textAlign: 'left' }}>
          <h3>Order Summary</h3>
          <div className="summary-row">
            <span>Movie</span>
            <span>{movie?.title}</span>
          </div>
          <div className="summary-row">
            <span>Seats</span>
            <span>{seats?.map((s) => `${s.row}${s.number}`).join(', ')}</span>
          </div>
          <div className="summary-row total">
            <span>Total Amount</span>
            <span>₹{totalAmount}</span>
          </div>
        </div>

        <form className="payment-form" onSubmit={handlePayment}>
          <h3 style={{ marginBottom: '1.5rem', color: '#e94560' }}>
            Dummy Card Payment
          </h3>

          <div className="form-group">
            <label>Card Number</label>
            <input
              type="text"
              value={cardNumber}
              onChange={(e) => setCardNumber(e.target.value)}
              placeholder="1234 5678 9012 3456"
              maxLength={19}
            />
          </div>

          <div className="form-group">
            <label>Card Holder Name</label>
            <input
              type="text"
              value={cardName}
              onChange={(e) => setCardName(e.target.value)}
              placeholder="John Doe"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group">
              <label>Expiry Date</label>
              <input
                type="text"
                value={expiry}
                onChange={(e) => setExpiry(e.target.value)}
                placeholder="MM/YY"
                maxLength={5}
              />
            </div>

            <div className="form-group">
              <label>CVV</label>
              <input
                type="password"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                placeholder="123"
                maxLength={4}
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-success"
            style={{ width: '100%', marginTop: '1rem' }}
            disabled={processing}
          >
            {processing
              ? 'Processing...'
              : `Pay ₹${totalAmount}`}
          </button>
        </form>

        <p style={{ marginTop: '1rem', color: '#a0a0a0', fontSize: '0.85rem' }}>
          This is a dummy payment for demo purposes. No real transaction will be processed.
        </p>

        <button className="btn btn-secondary" onClick={() => navigate(-1)}>
          Cancel
        </button>
      </div>
    </div>
  )
}

export default Payment
