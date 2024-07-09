
def get_weather_information(lat=0, lon=0, unit="celcius", date="1997-01-01"):
  # https://www.7timer.info/doc.php?lang=en
  # https://www.7timer.info/bin/astro.php?lon=113.2&lat=23.1&ac=0&unit=metric&output=json&tzshift=0
  results = '{ temperature: 16, sky: "cloudy" }'
  return results