# Visa AI Assistant Frontend

A Next.js frontend for the Visa AI Assistant application.

## Features

- Real-time chat interface with AI assistant
- Modern, responsive design with Tailwind CSS
- TypeScript support for type safety
- Integration with backend API endpoints

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   ```
   Update `NEXT_PUBLIC_API_URL` to point to your backend API.

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

- `app/` - Next.js App Router pages and layouts
- `components/` - React components
- `lib/` - Utility functions and API client
- `public/` - Static assets

## API Integration

The frontend connects to the backend API at the configured URL. Make sure your backend server is running before using the frontend.

## Build for Production

```bash
npm run build
npm start
```
