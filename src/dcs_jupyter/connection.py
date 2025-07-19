import socket
from typing import Tuple


class DCSConnection:
    """Handles UDP connection to DCS World for executing Lua code."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8042, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: socket.socket | None = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)
    
    def execute(self, lua_code: str) -> Tuple[bool, str]:
        """
        Execute Lua code in DCS.
        
        Returns:
            Tuple of (success: bool, result: str)
            - success: True if Lua execution succeeded, False if error
            - result: The actual result or error message
            
        Raises:
            socket.timeout: If DCS doesn't respond within timeout
            KeyboardInterrupt: If execution is interrupted
            Exception: For other connection errors
        """
        if self.socket is None:
            raise ConnectionError("Socket has disconnected.")
        
        self.socket.sendto(lua_code.encode(), (self.host, self.port))
        response = self.socket.recv(64 * 1024).decode()
        
        # Parse structured response: "STATUS|RESULT"
        if response.startswith("OK|"):
            return True, response[3:]  # Remove "OK|" prefix
        elif response.startswith("ERROR|"):
            return False, response[6:]  # Remove "ERROR|" prefix
        else:
            # Raise error if response doesn't have expected status prefix
            raise ValueError(f"Invalid response format from DCS: {response[:50]}...")
    
    def disconnect(self) -> None:
        """Close the UDP connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
