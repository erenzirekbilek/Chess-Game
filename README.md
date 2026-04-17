# ♟️ Chess Game - Full Stack Application

A real-time chess application built with Django + Django Channels (WebSocket), React.js, and Tailwind CSS. Play against an AI computer opponent or challenge other players online.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Getting Started](#getting-started)
4. [WebSocket Architecture](#websocket-architecture) ⭐
5. [Project Structure](#project-structure)
6. [API Endpoints](#api-endpoints)
7. [Chess AI Algorithms](#chess-ai-algorithms)
8. [Game Rules](#game-rules)

---

## Features

- **Play vs AI** - Challenge computer with multiple difficulty levels
- **Online Multiplayer** - Real-time chess against other players (coming soon)
- **Game History** - Review your past games
- **Player Profiles** - Track wins, losses, and ELO rating
- **Responsive Design** - Works on desktop and mobile

---

## Tech Stack

| Layer | Technology |
|-------|----------|
| Backend | Django 5.x |
| WebSocket | Django Channels 4.x |
| Frontend | React 18 + Vite |
| Styling | Tailwind CSS |
| Chess Board | react-chessboard |
| Chess Logic | python-chess / chess.js |
| Auth | JWT (SimpleJWT) |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis (optional for production)

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## WebSocket Architecture ⭐

This section explains how WebSockets work in our chess application.

### What is WebSocket?

HTTP is request-response based - the client always initiates communication. For real-time games like chess, we need bidirectional communication where both client and server can send messages anytime.

**WebSocket** is a protocol that maintains a persistent connection between client and server. Once connected, either side can send messages instantly without the overhead of HTTP headers.

### Our WebSocket Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    WebSocket Connection Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Client (React)                              Server (Django)     │
│       │                                          │               │
│       │  1. Connect to WS URL                    │               │
│       │  ───────────────────────────────────►    │               │
│       │                                          │               │
│       │                              Accept Connection           │
│       │  ◄───────────────────────────────────    │               │
│       │                                          │               │
│       │  2. Send move (JSON)                     │               │
│       │  ───────────���───────────────────────►    │               │
│       │                                          │               │
│       │  3. Process & validate move               │               │
│       │  ◄──► (Server only) ◄──►               │               │
│       │                                          │               │
│       │  4. Broadcast to opponent (JSON)        │               │
│       │  ◄───────────────────────────────────    │               │
│       │                                          │               │
│       │  5. Continue game...                   │               │
│       │  ◄───────►◄───────►◄───────►          │               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### WebSocket URL Pattern

```
ws://localhost:8000/ws/game/<game_id>/
ws://localhost:8000/ws/lobby/
```

### Message Protocol (JSON)

All messages are JSON with a `type` field:

```javascript
// Client → Server: Make a move
{
  "type": "move",
  "uci": "e2e4"  // UCI format: from-to
}

// Server → Client: Move broadcast
{
  "type": "move",
  "uci": "e2e4",
  "san": "e4",
  "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
  "turn": "black",
  "is_check": false,
  "is_checkmate": false,
  "is_stalemate": false
}

// Client → Server: Resign
{
  "type": "resign"
}

// Server → Client: Game over
{
  "type": "game_over",
  "result": "white_wins"
}
```

### Django Channels Implementation

#### 1. Install Channels

```bash
pip install channels
```

#### 2. Configure ASGI (backend/asgi.py)

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Add your WebSocket URLs here
        ])
    ),
})
```

#### 3. Create Consumer (games/consumers.py)

```python
import json
import chess
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group = f"game_{self.game_id}"

        # Join game group
        await self.channel_layer.group_add(self.game_group, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "move":
            await self.handle_move(data)
        elif message_type == "resign":
            await self.handle_resign(data)

    async def handle_move(self, data):
        uci = data.get("uci")
        # ... validate and process move ...

        # Broadcast to both players
        await self.channel_layer.group_send(
            self.game_group,
            {
                "type": "move_broadcast",
                "uci": uci,
                "fen": new_fen,
                # ... more data ...
            }
        )

    async def move_broadcast(self, event):
        # Send to WebSocket client
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_group, self.channel_name)
```

#### 4. Frontend WebSocket Hook (frontend/src/hooks/useWebSocket.js)

```javascript
import { useEffect, useRef, useState } from "react";

export function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setIsConnected(true);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data);
    };
    ws.onclose = () => setIsConnected(false);

    wsRef.current = ws;

    return () => ws.close();
  }, [url]);

  const send = (data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  };

  return { isConnected, lastMessage, send };
}

// Usage in a component:
function GamePage() {
  const wsUrl = `ws://localhost:8000/ws/game/${gameId}/`;
  const { isConnected, lastMessage, send } = useWebSocket(wsUrl);

  const handlePieceDrop = (source, target) => {
    send({ type: "move", uci: source + target });
  };

  useEffect(() => {
    if (lastMessage?.type === "move") {
      // Update board with new position
      setBoard(lastMessage.fen);
    }
  }, [lastMessage]);

  return <div>Connected: {isConnected ? "Yes" : "No"}</div>;
}
```

### Channel Layers

For development, we use `InMemoryChannelLayer`. For production with multiple servers, use Redis:

```python
# settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # For production:
        # "BACKEND": "channels_redis.RedisChannelLayer",
        # "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}
```

---

## Project Structure

```
chess-game/
├── backend/                  # Django backend
│   ├── chess_engine/       # AI algorithms
│   │   ├── minimax.py
│   │   ├── alphabeta.py
│   │   ├── mcts.py
│   │   ├── quiescence.py
│   │   ├── evaluation.py
│   │   ├── opening_book.py
│   │   ├── tablebases.py
│   │   └── engine.py
│   ├── settings.py
│   └── asgi.py            # WebSocket config
├── games/                  # Django app
│   ├── models.py
│   ├── views.py           # REST API
│   ├── consumers.py      # WebSocket consumers
│   └── urls.py
├── users/                  # Authentication
├── frontend/               # React app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/       # useWebSocket, useChessGame
│   │   └── api/        # axios client
│   └── tailwind.config.js
└── requirements.txt
```

---

## API Endpoints

### Games API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/games/` | Create new game |
| GET | `/api/games/{id}/` | Get game state |
| POST | `/api/games/{id}/make_move/` | Make a move |
| POST | `/api/games/{id}/resign/` | Resign game |
| GET | `/api/games/my_games/` | User's game history |

### Auth API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/login/` | Login (returns JWT) |
| GET | `/api/auth/me/` | Current user |

---

## Chess AI Algorithms

Our AI implements several search algorithms:

### 1. Minimax
Recursive search that maximizes for one side and minimizes for opponent.

```python
def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        max_eval = -∞
        for move in board.legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = ∞
        # ... similar but minimize
        return min_eval
```

### 2. Alpha-Beta Pruning
Optimizes Minimax by pruning branches that can't improve the result.

```python
def alpha_beta(board, depth, alpha, beta, maximizing):
    if depth == 0:
        return evaluate(board)

    if maximizing:
        for move in board.legal_moves:
            board.push(move)
            score = alpha_beta(board, depth-1, alpha, beta, False)
            board.pop()
            if score > alpha:
                alpha = score
            if beta <= alpha:  # Prune!
                break
        return alpha
    # ... similar for minimizing
```

### 3. Monte Carlo Tree Search (MCTS)
Random simulations to find the best move statistically.

### 4. Quiescence Search
Extends search to avoid "quiet" positions where captures are available.

### Evaluation Functions

- **Material**: Piece values (P=100, N=320, B=330, R=500, Q=900)
- **Position**: Piece-square tables
- **NNUE**: Neural network evaluation
- **Opening Book**: Pre-computed opening moves
- **Endgame Tablebases**: Perfect play in common endgames

---

## Game Rules

Standard chess rules are enforced:
- Legal move validation
- Check/checkmate/stalemate detection
- Castling (kingside/queenside)
- En passant
- Pawn promotion (to Queen automatically)

---

## License

MIT License - Feel free to use this for learning or your own projects!

---

## Credits

- [python-chess](https://python-chess.readthedocs.io/) - Chess logic in Python
- [react-chessboard](https://github.com/hippware/react-chessboard) - React chess board
- [Stockfish](https://stockfishchess.org/) - World's strongest chess engine (optional integration)