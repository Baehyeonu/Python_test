from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import SignupSerializer, LoginSerializer, UserSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    """회원가입 API"""
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # 필수 필드 검증
        if not request.data.get('email') or not request.data.get('password') or not request.data.get('name'):
            return Response(
                {'message': 'Email, password and name are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(
            {
                'userId': user.id,
                'message': 'User created successfully'
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """로그인 API"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        # 필수 필드 검증
        if not request.data.get('email') or not request.data.get('password'):
            return Response(
                {'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # 사용자 인증
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response(
                    {'message': 'Invalid email or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'message': 'Invalid email or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        
        # 토큰에 사용자 정보 추가
        refresh['userId'] = user.id
        refresh['email'] = user.email
        refresh['name'] = user.name
        
        access_token = refresh.access_token
        access_token['userId'] = user.id
        access_token['email'] = user.email
        access_token['name'] = user.name
        
        return Response(
            {'token': str(access_token)},
            status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveAPIView):
    """사용자 프로필 조회 API"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

