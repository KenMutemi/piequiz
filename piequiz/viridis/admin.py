from django.contrib import admin
from viridis.models import Test, Question, Choice, Vote

class VoteAdmin(admin.ModelAdmin): pass
admin.site.register(Vote, VoteAdmin)

class TestAdmin(admin.ModelAdmin): pass
admin.site.register(Test, TestAdmin)

admin.site.register(Choice)
admin.site.register(Question)
