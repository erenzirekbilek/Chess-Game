import json
import chess
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Game, Move, GameStatus, GameResult


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group = f"game_{self.game_id}"

        await self.channel_layer.group_add(self.game_group, self.channel_name)
        await self.accept()

        game = await self.get_game(self.game_id)
        if game:
            await self.send_game_state(game)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "move":
            await self.handle_move(data)
        elif message_type == "resign":
            await self.handle_resign(data)
        elif message_type == "draw_offer":
            await self.handle_draw_offer(data)
        elif message_type == "rematch":
            await self.handle_rematch(data)

    async def handle_move(self, data):
        uci = data.get("uci")
        if not uci:
            await self.send_error("No move provided")
            return

        game = await self.get_game(self.game_id)
        if not game or game.status == GameStatus.COMPLETED:
            await self.send_error("Game not found or completed")
            return

        try:
            board = chess.Board(game.fen)
            move = chess.Move.from_uci(uci)

            if move not in board.legal_moves:
                await self.send_error("Illegal move")
                return

            san = board.san(move)
            board.push(move)
            new_fen = board.fen()

            game.fen = new_fen
            game.current_turn = "white" if board.turn == chess.WHITE else "black"
            game.move_count += 1

            await self.save_move(game, game.move_count, san, uci, new_fen)

            is_check = board.is_check()
            is_checkmate = board.is_checkmate()
            is_stalemate = board.is_stalemate()

            await self.update_game(game, new_fen, game.current_turn, game.move_count)

            await self.channel_layer.group_send(
                self.game_group,
                {
                    "type": "move_broadcast",
                    "uci": uci,
                    "san": san,
                    "fen": new_fen,
                    "turn": game.current_turn,
                    "is_check": is_check,
                    "is_checkmate": is_checkmate,
                    "is_stalemate": is_stalemate,
                },
            )

            if is_checkmate or is_stalemate:
                game.status = GameStatus.COMPLETED
                if is_checkmate:
                    game.result = (
                        GameResult.WHITE_WINS
                        if board.turn == chess.BLACK
                        else GameResult.BLACK_WINS
                    )
                else:
                    game.result = GameResult.DRAW
                await self.update_game_status(game, game.status, game.result)

        except Exception as e:
            await self.send_error(str(e))

    async def handle_resign(self, data):
        game = await self.get_game(self.game_id)
        if game:
            game.status = GameStatus.COMPLETED
            game.result = GameResult.BLACK_WINS
            await self.update_game_status(game, game.status, game.result)

            await self.channel_layer.group_send(
                self.game_group, {"type": "game_over", "result": game.result}
            )

    async def handle_draw_offer(self, data):
        await self.channel_layer.group_send(
            self.game_group, {"type": "draw_offer", "from": data.get("from")}
        )

    async def handle_rematch(self, data):
        await self.channel_layer.group_send(
            self.game_group, {"type": "rematch_request", "from": data.get("from")}
        )

    async def move_broadcast(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "move",
                    "uci": event.get("uci"),
                    "san": event.get("san"),
                    "fen": event.get("fen"),
                    "turn": event.get("turn"),
                    "is_check": event.get("is_check"),
                    "is_checkmate": event.get("is_checkmate"),
                    "is_stalemate": event.get("is_stalemate"),
                }
            )
        )

    async def game_over(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "game_over",
                    "result": event.get("result"),
                }
            )
        )

    async def send_game_state(self, game):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "game_state",
                    "fen": game.fen,
                    "turn": game.current_turn,
                    "move_count": game.move_count,
                    "status": game.status,
                    "result": game.result,
                }
            )
        )

    async def send_error(self, message):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "error",
                    "message": message,
                }
            )
        )

    @database_sync_to_async
    def get_game(self, game_id):
        try:
            return Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return None

    @database_sync_to_async
    def save_move(self, game, move_number, san, uci, fen):
        Move.objects.create(
            game=game,
            move_number=move_number,
            san=san,
            uci=uci,
            fen_after=fen,
            from_square=uci[:2],
            to_square=uci[2:4],
        )

    @database_sync_to_async
    def update_game(self, game, fen, turn, count):
        game.fen = fen
        game.current_turn = turn
        game.move_count = count
        game.save()

    @database_sync_to_async
    def update_game_status(self, game, status, result):
        game.status = status
        game.result = result
        game.save()


class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add("lobby", self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps({"type": "connected", "message": "Connected to lobby"})
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("lobby", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "join_queue":
            await self.channel_layer.group_send(
                "lobby", {"type": "player_joined", "user": self.user.username}
            )
        elif action == "leave_queue":
            await self.channel_layer.group_send(
                "lobby", {"type": "player_left", "user": self.user.username}
            )

    async def player_joined(self, event):
        await self.send(
            text_data=json.dumps({"type": "player_joined", "user": event.get("user")})
        )

    async def player_left(self, event):
        await self.send(
            text_data=json.dumps({"type": "player_left", "user": event.get("user")})
        )
