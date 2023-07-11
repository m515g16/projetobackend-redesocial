from rest_framework import serializers
from .models import User, Followers, FriendSolicitations




class FriendAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendSolicitations
        fields = ["id","friend","user"]


class PenddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendSolicitations
        fields = ["id","friend","pendding"]

class UserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    pendding_requests = serializers.SerializerMethodField()

    def get_pendding_requests(self, user):
        penddings = FriendSolicitations.objects.filter(user=user, pendding=True)
        serializer = PenddingSerializer(penddings, many=True)

        return serializer.data

    def get_friends(self, user):
        friends_accepted = FriendSolicitations.objects.filter(user=user, accepted=True)
        friends_requested = FriendSolicitations.objects.filter(friend=user, accepted=True)
        friends = [*friends_accepted, *friends_requested]
        serializer = FriendAnswerSerializer(friends, many=True)

        return serializer.data

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
        fields = ["id", "perfil", "name", "username", "email", "password", "birthdate",
                  "created_at", "updated_at", "followers", "friends", "pendding_requests"]
        extra_kwargs = {
            'password': {'write_only': True},
            'friends': {'read_only': True}
        }

class UserPublicSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "perfil", "name", "username")

class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    follower = UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Followers
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
        model = FriendSolicitations
        fields = ["id", "friend", "user", "user_id", "accepted", "pendding"]
        read_only_fields = ["friend", "user"]
        extra_kwargs = {
            'user_id': {'write_only': True}
        }


class FriendUser1Serializer(serializers.ModelSerializer):
    friend = UserPublicSerializer(read_only=True)
    

    class Meta:
        model = FriendSolicitations
        fields = ["id", "friend"]
        read_only_fields = ["friend"]

class FriendUser2Serializer(serializers.ModelSerializer):
    
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = FriendSolicitations
        fields = ["id", "user"]
        read_only_fields = ["user"]

class UserFriendSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()

    def get_friends(self, user):
        friends_accepted = FriendSolicitations.objects.filter(user=user, accepted=True)
        friends_requested = FriendSolicitations.objects.filter(friend=user, accepted=True)
        serializer_requested = FriendUser2Serializer(friends_requested, many=True)
        serializer_accepted = FriendUser1Serializer(friends_accepted, many=True)
        friends = [*serializer_requested.data, *serializer_accepted.data]

        return friends

    class Meta:
        model = User
        fields = ["id", "perfil", "name", "username", "friends"]

class FollowerUserSerializer(serializers.ModelSerializer):
    follower = UserPublicSerializer(read_only=True)
    

    class Meta:
        model = FriendSolicitations
        fields = ["id", "follower"]
        read_only_fields = ["follower"]

class UserFollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    def get_followers(self, user):
        followers = Followers.objects.filter(user=user)
        
        followers = FollowerUserSerializer(followers, many=True)
        
        return followers.data

    class Meta:
        model = User
        fields = ["id", "perfil", "name", "username", "followers"]
       



