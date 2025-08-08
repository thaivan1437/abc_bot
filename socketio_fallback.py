"""
Fallback solution cho Socket.IO khi không cài được
Import file này trước khi import socketio để tránh crash
"""

import warnings
import sys
import types

class MockSocketIO:
    """Mock SocketIO client để app không crash"""
    
    def __init__(self, *args, **kwargs):
        warnings.warn("SocketIO not available, using mock client. Some features may not work.", UserWarning)
        self.connected = False
    
    def connect(self, url, *args, **kwargs):
        print(f"Mock SocketIO: Attempted to connect to {url}")
        print("⚠️ SocketIO not available - connection disabled")
        return False
    
    def disconnect(self, *args, **kwargs):
        print("Mock SocketIO: disconnect called")
        self.connected = False
    
    def emit(self, event, data=None, *args, **kwargs):
        print(f"Mock SocketIO: emit event '{event}' with data: {data}")
        print("⚠️ SocketIO not available - event not sent")
    
    def on(self, event, handler=None):
        print(f"Mock SocketIO: registered handler for event '{event}'")
        print("⚠️ SocketIO not available - handler not active")
        
        def decorator(func):
            return func
        
        if handler is None:
            return decorator
        else:
            return decorator(handler)
    
    def off(self, event, handler=None):
        print(f"Mock SocketIO: removed handler for event '{event}'")
    
    def wait(self, *args, **kwargs):
        print("Mock SocketIO: wait called")
        return None
    
    def sleep(self, seconds):
        import time
        time.sleep(seconds)

class MockEngineIO:
    """Mock EngineIO client"""
    
    def __init__(self, *args, **kwargs):
        warnings.warn("EngineIO not available, using mock client", UserWarning)

def setup_mock_socketio():
    """Setup mock socketio modules"""
    
    # Tạo mock socketio module
    mock_socketio = types.ModuleType('socketio')
    mock_socketio.Client = MockSocketIO
    mock_socketio.SimpleClient = MockSocketIO
    mock_socketio.AsyncClient = MockSocketIO
    mock_socketio.__version__ = "5.0.0-mock"
    
    # Tạo mock engineio module  
    mock_engineio = types.ModuleType('engineio')
    mock_engineio.Client = MockEngineIO
    mock_engineio.AsyncClient = MockEngineIO
    mock_engineio.__version__ = "4.0.0-mock"
    
    # Add to sys.modules
    sys.modules['socketio'] = mock_socketio
    sys.modules['engineio'] = mock_engineio
    
    print("⚠️ Using mock socketio/engineio modules")
    print("💡 Some real-time features will be disabled")

# Auto setup nếu socketio không có
try:
    import socketio
    import engineio
    print("✅ Real socketio/engineio modules available")
except ImportError as e:
    print(f"❌ SocketIO/EngineIO import failed: {str(e)}")
    setup_mock_socketio()
    print("✅ Mock modules setup complete")

# Export để có thể import
__all__ = ['MockSocketIO', 'MockEngineIO', 'setup_mock_socketio']