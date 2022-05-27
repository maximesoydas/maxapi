from telnetlib import STATUS
from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.test import tag


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.title + 'by' + self.author.first_name


class Contributor(models.Model):
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_choice = (
        (1, ("allowed")),
        (2, ("not allowed")),
    )
    permission = models.IntegerField(choices=permission_choice)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.contributor + ' ' + self.role


class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    author = models.ForeignKey(User,  related_name='author', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE)
    created_time =  models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.issue + "comment's"
