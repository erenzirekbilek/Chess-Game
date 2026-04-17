import uuid
from django.db import models
from django.contrib.auth.models import User


class GameStatus(models.TextChoices):
    WAITING = "waiting", "Waiting"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    ABANDONED = "abandoned", "Abandoned"


class GameResult(models.TextChoices):
    WHITE_WINS = "white_wins", "White Wins"
    BLACK_WINS = "black_wins", "Black Wins"
    DRAW = "draw", "Draw"
    IN_PROGRESS = "in_progress", "In Progress"


class GameType(models.TextChoices):
    VS_AI = "vs_ai", "vs AI"
    VS_HUMAN = "vs_human", "vs Human"


class Difficulty(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"
    EXPERT = "expert", "Expert"


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    white_player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games_as_white",
    )
    black_player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games_as_black",
    )
    game_type = models.CharField(
        max_length=10, choices=GameType.choices, default=GameType.VS_AI
    )
    status = models.CharField(
        max_length=15, choices=GameStatus.choices, default=GameStatus.WAITING
    )
    result = models.CharField(
        max_length=15, choices=GameResult.choices, default=GameResult.IN_PROGRESS
    )
    fen = models.CharField(
        max_length=100,
        default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    )
    pgn = models.TextField(blank=True, default="")
    ai_difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, null=True, blank=True
    )
    ai_color = models.CharField(max_length=5, blank=True, default="")
    current_turn = models.CharField(max_length=5, default="white")
    move_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id} - {self.game_type}"

    def get_board(self):
        import chess

        return chess.Board(self.fen)


class Move(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    move_number = models.IntegerField()
    san = models.CharField(max_length=10)
    uci = models.CharField(max_length=10)
    fen_after = models.CharField(max_length=100)
    from_square = models.CharField(max_length=2)
    to_square = models.CharField(max_length=2)
    captured_piece = models.CharField(max_length=2, blank=True, default="")
    is_check = models.BooleanField(default=False)
    is_checkmate = models.BooleanField(default=False)
    is_castling = models.BooleanField(default=False)
    castling_type = models.CharField(max_length=5, blank=True, default="")
    promotion = models.CharField(max_length=1, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["move_number"]

    def __str__(self):
        return f"Move {self.move_number}: {self.san}"


class MoveHistory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="history")
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]


class PlayerStats(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="stats",
    )
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    elo_rating = models.IntegerField(default=1200)
    highest_elo = models.IntegerField(default=1200)
    longest_streak = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    streak_type = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return f"{self.user.username} - {self.elo_rating} ELO"

    @property
    def win_rate(self):
        if self.games_played == 0:
            return 0
        return (self.wins / self.games_played) * 100


class GameInvitation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="invitations")
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations",
    )
    status = models.CharField(max_length=10, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.inviter} invites {self.invitee} for {self.game}"
