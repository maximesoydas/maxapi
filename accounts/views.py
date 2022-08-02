from xml.etree.ElementTree import XML
from requests import request
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.authentication import get_authorization_header
from maxapi.models import Project, Contributor, Comment, Issue
from rest_framework import authentication, generics, mixins, permissions, status
from .serializers import UserSerializer
from .models import User
from maxapi.serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
# from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
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
        tokens['user_access_jwt_token'] = str(RefreshToken.for_user(user).access_token)
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
        serializer.save(author=self.request.user)
        serializer.save()
        project = serializer.save()
        contributor = Contributor.objects.create(contributor=self.request.user,permission=1,project=project, role='author')
        contributor.save()

        # return super().perform_create(serializer)
    def list(self, request):
        queryset = Project.objects.filter(contributor__contributor=self.request.user.id).order_by('id')
        serializer = ProjectSerializer(queryset, many=True)   
        if serializer.data == []:
            return Response('There is no projects related to the current user') 
        return Response(serializer.data)

project_list_create_view = ProjectListCreateAPIView.as_view()


# # api/projects/id/
class ProjectDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset= Project.objects.all()
    print('TESTESTSETESTSE')
    # print(queryset)
    serializer_class = ProjectSerializer
    """
    Retrieve, update or delete a Project ID.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # contributors = queryset = Project.objects.filter(contributor__contributor=self.request.user.id).order_by('id')
        # contributor_serializer = ProjectSerializer(contributors)
        print('CONTRIBUTOR')
        contrib_obj = Contributor.objects.all()
        serialize_contributor = ContributorSerializer(contrib_obj)
        print(serialize_contributor)
        
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        print(project.id)
        print(project.author)
        print('AUTHOR AUTHOR')
        print(self.request.user.id)
        if project.author == self.request.user:
            print('true')
            print(serializer.data)
            return Response(serializer.data)
        
        else:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if project.author == self.request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

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
        project_id = Project.objects.get(id=pk)
        # print(project_id.author)
        # print(self.request.user.email)
        # print(serializer)
        # on va chercher a rajouter l'utilisateur x au projet
        # contributor/utilisateur, permission 1or2, role, project.id
        # pour mettre un contributor il nous faut etre author
        for contributor in Contributor.objects.filter(project= pk):
            print(str(contributor.contributor.id))
            print(str(serializer.data['contributor']))
            if str(contributor.contributor.id) == str(serializer.data['contributor']):
                raise ValidationError('Current user is already a contributor')
         
        if project_id.author == self.request.user:
            serializer.save(project = project_id)
        else:
            raise ValidationError('Current user is not the author of this project')
            # if contributor.contributor.id == serializer.contributor


    def list(self, request, pk):
        print(self.kwargs['pk'])
        project = Project.objects.get(id=pk)
        print('AUTHOR AUTHOR')
        print(project.author)
        # print(self.request.user.email)
        
        queryset = Contributor.objects.filter(project_id=pk).order_by('id')
        if project in Project.objects.filter(contributor__contributor=self.request.user):
            serializer = ContributorSerializer(queryset, many=True)
            # print(serializer.data['project'])
            for data in serializer.data:
                print(data)
                projid= Project.objects.get(id=data['project'])
                data['project'] = projid.title
                userid= User.objects.get(id=data['contributor'])
                data['contributor'] = userid.email
                
            return Response(serializer.data)
        else:
            return Response("User is not a contributor of this project")
contributor_list_create_view = ContributorListCreateAPIView.as_view()







class ContributorDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset= Project.objects.all()
    # print(queryset)
    serializer_class = ContributorSerializer
    """
    Retrieve, update or delete a Contributor ID.
    """

    
    def delete(self, request, format=None,*args, **kwargs):

        user_id = self.kwargs['pk_alt']

        project_id = self.kwargs['pk']
        print(user_id)
        print(project_id)
        for contributor in Contributor.objects.filter(project_id=project_id).order_by('id'):
            print(contributor.contributor.id)
            if contributor.contributor.id == user_id:
                # Maybe verify if user is the author of project? maybe dont remove author from contributors
                contributor.delete()
                return Response(f"Contributor {contributor.contributor} removed from project")
            else:
                return Response("Specifed user is not a contributor of this project")            
contributor_detail_view = ContributorDetailAPIView.as_view()





# api/delete/user
class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminAuthenticated]

    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})

user_delete_view = DeleteUser.as_view()
