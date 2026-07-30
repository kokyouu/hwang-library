# Hwang Library - FIT5032 Lab 10

Vue 3 implementation of the FIT5032 API lab. It provides:

- `/WeatherCheck`: current-location and city weather search in Celsius
- `/CountBookAPI`: author and book counts from `authors.json`
- `/GetAllBookAPI`: all books formatted as JSON

## Run locally

```sh
npm install
npm run dev
```

The weather page works without configuration through Open-Meteo. To use the OpenWeather service shown in the lab notes, copy `.env.example` to `.env.local` and add a valid `VITE_OPENWEATHER_API_KEY`. Never commit the key.

## Verify

```sh
npm run type-check
npm run test:unit -- --run
npm run build
```
