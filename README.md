# Gmail AI Agent

A modern, AI-powered Gmail client that combines the power of Google's Gemini AI with Gmail's API through the Model Context Protocol (MCP). This application provides an intelligent chat interface for managing your emails and a traditional email viewer, all wrapped in a clean, minimalist black-and-white UI.

![Gmail AI Agent](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-19.1-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green)

## Working Vid!

https://github.com/user-attachments/assets/b24016af-80bc-412a-8ce9-6aac37317a9b



## 🌟 Features

### 🤖 AI-Powered Chat Interface
- **Natural Language Email Management**: Ask the AI to list, read, or send emails using conversational language
- **Smart Function Calling**: Gemini AI intelligently decides when to call Gmail functions vs. respond conversationally
- **Context-Aware Responses**: The AI understands your intent and provides relevant email information
- **Fallback Handling**: Robust error handling ensures you always get a response, even if the AI encounters issues

### 📧 Traditional Email Interface
- **Email List View**: Browse your emails with sender, subject, and date information
- **Email Reader**: Read full email content with a clean, distraction-free interface
- **Search Functionality**: Search through your emails with Gmail's powerful query syntax
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🔐 Secure Authentication
- **Google OAuth 2.0**: Secure authentication using Google's OAuth flow
- **Token Management**: Automatic token refresh and secure credential storage
- **Easy Logout**: One-click logout to clear credentials and sign out

### 🎨 Modern UI/UX
- **Minimalist Design**: Clean black-and-white color scheme for distraction-free email management
- **Smooth Scrolling**: Properly implemented scroll areas for email lists and content
- **Responsive Layout**: Adapts to different screen sizes and devices
- **Loading States**: Clear visual feedback during data fetching

## 🏗️ Architecture

### Backend (FastAPI + MCP)
```
backend/
├── app.py                 # FastAPI application with OAuth and API endpoints
├── gmail_client.py        # MCP client for Gmail server communication
├── llm_client.py          # Gemini AI integration with function calling
├── models.py              # Pydantic models for request/response validation
└── gmail_mcp/
    ├── gmail_server.py    # MCP server with Gmail API tools
    └── auth.py            # Gmail authentication and credential management
```

### Frontend (React + TypeScript + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── AuthGuard.tsx      # Authentication wrapper component
│   │   ├── ChatInterface.tsx  # AI chat interface
│   │   ├── EmailList.tsx      # Email list sidebar
│   │   └── EmailView.tsx      # Email content viewer
│   ├── services/
│   │   └── api.ts             # API service for backend communication
│   └── types/
│       └── index.ts           # TypeScript type definitions
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- Google Cloud Project with Gmail API enabled
- Gemini API key (from Google AI Studio)

### 1. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials JSON file
   - Save it as `backend/gmail_mcp_credentials.json`

### 2. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key for later use

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run the server
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

### 5. Access the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Click "Sign in with Google" to authenticate
3. Grant the necessary Gmail permissions
4. Start using the AI chat or browse your emails!

## 🎯 Use Cases

### 1. **Quick Email Triage**
- "Show me my recent emails"
- "List unread emails from the last week"
- "Find emails from john@example.com"

### 2. **Email Reading**
- "Read the first email"
- "Show me the email from Sarah"
- "Open the email about the meeting"

### 3. **Email Composition**
- "Send an email to jane@example.com with subject 'Meeting Tomorrow' and body 'Let's meet at 3 PM'"
- "Compose an email to the team about the project update"

### 4. **Casual Interaction**
- "Hi, how are you?" - The AI responds conversationally without calling functions
- "What can you help me with?" - Get information about capabilities
- "Thanks!" - Natural conversation without unnecessary function calls

### 5. **Traditional Email Management**
- Switch to "Emails" view for a familiar email client experience
- Browse, search, and read emails with a clean interface
- Perfect for when you prefer manual email management

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **MCP (Model Context Protocol)**: Standardized protocol for LLM-tool integration
- **Google Gemini AI**: Advanced AI model with function calling capabilities
- **Gmail API**: Official Google API for Gmail integration
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **React 19**: Latest version of the popular UI library
- **TypeScript**: Type-safe JavaScript for better development experience
- **Vite**: Next-generation frontend tooling
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component primitives
- **Lucide React**: Beautiful, consistent icon set

## 📝 API Endpoints

### Authentication
- `GET /auth/start` - Initiate OAuth flow
- `GET /auth/callback` - OAuth callback handler
- `GET /api/auth/status` - Check authentication status
- `POST /api/auth/logout` - Logout and clear credentials

### Email Operations
- `POST /api/emails/list` - List emails with optional filters
- `POST /api/emails/read` - Read a specific email
- `POST /api/emails/send` - Send a new email

### Chat
- `POST /api/chat` - Send a message to the AI assistant
- `GET /api/chat/status` - Check if chat is available

## 🔒 Security & Privacy

- **OAuth 2.0**: Industry-standard authentication protocol
- **Local Token Storage**: Credentials stored securely on your machine
- **No Data Collection**: Your emails and data never leave your device
- **Secure Communication**: All API calls use HTTPS in production
- **Minimal Permissions**: Only requests necessary Gmail scopes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google for the Gmail API and Gemini AI
- Anthropic for the Model Context Protocol specification
- The FastAPI and React communities for excellent documentation

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, React, and Google Gemini AI**

