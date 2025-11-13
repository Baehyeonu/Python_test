from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """사용자 모델 매니저"""
    
    def create_user(self, email, password=None, **extra_fields):
        """일반 사용자 생성"""
        if not email:
            raise ValueError('이메일은 필수입니다')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """슈퍼유저 생성"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """사용자 모델 - 일반 로그인과 소셜 로그인 모두 지원"""
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='이메일'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='이름'
    )
    provider = models.CharField(
        max_length=50,
        default='local',
        verbose_name='로그인 방식'
    )
    provider_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='소셜 로그인 제공자 ID'
    )
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    is_staff = models.BooleanField(default=False, verbose_name='스태프')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
        unique_together = [['provider', 'provider_id']]
    
    def __str__(self):
        return self.email or f"{self.provider}_{self.provider_id}"

