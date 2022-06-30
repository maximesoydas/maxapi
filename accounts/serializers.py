from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
             'password': {'write_only': True}
        }
    # password hasher
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    
class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields= [
            'email',
            'first_name',
            'last_name',
        ]
        
        