import socket


class LuaExecutionError(Exception):
    """Raised when Lua code execution fails in DCS."""
    pass


class DCSConnection:
    """Handles UDP connection to DCS World for executing Lua code."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8042, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: socket.socket | None = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.timeout)
    
    def execute(self, lua_code: str) -> str:
        """
        Execute Lua code in DCS.
        
        Returns:
            The result string from successful Lua execution
            
        Raises:
            LuaExecutionError: If Lua execution fails
            socket.timeout: If DCS doesn't respond within timeout
            KeyboardInterrupt: If execution is interrupted
            Exception: For other connection errors
        """
        if self.socket is None:
            raise ConnectionError("Socket has disconnected.")
        
        self.socket.sendto(lua_code.encode(), (self.host, self.port))
        response = self.socket.recv(64 * 1024).decode()
        
        # Parse structured response using match statement
        match response:
            case s if s.startswith("OK|"):
                return s[3:]  # Remove "OK|" prefix
            case s if s.startswith("ERROR|"):
                raise LuaExecutionError(s[6:])  # Remove "ERROR|" prefix
            case _:
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
