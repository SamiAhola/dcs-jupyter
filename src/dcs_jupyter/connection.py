import socket


class DCSConnection:
    """Handles UDP connection to DCS World for executing Lua code."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 8042, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: socket.socket | None = None
    
    def connect(self) -> None:
        """Initialize UDP socket connection."""
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(self.timeout)
    
    def execute(self, lua_code: str) -> str:
        """
        Execute Lua code in DCS.
        
        Returns:
            Result string from DCS
            
        Raises:
            socket.timeout: If DCS doesn't respond within timeout
            KeyboardInterrupt: If execution is interrupted
            Exception: For other connection errors
        """
        if self.socket is None:
            raise ConnectionError("Socket not connected. Call connect() first.")
        
        self.socket.sendto(lua_code.encode(), (self.host, self.port))
        return self.socket.recv(64 * 1024).decode()
    
    def disconnect(self) -> None:
        """Close the UDP connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
