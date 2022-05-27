import re
from django.http import JsonResponse
from .models import Project, Contributor, Comment, Issue
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminAuthenticated


# recuperer le refresh et l'accesss token au result custom_signup/login



@api_view(['GET', 'POST'])
# @permission_classes((IsAdminAuthenticated, ))
def project_list(request, format=None):
    if request.method == 'GET':
        # get all projects
        projects = Project.objects.all()
        # serialize them
        serializer = ProjectSerializer(projects, many=True)
        # return json
        return Response(serializer.data)

    if request.method == 'POST':
        # serialize them
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data, status=status.HTTP_201_created)

@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request,id,format=None):
    try:
        project=Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # View Read
    if request.method == 'GET':
       serializer = ProjectSerializer(project)
       return Response(serializer.data)

    # View Update
    elif request.method == 'PUT':
        # serialize them
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # View Delete
    elif request.method == 'DELETE':
        # serialize them
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# CONTRIBUTOR VIEW API
@api_view(['GET', 'POST'])
# @permission_classes((IsAdminAuthenticated, ))
def contributor_list(request, format=None):
    if request.method == 'GET':
        # get all contributors
        contributors = Contributor.objects.all()
        # serialize them
        serializer = ContributorSerializer(contributors, many=True)
        # return json
        return Response(serializer.data)

    if request.method == 'POST':
        # serialize them
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data, status=status.HTTP_201_created)

@api_view(['GET', 'PUT', 'DELETE'])
def contributor_detail(request,id,format=None):
    try:
        contributor=Contributor.objects.get(pk=id)
    except Contributor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # View Read
    if request.method == 'GET':
       serializer = ContributorSerializer(contributor)
       return Response(serializer.data)

    # View Update
    elif request.method == 'PUT':
        # serialize them
        serializer = ContributorSerializer(contributor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # View Delete
    elif request.method == 'DELETE':
        # serialize them
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# COMMENT VIEW API
@api_view(['GET', 'POST'])
# @permission_classes((IsAdminAuthenticated, ))
def comment_list(request, format=None):
    if request.method == 'GET':
        # get all comments
        comments = Comment.objects.all()
        # serialize them
        serializer = CommentSerializer(comments, many=True)
        # return json
        return Response(serializer.data)

    if request.method == 'POST':
        # serialize them
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data, status=status.HTTP_201_created)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request,id,format=None):
    try:
        comment= Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # View Read
    if request.method == 'GET':
       serializer = CommentSerializer(comment)
       return Response(serializer.data)

    # View Update
    elif request.method == 'PUT':
        # serialize them
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # View Delete
    elif request.method == 'DELETE':
        # serialize them
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# ISSUE VIEW API

@api_view(['GET', 'POST'])
# @permission_classes((IsAdminAuthenticated, ))
def issue_list(request, format=None):
    if request.method == 'GET':
        # get all issues
        issues = Issue.objects.all()
        # serialize them
        serializer = IssueSerializer(issues, many=True)
        # return json
        return Response(serializer.data)

    if request.method == 'POST':
        # serialize them
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data, status=status.HTTP_201_created)

@api_view(['GET', 'PUT', 'DELETE'])
def issue_detail(request,id,format=None):
    try:
        issue= Issue.objects.get(pk=id)
    except Issue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # View Read
    if request.method == 'GET':
       serializer = IssueSerializer(issue)
       return Response(serializer.data)

    # View Update
    elif request.method == 'PUT':
        # serialize them
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return json
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # View Delete
    elif request.method == 'DELETE':
        # serialize them
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
