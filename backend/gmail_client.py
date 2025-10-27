import json
import subprocess
from typing import Optional
from typing import Dict, Any
from google_auth_oauthlib.flow import Flow

oauth_flow: Optional[Flow] = None

mcp_process: Optional[subprocess.Popen] = None

class GmailClient:

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0
        self.initialized = False

    def start(self):
        if self.process:
            return

        import sys
        import os

        # Get the current working directory
        cwd = os.path.dirname(os.path.abspath(__file__))

        print(f"Starting MCP server from: {cwd}")

        self.process = subprocess.Popen(
            [sys.executable, '-m', 'gmail_mcp.gmail_server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,  # Use binary mode
            bufsize=0,   # Unbuffered
            cwd=cwd
        )

        # Check if process started successfully
        import time
        time.sleep(0.5)  # Give it a moment to start

        if self.process.poll() is not None:
            # Process has already terminated
            stderr = self.process.stderr.read().decode('utf-8')
            raise Exception(f"MCP server failed to start. Error: {stderr}")

        # Initialize the MCP connection
        self._initialize()

    def _initialize(self):
        """Initialize the MCP connection"""
        if self.initialized:
            return

        self.request_id += 1

        init_request = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': 'initialize',
            'params': {
                'protocolVersion': '2024-11-05',
                'capabilities': {},
                'clientInfo': {
                    'name': 'gmail-mcp-client',
                    'version': '1.0.0'
                }
            }
        }

        request_str = json.dumps(init_request) + '\n'
        print(f"Initializing MCP: {request_str.strip()}")

        self.process.stdin.write(request_str.encode('utf-8'))
        self.process.stdin.flush()

        response_line = self.process.stdout.readline().decode('utf-8')
        print(f"Initialize response: {response_line.strip()}")

        response = json.loads(response_line)

        if 'error' in response:
            raise Exception(f"Failed to initialize MCP: {response['error']['message']}")

        # Send initialized notification
        self.request_id += 1
        initialized_notification = {
            'jsonrpc': '2.0',
            'method': 'notifications/initialized'
        }

        notif_str = json.dumps(initialized_notification) + '\n'
        print(f"Sending initialized notification: {notif_str.strip()}")

        self.process.stdin.write(notif_str.encode('utf-8'))
        self.process.stdin.flush()

        self.initialized = True
        print("MCP connection initialized successfully")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict:
        if not self.process:
            self.start()

        # Check if process is still running
        if self.process.poll() is not None:
            stderr = self.process.stderr.read().decode('utf-8')
            raise Exception(f"MCP server has terminated. Error: {stderr}")

        self.request_id += 1

        request = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': 'tools/call',
            'params': {
                'name': tool_name,
                'arguments': arguments
            }
        }

        try:
            request_str = json.dumps(request) + '\n'
            print(f"Sending request: {request_str.strip()}")

            self.process.stdin.write(request_str.encode('utf-8'))
            self.process.stdin.flush()

            response_line = self.process.stdout.readline().decode('utf-8')
            print(f"Received response: {response_line.strip()}")

            response = json.loads(response_line)

            if 'error' in response:
                raise Exception(response['error']['message'])

            result = response['result']['content'][0]['text']

            return result
        except Exception as e:
            # Try to read stderr for more context
            import select
            if hasattr(select, 'select'):
                # Unix-like systems
                pass
            else:
                # Windows - just try to read what's available
                pass
            print(f"Error in call_tool: {e}")
            raise
    
gmail_client = GmailClient()