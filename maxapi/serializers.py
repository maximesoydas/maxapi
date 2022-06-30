from rest_framework import serializers
from .models import Project, Issue, Comment,Contributor
from accounts.models import User
from accounts.serializers import UserDetailSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id',
                  'description',
                #   'author',
                  'title',
                  'type'
                  ]

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id','contributor','permission', 'role']
class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id','title','description', 'tag', 'priority','project','status','author','created_time','assignee','name','description']
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author','description', 'issue', 'created_time']
