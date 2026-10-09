from django.contrib import admin
from .models import Candidate , Polls , Vote
# Register your models here.

@admin.register(Polls)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')
    # inlines = [candidateInline]

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name' , 'description')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'poll', 'candidate', 'created_at')
    readonly_fields = ('created_at',)

