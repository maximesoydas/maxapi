from django.contrib import admin
from .models import Project
from .models import Issue
from .models import Comment
from .models import Contributor

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributor)
