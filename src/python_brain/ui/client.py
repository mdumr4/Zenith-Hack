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
    def send_chat_request(self, message: str, context: str = ""):
        """
        Sends a POST /chat request to the backend.
        Returns the response string.
        """
        try:
            # We create a FRESH connection for chat to avoid conflicting with the polling loop
            # Or we can reuse if thread-safe? http.client is NOT thread safe if shared.
            # Client.py is used by main thread (poll) and worker thread (chat).
            # We should probably instantiate a new client or new connection for chat.

            # Simple approach: Create a new short-lived connection for this request
            conn = http.client.HTTPConnection(self.host, self.port, timeout=5.0) # Longer timeout for LLM
            headers = {"Content-type": "application/json"}
            payload = json.dumps({"message": message, "context": context})

            conn.request("POST", "/chat", payload, headers)
            response = conn.getresponse()

            if response.status == 200:
                data = response.read().decode("utf-8")
                result = json.loads(data)
                conn.close()
                return result.get("response", "")
            else:
                response.read()
                conn.close()
                return f"Error: Server returned {response.status}"

        except Exception as e:
            return f"Error: Could not connect to backend ({e})"
