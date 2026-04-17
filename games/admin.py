from django.contrib import admin
from .models import Game, Move, PlayerStats, GameInvitation


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["id", "game_type", "status", "result", "created_at"]
    list_filter = ["game_type", "status", "result"]


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ["game", "move_number", "san", "uci"]


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    list_display = ["user", "elo_rating", "games_played", "wins", "losses", "draws"]


@admin.register(GameInvitation)
class GameInvitationAdmin(admin.ModelAdmin):
    list_display = ["game", "inviter", "invitee", "status", "created_at"]
