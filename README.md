# Hwang Library - FIT5032 Assessed Lab 11

Vue 3 application deployed for FIT5032 Assessed Lab 11. It provides:

- `/WeatherCheck`: current-location and city weather search in Celsius
- `/CountBookAPI`: author and book counts from `authors.json`
- `/GetAllBookAPI`: all books formatted as JSON

## Run locally

```sh
npm install
npm run dev
```

The weather page works without configuration through Open-Meteo. To use the OpenWeather service shown in the lab notes, copy `.env.example` to `.env.local` and add a valid `VITE_OPENWEATHER_API_KEY`. Never commit the key.

## Deploy to Cloudflare Pages

Connect this repository to Cloudflare Pages and use these build settings:

- Framework preset: `Vue`
- Build command: `npm run build`
- Build output directory: `dist`

No environment variables are required for the default Open-Meteo weather service. The
`public/_redirects` file makes Vue Router history routes such as `/WeatherCheck` work when
they are opened directly on the deployed domain.

## Verify

```sh
npm run type-check
npm run test:unit -- --run
npm run build
```
