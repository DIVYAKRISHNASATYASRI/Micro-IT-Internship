const apiKey = 'b7d813eb467a4e36984152539252005'; // Replace with your actual WeatherAPI key

async function getWeather() {
  const city = document.getElementById("city").value;

  if (!city) {
    alert("Please enter a city name.");
    return;
  }

  const url = `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${city}&days=3`;

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (data.error) {
      document.getElementById("weather-info").innerHTML = `<p>${data.error.message}</p>`;
      return;
    }

    const current = data.current;
    const location = data.location;
    const forecast = data.forecast.forecastday;

    let output = `
      <h2>${location.name}, ${location.country}</h2>
      <p><strong>${current.condition.text}</strong></p>
      <img src="https:${current.condition.icon}" alt="icon">
      <p>Temperature: ${current.temp_c}°C</p>
      <p>Humidity: ${current.humidity}%</p>
      <p>Wind: ${current.wind_kph} kph</p>
      <h3>3-Day Forecast</h3>
      <ul>
    `;

    forecast.forEach(day => {
      output += `
        <li>
          <strong>${day.date}</strong> - ${day.day.condition.text}
          <br>🌡️ Min: ${day.day.mintemp_c}°C / Max: ${day.day.maxtemp_c}°C
        </li>
      `;
    });

    output += `</ul>`;
    document.getElementById("weather-info").innerHTML = output;

  } catch (error) {
    document.getElementById("weather-info").innerHTML = "<p>Error fetching data.</p>";
  }
}
