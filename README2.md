# Chess Game - Development Setup

## Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Playing vs AI

1. Start the backend server
2. Start the frontend 
3. Select difficulty and play

## Project Structure

- `backend/chess_engine/` - AI algorithms
- `games/` - Django game app
- `users/` - Django user app
- `frontend/src/` - React components