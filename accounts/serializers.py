from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 시리얼라이저"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'provider', 'created_at')
        read_only_fields = ('id', 'provider', 'created_at')


class SignupSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    
    class Meta:
        model = User
        fields = ('email', 'password', 'name')
    
    def validate_email(self, value):
        """이메일 중복 확인"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value
    
    def create(self, validated_data):
        """사용자 생성"""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """로그인 시리얼라이저"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

