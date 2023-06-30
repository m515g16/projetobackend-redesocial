from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "name", "birthdate", "created_at", "updated_at"]
        extra_kwargs = {
            'password': {'write_only': True}
        }