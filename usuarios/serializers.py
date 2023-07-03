from rest_framework import serializers
from .models import User, Follower, Friend




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
        fields = ["id", "perfil", "name", "username", "email", "password", "birthdate", "created_at", "updated_at", "followers", "friend_solicitations", "friends"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    follower = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ["id", "follower", "user_id", "user"]
        read_only_fields = ["follower", "user"]
        extra_kwargs = {
            'user_id': {'write_only': True}
        }
    
class FriendSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    friend = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ["id", "friend", "user_id", "user", "pendding", "accepted", "solicited"]
        read_only_fields = ["friend", "user", "pendding", "accepted", "solicited"]
        extra_kwargs = {
            'user_id': {'write_only': True}
        }