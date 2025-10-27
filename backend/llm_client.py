import os
from typing import List, Dict, Any
from gmail_client import gmail_client
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiLLMClient:

    def __init__(self, model: str = "gemini-2.5-flash"):
        
        try:
            
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found. ")
            
            genai.configure(api_key=api_key)

            self.model_name = model

            self.model = genai.GenerativeModel(
                model_name=model,
                tools=self._get_function_declarations(),
                system_instruction=(
                    "You are a helpful Gmail assistant. "
                    "IMPORTANT: Do NOT call any functions unless the user explicitly requests an email-related action. "
                    "\n\nCall functions ONLY for these requests:"
                    "\n- Listing/showing/checking emails (use list_emails)"
                    "\n- Reading/opening a specific email (use read_email)"
                    "\n- Sending/composing an email (use send_email)"
                    "\n- Checking authentication status (use get_auth_status)"
                    "\n\nDo NOT call functions for:"
                    "\n- Greetings (hi, hello, how are you, etc.)"
                    "\n- General questions or conversation"
                    "\n- Asking about capabilities"
                    "\n- Any non-email-specific requests"
                    "\n\nRespond naturally and conversationally without using tools for casual interactions."
                )
            )

            self.chat_session = self.model.start_chat(history=[])
            
            print(f"Gemini LLM client initialized (model: {model})")
            
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini: {e}")
    
    def _get_function_declarations(self) -> List[Dict[str, Any]]:

        functions = [
            genai.protos.FunctionDeclaration(
                name="get_auth_status",
                description="Check if the user is authenticated with Gmail. ONLY use this when the user explicitly asks about authentication status or before performing Gmail operations.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={}
                )
            ),
            genai.protos.FunctionDeclaration(
                name="list_emails",
                description=(
                    "List emails from the user's Gmail inbox. "
                    "ONLY use this when the user explicitly asks to see, list, check, or search their emails. "
                    "DO NOT use for greetings, general questions, or casual conversation. "
                    "Supports Gmail search query syntax for filtering."
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "max_results": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Maximum number of emails to return (1-100). Default is 10."
                        ),
                        "query": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description=(
                                "Gmail search query to filter emails. Examples:\n"
                                "- 'is:unread' for unread emails\n"
                                "- 'from:user@example.com' for emails from specific sender\n"
                                "- 'subject:meeting' for emails with 'meeting' in subject\n"
                                "- 'has:attachment' for emails with attachments\n"
                                "- 'after:2024/01/01' for emails after a date\n"
                                "- Empty string for all emails"
                            )
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="read_email",
                description=(
                    "Read the full content of a specific email by its ID. "
                    "ONLY use this when the user explicitly asks to read, open, or view a specific email. "
                    "DO NOT use for greetings or general questions. "
                    "You must have the email ID from list_emails first."
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "email_id": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The Gmail message ID to read (obtained from list_emails)"
                        )
                    },
                    required=["email_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="send_email",
                description=(
                    "Send an email via the user's Gmail account. "
                    "ONLY use this when the user explicitly asks to send, compose, or write an email. "
                    "DO NOT use for greetings or general questions."
                ),
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "to": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Recipient email address (e.g., 'user@example.com')"
                        ),
                        "subject": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Email subject line"
                        ),
                        "body": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Email body content in plain text"
                        )
                    },
                    required=["to", "subject", "body"]
                )
            )
        ]
        
        return functions
    
    async def _call_mcp_tool(self, function_name: str, function_args: Dict[str, Any]) -> Dict[str, Any]:
        print(f"  Calling MCP tool: {function_name}")

        try:
            # Call the MCP server through gmail_client
            result_str = await gmail_client.call_tool(function_name, function_args)

            # Parse the JSON string returned by the MCP tool
            import json
            result = json.loads(result_str)

            return result

        except Exception as e:
            print(f"Tool error: {e}")
            error_result = {
                "status": 500,
                "message": f"Error calling tool: {str(e)}",
                "data": None
            }
            return error_result
    
    async def chat(self, user_message: str) -> str:

        # Send message to Gemini
        response = self.chat_session.send_message(user_message)
        
        function_calls = []
        for part in response.parts:
            if hasattr(part, 'function_call'):
                function_calls.append(part.function_call)
        
        # Handle function calls
        if function_calls:
            print(f"\nGemini wants to call {len(function_calls)} function(s)")
            
            function_responses = []
            
            for function_call in function_calls:
                function_name = function_call.name

                function_args = {}
                # Check if args exist before iterating
                if function_call.args:
                    for key, value in function_call.args.items():
                        if hasattr(value, 'string_value'):
                            function_args[key] = value.string_value
                        elif hasattr(value, 'number_value'):
                            function_args[key] = int(value.number_value)
                        elif hasattr(value, 'bool_value'):
                            function_args[key] = value.bool_value
                        else:
                            function_args[key] = str(value)

                print(f"\nFunction call: {function_name}")
                print(f"  Args: {function_args}")
                
                result = await self._call_mcp_tool(function_name, function_args)
                                
                function_response = genai.protos.FunctionResponse(
                    name=function_name,
                    response={"result": result}
                )
                
                function_responses.append(function_response)
            
            print(f"\nSending {len(function_responses)} function result(s) to Gemini")

            try:
                response = self.chat_session.send_message(
                    genai.protos.Content(
                        parts=[
                            genai.protos.Part(function_response=fr)
                            for fr in function_responses
                        ]
                    )
                )
            except Exception as e:
                print(f"Error getting response from Gemini: {e}")
                # Generate a fallback response based on the function results
                fallback_text = self._generate_fallback_response(function_responses)
                print(f"\nAssistant (fallback): {fallback_text}\n")
                return fallback_text

        final_text = ""
        for part in response.parts:
            if hasattr(part, 'text'):
                final_text += part.text

        print(f"\nAssistant: {final_text}\n")

        return final_text

    def _generate_fallback_response(self, function_responses) -> str:
        """Generate a fallback response when Gemini fails to respond after function calls."""
        if not function_responses:
            return "I encountered an error processing your request. Please try again."

        # Get the first function response
        first_response = function_responses[0]
        result = first_response.response.get("result", {})

        # Generate response based on function name
        function_name = first_response.name

        if function_name == "send_email":
            if result.get("status") == 200:
                return "✓ Email sent successfully!"
            else:
                return f"Failed to send email: {result.get('message', 'Unknown error')}"

        elif function_name == "list_emails":
            if result.get("status") == 200:
                data = result.get("data", {})
                count = data.get("count", 0)
                messages = data.get("messages", [])

                if count == 0:
                    return "You have no emails."

                response = f"Found {count} email(s):\n\n"
                for i, msg in enumerate(messages[:5], 1):
                    response += f"{i}. From: {msg.get('from', 'Unknown')}\n"
                    response += f"   Subject: {msg.get('subject', 'No subject')}\n"
                    response += f"   Date: {msg.get('date', 'Unknown')}\n\n"

                return response
            else:
                return f"Failed to list emails: {result.get('message', 'Unknown error')}"

        elif function_name == "read_email":
            if result.get("status") == 200:
                data = result.get("data", {})
                return f"From: {data.get('from', 'Unknown')}\nSubject: {data.get('subject', 'No subject')}\n\n{data.get('body', 'No content')}"
            else:
                return f"Failed to read email: {result.get('message', 'Unknown error')}"

        elif function_name == "get_auth_status":
            if result.get("authenticated"):
                return "✓ You are authenticated with Gmail."
            else:
                return "You are not authenticated with Gmail."

        return "Request completed, but I couldn't generate a detailed response."

    def reset_conversation(self):
        """
        Reset the conversation history.

        Use this to start a fresh conversation.
        """
        self.chat_session = self.model.start_chat(history=[])
        print("Conversation history reset")


try:
    llm_client = GeminiLLMClient()
except Exception as e:
    print(f"LLM client not initialized: {e}")
    llm_client = None