from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Move, PlayerStats, GameInvitation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = [
            "id",
            "move_number",
            "san",
            "uci",
            "fen_after",
            "from_square",
            "to_square",
            "captured_piece",
            "is_check",
            "is_checkmate",
            "is_castling",
            "castling_type",
            "promotion",
        ]


class GameSerializer(serializers.ModelSerializer):
    white_player = UserSerializer(read_only=True)
    black_player = UserSerializer(read_only=True)
    moves = MoveSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = [
            "id",
            "white_player",
            "black_player",
            "game_type",
            "status",
            "result",
            "fen",
            "pgn",
            "ai_difficulty",
            "ai_color",
            "current_turn",
            "move_count",
            "moves",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GameCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["game_type", "ai_difficulty", "ai_color"]


class MoveCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = [
            "game",
            "move_number",
            "san",
            "uci",
            "fen_after",
            "from_square",
            "to_square",
            "captured_piece",
            "is_check",
            "is_checkmate",
            "is_castling",
            "castling_type",
            "promotion",
        ]


class PlayerStatsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    win_rate = serializers.ReadOnlyField()

    class Meta:
        model = PlayerStats
        fields = [
            "user",
            "games_played",
            "wins",
            "losses",
            "draws",
            "elo_rating",
            "highest_elo",
            "win_rate",
            "longest_streak",
            "current_streak",
            "streak_type",
        ]


class GameInvitationSerializer(serializers.ModelSerializer):
    inviter = UserSerializer(read_only=True)
    invitee = UserSerializer(read_only=True)
    game = GameSerializer(read_only=True)

    class Meta:
        model = GameInvitation
        fields = [
            "id",
            "game",
            "inviter",
            "invitee",
            "status",
            "created_at",
            "expires_at",
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "fen", "pgn", "current_turn", "move_count", "status", "result"]
