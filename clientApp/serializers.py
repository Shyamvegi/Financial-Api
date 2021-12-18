from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):

    #token=serializers.Field(source='my_token')
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        user = authenticate(**data)
        if user.isactive==False:
            isactive=True
            return user
        else:
            raise serializers.ValidationError("user already logged in")
        raise serializers.ValidationError("Invalid Details.")

