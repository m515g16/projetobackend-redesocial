from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict) -> Usuario:
        return Usuario.objects.create_user(**validated_data)

    def update(self, instance: Usuario, validated_data: dict) -> Usuario:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Usuario
        fields = ["id", "username", "email", "password", "full_name", "birthdate"]
        extra_kwargs = {
            'password': {'write_only': True}
        }