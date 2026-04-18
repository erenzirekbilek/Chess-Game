import chess
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import (
    Game,
    Move,
    PlayerStats,
    GameInvitation,
    GameStatus,
    GameResult,
    GameType,
)
from .serializers import (
    GameSerializer,
    GameCreateSerializer,
    GameDetailSerializer,
    MoveSerializer,
    PlayerStatsSerializer,
)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return GameCreateSerializer
        elif self.action in ["retrieve", "update", "partial_update"]:
            return GameDetailSerializer
        return GameSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        game_type = serializer.validated_data.get("game_type", GameType.VS_AI)
        ai_difficulty = serializer.validated_data.get("ai_difficulty", "medium")
        ai_color = serializer.validated_data.get("ai_color", "black")

        if game_type == GameType.VS_AI:
            import random

            player_color = ai_color if ai_color else random.choice(["white", "black"])
            ai_color = "black" if player_color == "white" else "white"
        else:
            player_color = "white"
            ai_color = ""

        board = chess.Board()
        fen = board.fen()

        game = Game.objects.create(
            game_type=game_type,
            status=GameStatus.ACTIVE
            if game_type == GameType.VS_AI
            else GameStatus.WAITING,
            fen=fen,
            ai_difficulty=ai_difficulty,
            ai_color=ai_color,
            current_turn="white",
            move_count=0,
        )

        response_serializer = GameSerializer(game)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = GameSerializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def make_move(self, request, pk=None):
        game = self.get_object()
        uci = request.data.get("uci")

        if not uci:
            return Response(
                {"error": "No move provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            board = chess.Board(game.fen)
            move = chess.Move.from_uci(uci)

            if move not in board.legal_moves:
                return Response(
                    {"error": "Illegal move"}, status=status.HTTP_400_BAD_REQUEST
                )

            san = board.san(move)
            captured = board.piece_at(move.to_square)
            is_check = board.is_check()
            is_castling = board.is_castling(move)
            castling_type = ""
            if is_castling:
                if chess.square_file(move.from_square) < chess.square_file(
                    move.to_square
                ):
                    castling_type = "kingside"
                else:
                    castling_type = "queenside"

            board.push(move)
            new_fen = board.fen()
            game.fen = new_fen
            game.current_turn = "white" if board.turn == chess.WHITE else "black"
            game.move_count += 1

            Move.objects.create(
                game=game,
                move_number=game.move_count,
                san=san,
                uci=uci,
                fen_after=new_fen,
                from_square=chess.square_name(move.from_square),
                to_square=chess.square_name(move.to_square),
                captured_piece=captured.symbol() if captured else "",
                is_check=is_check,
                is_checkmate=board.is_checkmate(),
                is_castling=is_castling,
                castling_type=castling_type,
                promotion=move.promotion.name.lower() if move.promotion else "",
            )

            if board.is_checkmate():
                game.status = GameStatus.COMPLETED
                game.result = (
                    GameResult.WHITE_WINS
                    if board.turn == chess.BLACK
                    else GameResult.BLACK_WINS
                )
            elif board.is_stalemate() or board.is_insufficient_material():
                game.status = GameStatus.COMPLETED
                game.result = GameResult.DRAW

            game.save()

            response_data = {
                "fen": new_fen,
                "turn": "white" if board.turn == chess.WHITE else "black",
                "move": uci,
                "san": san,
                "is_checkmate": board.is_checkmate(),
                "is_check": board.is_check(),
                "is_stalemate": board.is_stalemate(),
            }

            if game.game_type == GameType.VS_AI and game.status != GameStatus.COMPLETED:
                if board.turn == chess.BLACK and game.ai_color == "black":
                    response_data["ai_move"] = None
                elif board.turn == chess.WHITE and game.ai_color == "white":
                    response_data["ai_move"] = None
                else:
                    from backend.chess_engine import create_engine

                    engine = create_engine(difficulty=game.ai_difficulty or "medium")
                    ai_move = engine.get_best_move(board)
                    if ai_move:
                        ai_uci = ai_move.uci()
                        board.push(ai_move)
                        ai_fen = board.fen()
                        game.fen = ai_fen
                        game.current_turn = (
                            "white" if board.turn == chess.WHITE else "black"
                        )
                        game.move_count += 1

                        Move.objects.create(
                            game=game,
                            move_number=game.move_count,
                            san=board.san(ai_move),
                            uci=ai_uci,
                            fen_after=ai_fen,
                            from_square=chess.square_name(ai_move.from_square),
                            to_square=chess.square_name(ai_move.to_square),
                            is_check=board.is_check(),
                            is_checkmate=board.is_checkmate(),
                        )

                        if board.is_checkmate() or board.is_stalemate():
                            game.status = GameStatus.COMPLETED
                            if board.is_checkmate():
                                winner = (
                                    game.white_player
                                    if board.turn == chess.BLACK
                                    else game.black_player
                                )
                                game.result = (
                                    GameResult.WHITE_WINS
                                    if winner == game.white_player
                                    else GameResult.BLACK_WINS
                                )
                            else:
                                game.result = GameResult.DRAW

                        game.save()
                        response_data["ai_move"] = ai_uci
                        response_data["ai_fen"] = ai_fen
                        response_data["turn"] = "white" if board.turn == chess.WHITE else "black"

            return Response(response_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def resign(self, request, pk=None):
        game = self.get_object()
        player = request.user if request.user.is_authenticated else None

        game.status = GameStatus.COMPLETED
        if game.white_player == player:
            game.result = GameResult.BLACK_WINS
        else:
            game.result = GameResult.WHITE_WINS

        game.save()
        return Response({"message": "Resigned"})

    @action(detail=False, methods=["get"])
    def my_games(self, request):
        if not request.user.is_authenticated:
            return Response([])
        games = Game.objects.filter(
            models.Q(white_player=request.user) | models.Q(black_player=request.user)
        ).order_by("-created_at")[:20]
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        games = Game.objects.filter(status=GameStatus.ACTIVE)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
