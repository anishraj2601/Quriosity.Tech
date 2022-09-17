from django.contrib import admin
from .models import topic, problem, userProblemData, myfaq, account_verification, like



# class ProblemTopicInline(admin.TabularInline):
#     model = topic
#     extra = 1

# class ProblemAdmin(admin.ModelAdmin):
#     inlines = [ProblemTopicInline]



# Register your models here.
admin.site.register(topic)
admin.site.register(problem)
admin.site.register(userProblemData)
admin.site.register(myfaq)
admin.site.register(account_verification)
admin.site.register(like)

