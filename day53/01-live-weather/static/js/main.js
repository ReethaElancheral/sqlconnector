async function fetchWeather() {
  document.getElementById("loading").classList.remove("d-none");
  document.getElementById("weatherData").classList.add("d-none");

  try {
    let res = await fetch("/api/weather");
    let data = await res.json();

    document.getElementById("status").textContent = data.status;
    document.getElementById("temperature").textContent = data.temperature;
    document.getElementById("humidity").textContent = data.humidity;

    document.getElementById("loading").classList.add("d-none");
    document.getElementById("weatherData").classList.remove("d-none");
  } catch (error) {
    console.error("Error fetching weather:", error);
  }
}

// Fetch every 10 seconds
fetchWeather();
setInterval(fetchWeather, 10000);
