# Alibaba Cloud Function Compute deployment

This directory is a dependency-free Node.js web function for FIT5032 Assessed Lab 9.

- Runtime: custom runtime based on Node.js 20 or later
- Startup command: `npm start`
- Listening port: `9000` (or `FC_SERVER_PORT` when supplied by Function Compute)
- Instance: elastic, 0.35 vCPU, 512 MB memory, 512 MB disk
- Minimum instances: 0
- Network: public internet only; do not attach a VPC
- Routes: `/health`, `/api/books/count`, `/api/books/marketplace`

The function is isolated from all existing Alibaba Cloud servers and reads the existing public
Cloud Firestore REST endpoint. Deploy it to the China (Hong Kong) region so the Google API is
reachable without attaching any existing VPC or server resources.
