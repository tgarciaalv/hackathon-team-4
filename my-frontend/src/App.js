import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [dayOfWeek, setDayOfWeek] = useState('');
  const [originAirportId, setOriginAirportId] = useState('');
  const [destAirportId, setDestAirportId] = useState('');
  const [carrier, setCarrier] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('https://expert-space-guide-g4gq79j46q2964v.github.dev/predict', {
        day_of_week: parseInt(dayOfWeek),
        origin_airport_id: parseInt(originAirportId),
        dest_airport_id: parseInt(destAirportId),
        carrier: carrier
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="App">
      <h1>Flight Delay Prediction</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Day of the Week:
          <input
            type="number"
            value={dayOfWeek}
            onChange={(e) => setDayOfWeek(e.target.value)}
          />
        </label>
        <br />
        <label>
          Origin Airport ID:
          <input
            type="number"
            value={originAirportId}
            onChange={(e) => setOriginAirportId(e.target.value)}
          />
        </label>
        <br />
        <label>
          Destination Airport ID:
          <input
            type="number"
            value={destAirportId}
            onChange={(e) => setDestAirportId(e.target.value)}
          />
        </label>
        <br />
        <label>
          Carrier:
          <input
            type="text"
            value={carrier}
            onChange={(e) => setCarrier(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Predict</button>
      </form>
      {result && (
        <div>
          <h2>Prediction Result</h2>
          <p>{JSON.stringify(result)}</p>
        </div>
      )}
    </div>
  );
}

export default App;