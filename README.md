# Hwang Library - FIT5032 Assessed Lab 9

Vue 3 and Cloudflare Pages Functions implementation of the FIT5032 cloud-functions lab. It provides:

- `/BookCounter`: calls a cloud function that counts the live Firestore `books` collection
- `/DataMarketplace`: converts the live Firestore collection into priced educational data offers
- `/WeatherCheck`: current-location and city weather search in Celsius
- `/CountBookAPI`: author and book counts from `authors.json`
- `/GetAllBookAPI`: all books formatted as JSON
- `/api/books/count`: Cloudflare Pages Function backed by Cloud Firestore
- `/api/books/marketplace`: Cloudflare Pages Function for the data marketplace

## Run locally

```sh
npm install
npm run dev
```

The weather page works without configuration through Open-Meteo. To use the OpenWeather service shown in the lab notes, copy `.env.example` to `.env.local` and add a valid `VITE_OPENWEATHER_API_KEY`. Never commit the key.

Cloudflare Pages serves the Vue app and the functions from the same origin. For local UI development against a deployed function, set `VITE_LIBRARY_FUNCTION_BASE_URL` in `.env.local` to the deployed Pages URL.

## Verify

```sh
npm run type-check
npm run test:unit -- --run
npm run build
```
