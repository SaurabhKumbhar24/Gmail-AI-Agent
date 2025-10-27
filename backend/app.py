import sys
import json
import pickle
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google_auth_oauthlib.flow import Flow
from fastapi.responses import RedirectResponse, HTMLResponse
from gmail_mcp.auth import save_credentials, logout as auth_logout
from gmail_client import gmail_client
from models import EmailListRequest, EmailReadRequest, EmailSendRequest, ChatMessage, ChatResponse
from typing import Optional
from llm_client import llm_client

app = FastAPI(title="MCP Client")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

TOKEN_PATH = Path.home() / '.gmail_mcp_token.pickle'
CREDENTIALS_PATH = './gmail_mcp_credentials.json'
OAUTH_PORT = 8080
REDIRECT_URI = f'http://localhost:{OAUTH_PORT}/auth/callback'

oauth_flow: Optional[Flow] = None

@app.get("/auth/start")
async def auth_start():
    global oauth_flow

    oauth_flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = oauth_flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    return RedirectResponse(url=authorization_url)

@app.get("/auth/callback")
async def auth_callback(code: str, state: str):
    global oauth_flow

    if not oauth_flow:
        raise HTTPException(status_code=400, detail="OAuth flow not started")
    
    try:
        oauth_flow.fetch_token(code=code)
        token = oauth_flow.credentials
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(token, f)

        sys.path.insert(0, str(Path(__file__).parent))
        save_credentials(token)

        return HTMLResponse(
            """
            <html>
                <head>
                    <title>Authentication Successful</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background: #f0f0f0;
                        }
                        .container {
                            background: white;
                            padding: 40px;
                            border-radius: 10px;
                            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                            text-align: center;
                        }
                        h1 { color: #000000; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>✓ Authentication Successful!</h1>
                        <p>Redirecting back to app...</p>
                        <script>
                            setTimeout(() => {
                                window.location.href = 'http://localhost:5173';
                            }, 2000);
                        </script>
                    </div>
                </body>
            </html>
            """
        )
    
    except Exception as e:
        print(f"Error fetching token: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/api/auth/status")
async def auth_status():
    """Check if user is authenticated"""
    result = await gmail_client.call_tool("get_auth_status", {})
    return json.loads(result)

@app.post("/api/auth/logout")
async def logout():
    """Logout and clear credentials"""
    try:
        auth_logout()
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/list")
async def list_emails(request: EmailListRequest):
    """List emails"""
    result = await gmail_client.call_tool("list_emails", request.model_dump())
    return json.loads(result)

@app.post("/api/emails/read")
async def read_email(request: EmailReadRequest):
    """Read email"""
    result = await gmail_client.call_tool("read_email", request.model_dump())
    return json.loads(result)

@app.post("/api/emails/send")
async def send_email(request: EmailSendRequest):
    """Send email"""
    result = await gmail_client.call_tool("send_email", request.model_dump())
    return json.loads(result)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat with the AI"""
    if llm_client is None:
        return ChatResponse(
            response="",
            error="LLM is not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    try:
        
        response_text = await llm_client.chat(message.message)
        
        print(f"Chat response: {response_text[:100]}...")
        
        return ChatResponse(
            response=response_text,
            error=None
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(
            response="",
            error=f"An error occurred: {str(e)}"
        )


@app.get("/api/chat/status")
async def chat_status():
    
    if llm_client:
        import os
        provider = os.getenv('LLM_PROVIDER', 'gemini')
        return {
            "available": True,
            "provider": provider,
            "message": f"Chat is available using {provider}"
        }
    else:
        return {
            "available": False,
            "provider": None,
            "message": "Chat is not available. Configure LLM provider."
        }
    
@app.on_event("startup")
async def startup_event():
    """Called when FastAPI starts"""
    print("=" * 70)
    print("Starting Gmail MCP Client API")
    print("=" * 70)
    gmail_client.start()
    print("✓ MCP client initialized")
    
    if llm_client:
        print("✓ LLM chat enabled")
    else:
        print("⚠ LLM chat disabled (no API key configured)")
    
    print(f"✓ API running at: http://localhost:{OAUTH_PORT}")
    print("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Called when FastAPI shuts down"""
    print("\nShutting down Gmail MCP Client API...")
    gmail_client.stop()
    print("Have a gr8 day!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)