from rest_framework import serializers
from .models import Student,Song


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['title','artists','genre','album_or_movie','user_rating','url']

        def validate_url(self, value):
            if value and not value.startswith(('http://', 'https://')):
               raise serializers.ValidationError("The URL must start with http:// or https://.")
            return value

