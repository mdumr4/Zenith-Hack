# client.py
import http.client
import json

class UIClient:
    def __init__(self, host="127.0.0.1", port=18492):
        self.host = host
        self.port = port
        self.connection = None

    def _get_connection(self):
        if self.connection is None:
            self.connection = http.client.HTTPConnection(self.host, self.port, timeout=0.05) # Very short timeout for polling
        return self.connection

    def poll_state(self):
        """
        Polls GET /ui/state from the backend.
        Returns a dictionary adhering to the schema or None if failed.
        """
        try:
            conn = self._get_connection()
            conn.request("GET", "/ui/state")
            response = conn.getresponse()
            
            if response.status == 200:
                data = response.read().decode("utf-8")
                # Strict Schema Validation could go here, but for now we trust JSON parsing
                return json.loads(data)
            else:
                # Consume response to keep connection clean
                response.read()
                return None
        except Exception:
            # Connection failed (Server likely not up or busy)
            # Reset connection
            if self.connection:
                self.connection.close()
            self.connection = None
            return None
