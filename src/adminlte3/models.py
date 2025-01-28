from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Role(models.Model):
    id = models.AutoField(primary_key=True)  # Tự động tạo id
    name = models.CharField(max_length=50, unique=True)  # Tên vai trò, không trùng lặp
    description = models.TextField(blank=True, null=True)  # Mô tả vai trò (tùy chọn)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Mã hóa mật khẩu
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# class User(models.Model):
#     id = models.AutoField(primary_key=True)  # Tự động tạo id
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Trường ảnh
#     name = models.CharField(max_length=100)  # Tên người dùng
#     email = models.EmailField(unique=True)  # Email, không trùng lặp
#     password = models.CharField(max_length=128)  # Mật khẩu (thường được hash)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")  
#     # Khóa ngoại tham chiếu đến Role
#     # on_delete=models.CASCADE: Xóa User nếu Role bị xóa
#     # related_name="users": Tạo mối quan hệ ngược để truy cập User từ Role (role.users.all())

#     def __str__(self):
#         return self.name

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Tự động tạo id
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Trường ảnh
    name = models.CharField(max_length=100)  # Tên người dùng
    email = models.EmailField(unique=True)  # Email, không trùng lặp
    password = models.CharField(max_length=128)  # Mật khẩu (thường được hash)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")  

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Đăng nhập bằng email
    REQUIRED_FIELDS = []  # Không có trường bắt buộc ngoài email

    def __str__(self):
        return self.email