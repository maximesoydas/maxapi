from ast import Not
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from maxapi.models import Project, Contributor, Comment, Issue
from rest_framework import generics, permissions, status
from .serializers import UserSerializer
from .models import User
from maxapi.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAdminAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotFound
#api/regitser
class RegisterAPIView(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
 
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

register_view = RegisterAPIView.as_view()


#api/login
class LoginAPIView(APIView):
    def post(self,request):
        tokens = {}
        user = User.objects.filter(email=request.data['email']).first()
        password = request.data.get("password")
        if not user:
            raise APIException('Invalid Credentials !')
        if not user.check_password(request.data['password']):
            raise APIException('Invalid Credentials')
        tokens['user_email'] = user.email
        tokens['user_name'] = f"{user.first_name} {user.last_name}"
        tokens['user_access_jwt_token'] = str(AccessToken.for_user(user))
        tokens['user_refresh_jwt_token'] = str(RefreshToken.for_user(user).access_token)
        tokens['user_id'] = user.id
        response = Response(tokens)
        return response

login_view = LoginAPIView.as_view()

# api/projects
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset= Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save()
        contributor = Contributor.objects.create(contributor=self.request.user,permission=1,project=project, role='author')
        contributor.save()
        return super(ProjectListCreateAPIView, self).perform_create(serializer)

    def list(self, request):
        # try:
        queryset = Project.objects.filter(contributor__contributor=self.request.user.id).order_by('id')
        serializer = ProjectSerializer(queryset, many=True)   
        for project_data in serializer.data:
            proj = Project.objects.filter(id=project_data['id']).order_by('id')
            for p in proj:
                author = p.author
            project_data['author'] = str(author)

        if serializer.data == []:
            return Response('There is no projects related to the current user') 
        return Response(serializer.data)
    


project_list_create_view = ProjectListCreateAPIView.as_view()

# api/projects/id/
class ProjectDetailAPIView(APIView):
    """
    Retrieve, update or delete a Project ID.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {pk}":"Not found"})

    def get(self, request, pk, format=None):
        try:
            contrib_obj = Contributor.objects.all()
            serialize_contributor = ContributorSerializer(contrib_obj)
            project = Project.objects.get(id=pk)
            serializer = ProjectSerializer(project)
            contriblist = []
            for contributor in Contributor.objects.filter(project_id=pk).order_by('id'):
                contriblist.append(str(contributor.contributor.email))
            if project.author == self.request.user:
                return Response(serializer.data)
            if self.request.user.email in contriblist:
                return Response(serializer.data)
            else:
                return Response(data={f"User is not a contributor of this project"})
        except Project.DoesNotExist:
            return Response(data={f"Project {pk} was not found"})


    def put(self, request, pk, format=None):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(data={f"Project {pk} was not found"})
        data = self.request.data
        project.description = data["description"]
        project.title = data["title"]
        project.type = data["type"]
        if project.author == self.request.user:
            project.save()
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        else:
            return Response("User is not the author of this Project")

    def delete(self, request, pk, format=None):
        
        project = self.get_object(pk)
        if project.author == self.request.user:
            project.delete()
            return Response(f"Project {pk} deleted")
        else:
            return Response("User is not an author of this Project (only the author of a project can successfully use the Delete request)")
project_detail_view = ProjectDetailAPIView.as_view()

# api/projects/id/users/
class ContributorListCreateAPIView(generics.ListCreateAPIView):
    queryset= Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            project_id = Project.objects.get(id=pk)
            for contributor in Contributor.objects.filter(project= pk):
                print(str(contributor.contributor.id))
                print(str(serializer.validated_data['contributor']))
                if str(contributor.contributor.id) == str(serializer.validated_data['contributor'].id):
                    raise NotFound({f'User {pk} ': 'Current user is already a contributor'})
                
            
            if project_id.author == self.request.user:
                serializer.save(project = project_id)
            else:
                raise NotFound('Current user is not the author of this project')
        except Project.DoesNotExist:
            raise NotFound({f"Project {pk}": "Not Found"})


    def list(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            return Response(data={f"Project {pk} was not found"})
        queryset = Contributor.objects.filter(project_id=pk).order_by('id')
        if project in Project.objects.filter(contributor__contributor=self.request.user):
            serializer = ContributorSerializer(queryset, many=True)
            for data in serializer.data:
                projid= Project.objects.get(id=data['project'])
                data['project'] = projid.title
                userid= User.objects.get(id=data['contributor'])
                data['contributor'] = userid.id
                
            return Response(serializer.data)
        else:
            return Response("User is not a contributor of this project")
contributor_list_create_view = ContributorListCreateAPIView.as_view()



# api/projects/id/users/id/
class ContributorDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContributorSerializer
    """
    Retrieve, update or delete a Contributor ID.
    """
    def delete(self, request, format=None,*args, **kwargs):
        user_id = self.kwargs['pk_alt']
        project_id = self.kwargs['pk']
        project = Project.objects.get(pk=project_id)
        contriblist = []
        for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
            contriblist.append(contributor.contributor.id)
        if user_id == project.author.id:
            # Maybe verify if the user is the author of project dont remove author from contributors
            raise  NotFound({f"Project {project_id}": "Project author cannot be removed from contributors"}) 
        if user_id in contriblist:
            if self.request.user.id == user_id:
                contributor.delete()
                return Response(f"Contributor {contributor.contributor} removed from project")
            elif self.request.user.id == project.author.id:
                contributor.delete()
                return Response(f"Contributor {contributor.contributor} removed from project")
            else:
                return Response(f"User is neither the project owner nor the specified contributor ")
        else:
            return Response("Specifed user is not a contributor of this project")            
contributor_detail_view = ContributorDetailAPIView.as_view()


# api/delete/user
class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminAuthenticated]
    # delete own account
    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()
        return Response({"result":"user delete"})

user_delete_view = DeleteUser.as_view()

# api/projects/id/users/
class IssueListCreateAPIView(generics.ListCreateAPIView):
    queryset= Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    project = None
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            project_id = Project.objects.get(id=pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {pk}":"Project was not found"})
        print(serializer.validated_data['assignee'])
        contriblist=[]
        # if assignee is not in contributor return error
        for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
            contriblist.append(str(contributor.contributor.email))
            if contributor == self.request.user.email:
                if contributor.permission == 2:
                    return Response("Contributor has permission level 2 therefore he is not allowed to create issues on this project")

        if str(self.request.user.email) not in contriblist:
            raise NotFound({"User":"Not a contributor of this project"})
        if str(serializer.validated_data['assignee']) not in contriblist:
            print('xzx')
            raise NotFound({"Please set the assignee as a contributor before assigning issues"})
        serializer.validated_data['project']= project_id
        serializer.validated_data['author'] = self.request.user
        serializer.save()
        

    def list(self, request, pk):
        print(self.kwargs['pk'])
        project = Project.objects.get(id=pk)
        # print(self.request.user.email)
        
        queryset = Issue.objects.filter(project_id=pk).order_by('id')
        if project in Project.objects.filter(contributor__contributor=self.request.user):
            serializer = IssueSerializer(queryset, many=True)
            # print(serializer.data['project'])
            
            return Response(serializer.data)
        else:
            return Response("User is not a contributor of this project")
issue_list_create_view = IssueListCreateAPIView.as_view()


class IssueDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset= Project.objects.all()
    # print(queryset)
    serializer_class = IssueSerializer
    def get_object(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            raise Http404
    """
    Retrieve, update or delete an issue.
    """
          
    def put(self, *args, **kwargs):
        pk = self.kwargs['pk_alt']
    
        try:
            issue = Issue.objects.get(id=pk)
        except Issue.DoesNotExist:
            raise NotFound({f"Issue {pk}": "Not Found"})
        print(issue)
        data = self.request.data
        
        issue.title = data["title"]
        issue.tag = data["tag"]
        issue.priority = data["priority"]
        issue.status = data["status"]
        issue.assignee = User.objects.get(pk=data["assignee"])
        issue.name = data["name"]
        issue.description = data["description"]
        if issue.author == self.request.user:
            issue.save()
            serializer = IssueSerializer(issue)
            return Response(serializer.data)
        else:
            return Response("User is not the author of this issue")


    def delete(self, request, format=None,*args, **kwargs):

        obj_id = self.kwargs['pk_alt']

        project_id = self.kwargs['pk']
        contriblist = []

        for issue in Issue.objects.filter(pk=obj_id).order_by('pk'):
            print(issue.author.id)
            if issue.author.id == self.request.user.id:
                # Maybe verify if the user is the author of project? maybe dont remove author from contributors
                issue.delete()
                return Response(f"Issue {issue} removed from project")
            for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
                print(contributor.contributor.id)
                print(self.request.user.id)
                if str(self.request.user.id) == str(contributor.contributor.id):
                    print(contributor.permission)
                    if contributor.permission == 1:
                        
                        issue.delete()
                        return Response(f"Issue {obj_id} : {issue} removed from project by contributor {contributor.contributor} with permission ")
            else:
                return Response("Current user cannot remove the issue (missing rights)")      
        return Response("Wrong issue id (incomplete or inexistent)")           
issue_detail_view = IssueDetailAPIView.as_view()


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset= Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def perform_create(self, serializer, *args, **kwargs):
        project_pk = self.kwargs['pk']
        issue_pk = self.kwargs['pk_alt']
        try:
            project_id = Project.objects.get(id=project_pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {project_pk}": "Not Found"})
        try:
            issue_id = Issue.objects.get(id=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound({f"Issue {issue_pk}": "Not Found"})
        
        contriblist=[]
        # if assignee is not in contributor return error
        for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
            print(contributor.contributor)
            # print(serializer.data)
            contriblist.append(str(contributor.contributor.email))
        if str(self.request.user.email) not in contriblist:
            raise NotFound({f"User {self.request.user.email}":" is not a contributor of this project"})
        serializer.validated_data['issue']= issue_id
        serializer.validated_data['author'] = self.request.user
        serializer.save()
        


    def list(self, request, pk, *args, **kwargs):
        
        project_pk = self.kwargs['pk']
        issue_pk = self.kwargs['pk_alt']
        try:
            project_id = Project.objects.get(id=project_pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {project_pk}": "Not Found"})
        try:
            issue = Issue.objects.get(id=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound({f"Issue {issue_pk}": "Not Found"})
        contriblist=[]
        for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
            contriblist.append(str(contributor.contributor.email))
            
        if str(self.request.user.email) not in contriblist:
            raise NotFound("User is not a contributor of this project")
        queryset = Comment.objects.filter(issue_id=issue).order_by('id')
        serializer = CommentSerializer(queryset, many=True)
            
        return Response(serializer.data)

comment_list_create_view = CommentListCreateAPIView.as_view()

class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    
    def get(self,*args, **kwargs):
        project_pk = self.kwargs['pk_project']
        issue_pk = self.kwargs['pk_issue']
        comment_pk = self.kwargs['pk_comment']
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {project_pk}": "Not Found"})
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound({f"Issue {issue_pk}": "Not Found"})
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound({f"Comment {comment_pk}": "Not Found"})
        
        contriblist = []
        for contributor in Contributor.objects.filter(project_id=project).order_by('id'):
            contriblist.append(str(contributor.contributor.email))
        serializer = CommentSerializer(comment)

        if str(self.request.user.email) not in contriblist:
            return Response("User is not a contributor of this project")
        else:
            return Response(serializer.data)

    
    def put(self, *args, **kwargs):
        data = self.request.data
        project_pk = self.kwargs['pk_project']
        issue_pk = self.kwargs['pk_issue']
        comment_pk = self.kwargs['pk_comment']

        
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise NotFound({f"Project {project_pk}": "Not Found"})
        try:
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound({f"Issue {issue_pk}": "Not Found"})
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound({f"Comment {comment_pk}": "Not Found"})
        comment.description = data["description"]
        if comment.author == self.request.user:
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response("User is not the author of this comment")


    def delete(self, request, format=None,*args, **kwargs):
        comment_pk = self.kwargs['pk_comment']
        try:
            comment=Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
          raise NotFound({f"Comment {comment_pk}": "Comment not found"})
        if comment.author == self.request.user:
            comment.delete()
            serializer = CommentSerializer(comment)
            return Response(f"comment id number {comment_pk} deleted successfully")
        else:
            return Response("User is not the author of this comment")
    
comment_detail_view = CommentDetailAPIView.as_view()
