from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



class StudentApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        print(request.user)
        queryset = Student.objects.all()
        serializer= StudentSerializer(queryset,many=True)
        return Response({
            "status" : True,
            "data" : serializer.data
        })
    

class SignupAPI(APIView):
    def post(self, request):
        data = request.data

        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
       

        if not name or not password or not email:
            return Response({
                "status": False,
                "message": "name, password, and email are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        
        if User.objects.filter(email=email).exists():
            return Response({
                "status": False,
                "message": "email already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        
        try:
            user = User.objects.create_user(name=name, password=password, email=email)
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "status": True,
                "message": "User created successfully.",
                "data": {"token": str(token)}
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"Error: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginAPI(APIView):
    def post(self , request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
            "status" : False,
            "data" : serializer.errors,
            "message": "Invalid data"
        })
        
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']


        user_obj = User.objects.filter(email=email).first()


        if user_obj and user_obj.check_password(password):
            token , _= Token.objects.get_or_create(user=user_obj)
            return Response({
            "status" : True,
            "data" : {'token' : str(token)  }
        })

        return Response({
            "status" : False,
            "data" : {},
            "message" : "invalid credentials"
        })
    

class PlaySongAPI(APIView):
  
    permission_classes = [IsAuthenticated]

    def post(self, request):
        song_id = request.data.get("song_id")  
        song = {"id": song_id, "title": "Example Song", "artist": "Example Artist"}

        if not song_id:
            return Response(
                {
                    "status": False,
                    "message": "Song ID is required to play a song.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        
        return Response(
            {
                "status": True,
                "message": f"Playing song: {song['title']} by {song['artist']}",
                "data": song,
            },
            status=status.HTTP_200_OK,
        )