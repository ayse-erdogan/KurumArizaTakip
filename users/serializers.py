from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser, Issue, IssueComment, IssueAttachment
from django.contrib.auth import authenticate

# 🔹 **Kullanıcı Serializer**

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'role', 'assigned_area']

    def to_representation(self, instance):
        """🔥 Serializer çıktısını manuel olarak kontrol ediyoruz"""
        data = super().to_representation(instance) #manuel olarak instance.role ile ekler
        if 'role' not in data:
            data['role'] = instance.role
        print(f"✅ Serializer Output: {data}")
        return data



# 🔹 **Kullanıcı Rol Güncelleme Serializer (Admin için)**
class UserRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role']

    def validate_role(self, value):
        if value not in ['admin', 'technician', 'user']:
            raise serializers.ValidationError("Geçersiz rol.")
        return value


# 🔹 **Admin Kullanıcı Oluşturma Serializer**
class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'role', 'assigned_area', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            role=validated_data.get('role', 'user'),
            assigned_area=validated_data.get('assigned_area', '')
        )
        return user


# 🔹 **Arıza Serializer**
class IssueSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')  # ✅ Kullanıcının email'ini döndür
    assigned_to = UserSerializer(read_only=True)
    category = serializers.CharField(default="Diğer", allow_blank=True)

    class Meta:
        model = Issue
        fields = '__all__'


# 🔹 **Arıza Yorumları Serializer**
class IssueCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = IssueComment
        fields = '__all__'


# 🔹 **Kullanıcı Kayıt Serializer**
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', '')
        )
        return user


# 🔹 **Kullanıcı Giriş Serializer**
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user and user.is_active:
            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "assigned_area": user.assigned_area,
            }
        raise serializers.ValidationError("Geçersiz giriş bilgileri.")



# 🔹 **Arıza Fotoğrafı Serializer**
class IssueAttachmentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = IssueAttachment
        fields = ['id', 'issue', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None
