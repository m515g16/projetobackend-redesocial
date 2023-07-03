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
        fields = ["id", "perfil", "name", "username", "email", "password", "birthdate", "created_at", "updated_at", "followers", "friends"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class FollowerSerializer(serializers.ModelSerializer):
    # follower_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    follower = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    # def create(self, validated_data: dict) -> User:
    #     return User.objects.create(**validated_data)

    class Meta:
        model = Follower
        fields = ["id", "follower", "user_id", "user"]
        # extra_kwargs = {
        #     'follower': {'read_only': True},
        #     'user': {'read_only': True}
        # }
        read_only_fields = ["follower", "user"]
    
class FriendSerializer(serializers.ModelSerializer):
    ...
#     # followers = UserSerializer(read_only=True)
#     # friends = UserSerializer(read_only=True)

#     def create(self, validated_data: dict) -> User:
#         return User.objects.create_user(**validated_data)

#     def update(self, instance: User, validated_data: dict) -> User:
#         for key, value in validated_data.items():
#             if key == "password":
#                 instance.set_password(value)
#             else:
#                 setattr(instance, key, value)

#         instance.save()

#         return instance

#     class Meta:
#         model = User
#         fields = ["id", "perfil", "name", "username", "email", "password", "birthdate", "created_at", "updated_at", "followers", "friends"]
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }