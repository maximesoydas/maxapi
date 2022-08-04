from rest_framework import serializers
from .models import Project, Issue, Comment,Contributor
from accounts.models import User
from accounts.serializers import UserDetailSerializer


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())    
    class Meta:
        model = Project
        fields = ['id','description','title','type','author']
        read_field_only = ['author']
class ContributorSerializer(serializers.ModelSerializer):
    # contributor = serializers.RelatedField(source='email', read_only=True)
    class Meta:
        model = Contributor
        fields = ['contributor','permission', 'role', 'project']
        read_field_only = ['project']
class IssueSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())
    project = serializers.CharField(default='')
    class Meta:
        model = Issue
        fields = ['id','title','description', 'tag','project','author', 'priority','status','created_time','assignee','name','description']
        read_field_only = ['project', 'author']
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())
    issue = serializers.CharField(default='')
    class Meta:
        model = Comment
        fields = ['id','author','description', 'issue', 'created_time']
        read_field_only = ['author', 'issue']
