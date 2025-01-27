import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/resumes/')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h1>Datos desde Django:</h1>
      <ul>
        {data.map(item => (
          <li key={item.id}>{item.full_name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;