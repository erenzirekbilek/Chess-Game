# ♟️ Chess Game — Full Stack Project Documentation

> A real-time, full-featured chess application built with Django + Django Channels (WebSocket), React.js, and Tailwind CSS. Play against an AI engine or challenge other players online — all with free, open-source tools.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Feature List](#feature-list)
5. [Backend Structure (Django)](#backend-structure-django)
6. [Frontend Structure (React)](#frontend-structure-react)
7. [WebSocket Flow (Django Channels)](#websocket-flow-django-channels)
8. [AI Engine Integration](#ai-engine-integration)
9. [Online Matchmaking Flow](#online-matchmaking-flow)
10. [Database Design](#database-design)
11. [Free Tools & Libraries](#free-tools--libraries)
12. [Development Roadmap](#development-roadmap)
13. [Deployment Notes](#deployment-notes)

---

## Project Overview

This is a full-stack chess platform where:

- A player can start a **single-player game** against a computer AI (Stockfish engine).
- A player can play **online multiplayer** against another human in real time via WebSockets.
- The board is rendered in a beautiful, interactive React UI styled with Tailwind CSS.
- All game state, move history, and user sessions are managed by the Django backend.
- Real-time communication is handled by Django Channels and Redis as the channel layer.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend Framework | Django 4.x | REST API, authentication, game logic |
| WebSocket Server | Django Channels 4.x | Real-time bidirectional communication |
| Channel Layer | Redis (via channels-redis) | Message broker between consumers |
| Chess Logic (server) | python-chess | Move validation, FEN/PGN parsing, game state |
| AI Engine | Stockfish (via python-chess) | Computer opponent |
| Frontend Framework | React 18 | UI rendering, component state |
| Styling | Tailwind CSS | Utility-first, responsive styling |
| Chess UI Component | react-chessboard | Interactive board rendering |
| Chess Logic (client) | chess.js | Client-side move validation |
| HTTP Client | Axios | API calls from React to Django |
| WebSocket Client | Native Browser WebSocket API | Real-time game communication |
| Database | PostgreSQL (or SQLite for dev) | Persistent data storage |
| Auth | Django REST Framework + SimpleJWT | Token-based authentication |

---

## Architecture

The system is divided into three main layers:

```
┌─────────────────────────────────────┐
│           React Frontend            │
│  (Board UI, Lobby, Chat, History)   │
│     Tailwind CSS for styling        │
└────────────┬────────────────────────┘
             │  HTTP (REST) + WebSocket (ws://)
             │
┌────────────▼────────────────────────┐
│         Django Backend              │
│                                     │
│  ┌──────────────┐  ┌─────────────┐  │
│  │  REST API    │  │  Channels   │  │
│  │  (DRF)       │  │  Consumers  │  │
│  └──────────────┘  └──────┬──────┘  │
│                           │         │
│  ┌────────────────────────▼──────┐  │
│  │     Redis Channel Layer       │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  python-chess + Stockfish    │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  PostgreSQL / SQLite DB      │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## Feature List

### Core Gameplay
- Interactive drag-and-drop chess board
- Full chess rule enforcement (castling, en passant, promotion, check, checkmate, stalemate)
- Legal move highlighting when a piece is selected
- Move history panel (SAN notation)
- Board flip / rotate option
- Captured pieces display

### Player vs Computer
- Difficulty selector (easy / medium / hard) mapped to Stockfish depth levels
- AI move with a visual "thinking" animation/delay
- Option to undo the last move pair (player + AI)

### Online Multiplayer
- Lobby system: create a game or join a random queue (matchmaking)
- Private game rooms with shareable links
- Real-time move sync over WebSocket
- Player disconnect handling (timeout or forfeit)
- Rematch request system

### User System
- Registration and login (JWT-based)
- Guest play (anonymous session, no history saved)
- User profile with win/loss/draw stats
- Game history with replay ability

### UI/UX
- Responsive design (desktop + mobile)
- Light / Dark theme toggle
- In-game clock (optional countdown timer)
- Real-time move broadcast animation

---

## Backend Structure (Django)

```
backend/
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py          # Main settings, Channels config, Redis
│   ├── asgi.py              # ASGI entrypoint for Channels
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── models.py            # Custom User model, UserProfile
│   ├── views.py             # Register, login, profile endpoints
│   ├── serializers.py
│   └── urls.py
├── games/
│   ├── models.py            # Game, Move models
│   ├── views.py             # Create game, list games, game detail
│   ├── serializers.py
│   ├── consumers.py         # WebSocket consumer (game room logic)
│   ├── routing.py           # WebSocket URL routing
│   ├── engine.py            # Stockfish integration via python-chess
│   ├── utils.py             # FEN helpers, move validation wrappers
│   └── urls.py
└── lobby/
    ├── models.py            # Matchmaking queue model
    ├── consumers.py         # Lobby WebSocket consumer
    └── routing.py
```

### Key Django Apps

**`users` app** — handles authentication, JWT token issuance, and player profiles including ELO rating and game statistics.

**`games` app** — the heart of the project. Contains the Game model that stores FEN state and game metadata, the Move model for full move history, and the two most important files: `consumers.py` (WebSocket logic) and `engine.py` (AI interface).

**`lobby` app** — manages matchmaking. Players enter the queue via WebSocket; the lobby consumer pairs two players and creates a Game object, then redirects both to the game room consumer.

---

## Frontend Structure (React)

```
frontend/
├── public/
├── src/
│   ├── main.jsx
│   ├── App.jsx              # Router setup
│   ├── index.css            # Tailwind directives
│   ├── api/
│   │   ├── axios.js         # Axios instance with JWT interceptors
│   │   ├── auth.js          # Login, register API calls
│   │   └── games.js         # Fetch game history, create game
│   ├── hooks/
│   │   ├── useWebSocket.js  # Custom hook for WS connection lifecycle
│   │   ├── useChessGame.js  # Game state, move logic, chess.js wrapper
│   │   └── useAuth.js       # Auth context hook
│   ├── components/
│   │   ├── Board/
│   │   │   ├── ChessBoard.jsx     # react-chessboard wrapper
│   │   │   ├── MoveHistory.jsx    # SAN move list
│   │   │   └── CapturedPieces.jsx
│   │   ├── Game/
│   │   │   ├── GameControls.jsx   # Resign, draw, undo, flip
│   │   │   ├── PlayerInfo.jsx     # Name, avatar, clock
│   │   │   └── GameOverModal.jsx  # Result screen + rematch
│   │   ├── Lobby/
│   │   │   ├── LobbyPage.jsx      # Create/join game options
│   │   │   └── MatchmakingSpinner.jsx
│   │   └── UI/
│   │       ├── Navbar.jsx
│   │       ├── ThemeToggle.jsx
│   │       └── LoadingSpinner.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── GamePage.jsx     # Main game page (vs AI or online)
│   │   ├── ProfilePage.jsx
│   │   └── HistoryPage.jsx
│   └── context/
│       ├── AuthContext.jsx
│       └── ThemeContext.jsx
├── tailwind.config.js
├── vite.config.js
└── package.json
```

---

## WebSocket Flow (Django Channels)

### Connection Lifecycle

1. The React client connects to a WebSocket URL like `ws://localhost:8000/ws/game/<game_id>/`.
2. Django Channels routes this to the `GameConsumer` class.
3. On connect, the consumer verifies the JWT token passed in the query string, then adds the socket to a Channel Group named after the game ID.
4. Both players are now in the same group and all messages sent to the group reach both clients.

### Message Types (JSON protocol)

| Type | Direction | Description |
|---|---|---|
| `move` | Client → Server | Player submits a move (e.g., `e2e4`) |
| `move_broadcast` | Server → Clients | Valid move echoed to both players |
| `game_over` | Server → Clients | Checkmate/stalemate/draw detected |
| `error` | Server → Client | Illegal move or rule violation |
| `resign` | Client → Server | Player resigns |
| `draw_offer` | Client → Server | Player offers a draw |
| `draw_response` | Client → Server | Accept or decline draw |
| `rematch_request` | Client → Server | Request rematch |
| `rematch_response` | Client → Server | Accept or decline |
| `ping` | Client → Server | Keep-alive |

### Move Processing (Server Side)

When a `move` message arrives at the consumer, the flow is:

1. Load the current game from the database (fetching the FEN string).
2. Use `python-chess` to verify the move is legal on the current board.
3. Push the move, update the FEN, and save the new state to the database.
4. Broadcast a `move_broadcast` message with the updated FEN to all players in the group.
5. Check for game-ending conditions (checkmate, stalemate, insufficient material, 50-move rule) and send a `game_over` message if needed.

---

## AI Engine Integration

The AI opponent uses **Stockfish**, the world's strongest open-source chess engine.

### How It Works

- Stockfish is installed as a binary on the server (free to download).
- The `python-chess` library provides a clean Python interface (`chess.engine.SimpleEngine`) to communicate with Stockfish via UCI protocol.
- When it's the AI's turn, the backend calls `engine.play(board, chess.engine.Limit(depth=N))` where `N` maps to the selected difficulty.
- The AI move is then processed exactly like a human move and broadcast to the client.

### Difficulty Mapping

| UI Label | Stockfish Depth | Approximate ELO |
|---|---|---|
| Easy | 2 | ~600 |
| Medium | 8 | ~1500 |
| Hard | 18 | ~2800+ |

### Important Consideration

For "vs computer" games, there is no need for a second WebSocket player. The Django view creates a single-player game room, and after the human's move is received via WebSocket, the server computes the Stockfish response synchronously in the consumer (or asynchronously in a Celery task for better performance) and immediately broadcasts it back.

---

## Online Matchmaking Flow

1. Logged-in player opens the Lobby page and clicks **"Play Online"**.
2. The frontend connects to `ws://localhost:8000/ws/lobby/`.
3. The `LobbyConsumer` checks the queue. If empty, it adds the player to a waiting list. If another player is already waiting, it pairs them.
4. The consumer creates a new `Game` object in the database and assigns both players their colors (White/Black randomly).
5. Both clients receive a `game_ready` message containing the `game_id`.
6. The frontend disconnects from the lobby WebSocket and navigates to `/game/<game_id>`, connecting to the game room WebSocket.
7. The game begins.

---

## Database Design

### `User` (extends Django AbstractUser)
- `username`, `email`, `password`
- `elo_rating` (integer, default 1200)
- `games_played`, `wins`, `losses`, `draws`

### `Game`
- `id` (UUID)
- `white_player` (FK to User, nullable for guest)
- `black_player` (FK to User, nullable for AI)
- `game_type` (choices: `vs_ai`, `vs_human`)
- `status` (choices: `waiting`, `active`, `completed`, `abandoned`)
- `result` (choices: `white_wins`, `black_wins`, `draw`, `in_progress`)
- `fen` (current board state as FEN string)
- `pgn` (full game PGN for replay)
- `created_at`, `updated_at`
- `ai_difficulty` (nullable, integer for Stockfish depth)

### `Move`
- `id`
- `game` (FK to Game)
- `player` (FK to User)
- `move_number` (integer)
- `san` (Standard Algebraic Notation, e.g. "Nf3")
- `uci` (UCI format, e.g. "g1f3")
- `fen_after` (board state after move)
- `timestamp`

---

## Free Tools & Libraries

Every tool and library in this project is **completely free and open-source**:

| Tool | License | Purpose |
|---|---|---|
| Django | BSD | Backend web framework |
| Django Channels | BSD | WebSocket / async support |
| Django REST Framework | BSD | REST API |
| djangorestframework-simplejwt | MIT | JWT authentication |
| python-chess | GPL-3 | Chess logic + engine bridge |
| Stockfish | GPL-3 | AI chess engine (binary) |
| channels-redis | BSD | Redis channel layer backend |
| Redis | BSD | Message broker |
| React | MIT | Frontend UI library |
| Tailwind CSS | MIT | Utility CSS framework |
| react-chessboard | MIT | Chess board React component |
| chess.js | BSD | Client-side chess rules |
| Axios | MIT | HTTP client |
| Vite | MIT | Frontend build tool |
| PostgreSQL | PostgreSQL License | Database (or SQLite for dev) |

---

## Development Roadmap

### Phase 1 — Foundation
- Project setup: Django + Channels + Redis, React + Vite + Tailwind
- User registration and JWT login
- Basic board rendering with react-chessboard
- REST API for game creation

### Phase 2 — Single Player (vs AI)
- Stockfish integration with `python-chess`
- WebSocket consumer for AI game flow
- Difficulty selector UI
- Move history panel

### Phase 3 — Online Multiplayer
- Lobby WebSocket consumer and matchmaking queue
- Game room WebSocket consumer
- Private game room with share link
- Disconnect / forfeit handling

### Phase 4 — Polish & Features
- Clocks / timers (Blitz, Rapid, Classical)
- User profile and game history
- Game replay viewer
- Rematch and draw offer system
- Dark/light theme toggle
- Mobile responsive layout

### Phase 5 — Optional Enhancements
- Spectator mode
- ELO rating system
- Chat within game
- Opening name detection (via ECO codes in python-chess)
- Analysis board powered by Stockfish

---

## Deployment Notes

For production, the key differences from local development are:

- **ASGI server**: Use `Daphne` or `Uvicorn` instead of `runserver` to properly serve WebSocket connections alongside HTTP.
- **Redis**: A managed Redis instance (e.g., Redis Cloud free tier, or Railway) is required for the channel layer.
- **Stockfish binary**: Must be installed on the server. On Linux this is a simple `apt install stockfish`.
- **Database**: Switch from SQLite to PostgreSQL for production.
- **Static files**: Serve React build output via Nginx or a CDN. Django serves only the API and WebSocket endpoints.
- **Environment variables**: Store `SECRET_KEY`, `DATABASE_URL`, `REDIS_URL` in a `.env` file — never commit them.

A typical production stack would be: **Nginx → Daphne (Django/Channels) + React static files**, with Redis and PostgreSQL running as separate services.

---

*This document covers the full architecture and design plan. No implementation code is included — this is a planning and reference guide for the development team.*
