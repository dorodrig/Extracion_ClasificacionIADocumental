type WSMessageCallback = (data: any) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000;
  private onMessageCallback: WSMessageCallback | null = null;
  private heartbeatInterval: NodeJS.Timeout | null = null;

  constructor(url: string) {
    this.url = url;
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.CONNECTING || this.ws.readyState === WebSocket.OPEN)) {
      return;
    }

    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('[WebSocket] Connected to', this.url);
      this.reconnectAttempts = 0;
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      if (event.data === 'pong') {
        return;
      }
      try {
        const data = JSON.parse(event.data);
        if (this.onMessageCallback) {
          this.onMessageCallback(data);
        }
      } catch (err) {
        console.error('[WebSocket] Failed to parse message', err);
      }
    };

    this.ws.onclose = () => {
      console.warn('[WebSocket] Connection closed');
      this.stopHeartbeat();
      this.reconnect();
    };

    this.ws.onerror = (error) => {
      console.error('[WebSocket] Error', error);
      this.ws?.close();
    };
  }

  private startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
      }
    }, 30000);
  }

  private stopHeartbeat() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  private reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`[WebSocket] Reconnecting in ${this.reconnectDelay}ms (Attempt ${this.reconnectAttempts})`);
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay);
    } else {
      console.error('[WebSocket] Max reconnect attempts reached');
    }
  }

  disconnect() {
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  onMessage(callback: WSMessageCallback) {
    this.onMessageCallback = callback;
  }
}

export const wsService = new WebSocketService('ws://localhost:8000/api/v1/pendientes/ws');
