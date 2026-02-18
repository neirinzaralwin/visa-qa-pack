# Visa AI Assistant Frontend

A Next.js frontend for the Visa AI Assistant application.

## Features

- Real-time chat interface with AI assistant
- Modern, responsive design with Tailwind CSS
- TypeScript support for type safety
- Integration with backend API endpoints

## Getting Started

### AI Training Interface
- **Sample Training Data**: Pre-loaded conversation examples
- **Batch Training**: Train multiple examples simultaneously
- **Performance Tracking**: Monitor training progress and results
- **Comparison View**: Compare AI responses with expected replies
- **Statistics Dashboard**: Track training metrics and success rates

### Analytics Dashboard
- **Conversation Metrics**: Total conversations, response times, satisfaction scores
- **Topic Analysis**: Most common visa questions and topics
- **Dropoff Analysis**: Identify where customers abandon the process
- **Trend Visualization**: Weekly/monthly conversation trends
- **AI Performance**: Response quality, tone accuracy, and correctness metrics

## 🛠️ Technology Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with responsive design
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React Hooks (useState, useEffect, useRef)

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API server running (see backend documentation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd complete_chatbot_pack/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local` and configure:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000  # Your backend API URL
   ```

4. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
frontend/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main page with navigation
├── components/
│   ├── ChatInterface.tsx    # Chat interface component
│   ├── AdminPanel.tsx       # Admin panel for prompt management
│   ├── TrainingInterface.tsx # AI training interface
│   ├── AnalyticsDashboard.tsx # Analytics dashboard
│   └── Navigation.tsx       # Navigation sidebar
├── lib/
│   └── api.ts              # API integration layer
├── public/                 # Static assets
├── .env.local.example      # Environment variables template
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind configuration
└── tsconfig.json          # TypeScript configuration
```

## 🔧 Configuration

### API Integration

The frontend communicates with the backend API through the `/lib/api.ts` module. Key endpoints:

- `POST /generate-reply` - Generate AI responses
- `POST /improve-ai` - Auto-improve AI prompts
- `POST /improve-ai-manually` - Manual prompt improvements
- `GET /health` - Health check

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:5000` |

## 🎯 Usage Guide

### For Users

1. **Chat Interface**: Start conversations about visa applications
2. **Ask Questions**: Use suggested questions or type your own
3. **Provide Feedback**: Rate AI responses to improve quality
4. **Copy Responses**: Save important information for later

### For Administrators

1. **Admin Panel**: 
   - View current AI prompts
   - Make manual improvements
   - Test changes in real-time
   - Use quick action templates

2. **Training Interface**:
   - Train AI with sample conversations
   - Compare AI vs expected responses
   - Monitor training progress
   - Track improvement metrics

3. **Analytics Dashboard**:
   - Monitor conversation volume
   - Analyze customer satisfaction
   - Identify dropoff points
   - Track AI performance trends

## 🎨 Design Principles

- **User-Centric**: Intuitive interface with clear visual hierarchy
- **Responsive**: Optimized for all device sizes
- **Accessible**: Semantic HTML and ARIA labels
- **Performant**: Optimized loading and smooth interactions
- **Modern**: Clean, professional design with subtle animations

## 🔄 Development Workflow

### Adding New Features

1. Create new components in `/components/`
2. Add API functions to `/lib/api.ts`
3. Update TypeScript types as needed
4. Test responsive design
5. Update documentation

### Code Style

- TypeScript for type safety
- Tailwind CSS for styling
- Functional components with hooks
- Proper error handling
- Semantic HTML structure

## 🚀 Deployment

### Build for Production

```bash
npm run build
npm start
```

### Environment Setup

1. Set production environment variables
2. Configure API endpoints
3. Set up proper CORS on backend
4. Configure domain and SSL

### Recommended Platforms

- **Vercel** (Recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **DigitalOcean App Platform**

## 🔍 API Integration Details

### Error Handling

- Network errors with retry functionality
- Graceful degradation when API is unavailable
- User-friendly error messages
- Loading states and indicators

### State Management

- Local component state for UI interactions
- No external state management required
- Optimistic updates for better UX
- Proper cleanup and memory management

## 📊 Analytics & Monitoring

### Frontend Metrics

- Page load times
- Interaction rates
- Error rates
- User engagement

### Business Metrics

- Conversation volume
- User satisfaction scores
- AI response accuracy
- Dropoff rates

## 🤝 Contributing

1. Follow the existing code style
2. Add TypeScript types for new props
3. Test on multiple screen sizes
4. Update documentation
5. Ensure accessibility standards

## 📝 License

This project is part of the Issa Compass Vibe Hackathon submission.

## 🆘 Support

For technical support or questions:
- Check the [API documentation](../api/README.md)
- Review the [main project README](../README.md)
- Contact the development team

---

Built with ❤️ for the Issa Compass Vibe Hackathon 2024
