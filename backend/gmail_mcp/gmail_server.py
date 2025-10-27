import json
import base64
from typing import Optional
from email.mime.text import MIMEText
from mcp.server.fastmcp import FastMCP
from googleapiclient.errors import HttpError
from .auth import get_gmail_service, ensure_auth

mcp = FastMCP("Gmail MCP Server")

@mcp.tool()
def get_auth_status() -> str:
    """Check if the user is authenticated with Gmail."""

    service = get_gmail_service()
    return json.dumps({
        "authenticated": service is not None,
        "message": "Authenticated with Gmail" if service else "Not authenticated with Gmail"
    })

@mcp.tool()
def list_emails(max_results: int = 10, query: Optional[str] = "") -> str:
    """List emails from the user's Gmail account."""

    service = ensure_auth()
    try:
        results = service.users().messages().list(
            userId="me",
            maxResults=min(max_results, 100),
            q=query
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            return json.dumps({"status": 200, "message": "No emails found", "data": {"count": 0, "messages": []}})

        email_data = []
        for message in messages:
            message_data = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "Date"]
            ).execute()
            headers = {header["name"]: header["value"] for header in message_data["payload"]["headers"]}
            email_data.append({
                "id": message["id"],
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", "")
            })

        return json.dumps({
            "status": 200,
            "message": "Emails listed successfully",
            "data":{
                "count": len(email_data),
                "messages": email_data
            }
        })
    
    except HttpError as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
    except Exception as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
@mcp.tool()
def read_email(email_id: str) -> str:
    """Read the content of an email."""

    service = ensure_auth()
    try:
        messages = service.users().messages().get(
            userId="me",
            id=email_id,
            format="full"
        ).execute()

        headers = {header["name"]: header["value"] for header in messages["payload"]["headers"]}

        body = ""
        if "parts" in messages["payload"]:
            for part in messages["payload"]["parts"]:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode('utf-8')
                    break
        elif 'body' in messages["payload"] and "data" in messages["payload"]["body"]:
            body = base64.urlsafe_b64decode(messages["payload"]["body"]["data"]).decode('utf-8')
        
        return json.dumps({
            "status": 200,
            "message": "Email read successfully",
            "data": {
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", ""),
                "body": body
            }
        })
    
    except HttpError as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
    except Exception as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""

    service = ensure_auth()

    try:
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject

        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())

        return json.dumps({
            "status": 200,
            "message": "Email sent successfully",
            "data": send_message['id']
        })
    
    except HttpError as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
    except Exception as error:
        return json.dumps({"status": 500, "message": f"An error occurred: {error}" ,"data": str(error)})
    
if __name__ == "__main__":
    mcp.run()