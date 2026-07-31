# Hwang Library - FIT5032 Assessed Lab 9

Vue 3 and Alibaba Cloud Function Compute implementation of the FIT5032 cloud-functions lab. It provides:

- `/BookCounter`: calls a cloud function that counts the live Firestore `books` collection
- `/DataMarketplace`: converts the live Firestore collection into priced educational data offers
- `/WeatherCheck`: current-location and city weather search in Celsius
- `/CountBookAPI`: author and book counts from `authors.json`
- `/GetAllBookAPI`: all books formatted as JSON
- `/api/books/count`: Alibaba Cloud web-function route backed by Cloud Firestore
- `/api/books/marketplace`: Alibaba Cloud web-function route for the data marketplace

## Run locally

```sh
npm install
npm run dev
```

The weather page works without configuration through Open-Meteo. To use the OpenWeather service shown in the lab notes, copy `.env.example` to `.env.local` and add a valid `VITE_OPENWEATHER_API_KEY`. Never commit the key.

Alibaba Cloud Function Compute serves both API routes from the isolated web function in
`aliyun-function`. The production build uses the public Hong Kong Function Compute endpoint from
`.env.production`. Set `VITE_LIBRARY_FUNCTION_BASE_URL` in `.env.local` only when a local override
is needed. Cloudflare Pages may continue to host the static Vue build, but it is not the Lab 9
function host.

## Verify

```sh
npm run type-check
npm run test:unit -- --run
npm run build
cd aliyun-function && npm test
```
