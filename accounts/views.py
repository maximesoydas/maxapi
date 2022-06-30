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

class RegisterAPIView(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
 
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

register_view = RegisterAPIView.as_view()

class LoginAPIView(APIView):
    
    # authentication_classes = [] #disables authentication
    # permission_classes = [] #disables permission
    def post(self,request):
        user = User.objects.filter(email=request.data['email']).first()
        password = request.data.get("password")
        if not user:
            raise APIException('Invalid Credentials !')
        if not user.check_password(request.data['password']):
            raise APIException('Invalid Credentials')

        response = Response()
        
        return response

login_view = LoginAPIView.as_view()

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset= Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.TokenAuthentication]
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        # title = serializer.validated_data.get('title')
        serializer.save(author=self.request.user)
        # return super().perform_create(serializer)
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = ProjectSerializer(queryset, many=True)
        print('TESTESTESTESTESTES')
        # print(serializer.validated_data)
        print(serializer.data)
        self_user_projects = []
        for data in serializer.data:
            project_id = data['id']
            project_author = Project.objects.filter(pk=project_id).first().author 
            print(project_author)
            print(self.request.user.email)
            # author_id = project_author
            # data['author'] = User.objects.filter(pk=author_id).first().email
            if str(self.request.user.email) == str(project_author):
                self_user_projects.append(data)
                print('true')
            else:
                print('false')
        
        # serializer.data = self_user_projects
        print(serializer.data)
        return Response(self_user_projects)

project_list_create_view = ProjectListCreateAPIView.as_view()

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
    
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        for x in Project.objects.all():
            print(x)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

project_detail_view = ProjectDetailAPIView.as_view()

class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})

user_delete_view = DeleteUser.as_view()
# class UserAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         auth = get_authorization_header(request).split()
#         if auth and len(auth)== 2:
#             token = auth[1].decode('utf-8')
#             id= decode_access_token(token)
#             # use the token to decode the user's primary key/id
#             user = User.objects.filter(pk=id).first()
            
#             return Response(UserSerializer(user).data)
#         raise AuthenticationFailed('unauthenticated')    
            
            
# class RefreshAPIView(APIView):
#     def post(self,request):
#         refresh_token = request.COOKIES.get('refreshToken')
#         id = decode_refresh_token(refresh_token)
        
#         access_token = create_access_token(id)
#         return Response({
#             'token': access_token
#         })
        
        
# class LogoutAPIView(APIView):
#     def post(self,_):
#         response = Response()
#         response.delete_cookie(key='refreshTokens')
#         response.data ={
#             'message':'success',
#         }
#         return response
    
    
    
# class ProjectAPIView(APIView):
    
#     def get(self, request):
#         auth = get_authorization_header(request).split()
#         if auth and len(auth)== 2:
#             token = auth[1].decode('utf-8')
#             id= decode_access_token(token)
#             project = Project.objects.filter(pk=id).first()
            
#             return Response(ProjectSerializer(project).data)
#         raise AuthenticationFailed('unauthenticated')   
    
    
#     def post(self,request):
        
#         serializer = ProjectSerializer(data=request.data)
#         auth = get_authorization_header(request).split()
#         author = self.request.user
#         if serializer.is_valid():
#             token = auth[1].decode('utf-8')
#             id= decode_access_token(token)
#             # serializer.save()
#             title = serializer.data.get('title')
#             message = 'Posted by {0}'.format(title)
#             serializer.data['author'] = author
#             # return json
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)