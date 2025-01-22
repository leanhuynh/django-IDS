from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True)  # Tự động tạo id
    name = models.CharField(max_length=50, unique=True)  # Tên vai trò, không trùng lặp
    description = models.TextField(blank=True, null=True)  # Mô tả vai trò (tùy chọn)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.AutoField(primary_key=True)  # Tự động tạo id
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Trường ảnh
    name = models.CharField(max_length=100)  # Tên người dùng
    email = models.EmailField(unique=True)  # Email, không trùng lặp
    password = models.CharField(max_length=128)  # Mật khẩu (thường được hash)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")  
    # Khóa ngoại tham chiếu đến Role
    # on_delete=models.CASCADE: Xóa User nếu Role bị xóa
    # related_name="users": Tạo mối quan hệ ngược để truy cập User từ Role (role.users.all())

    def __str__(self):
        return self.name