import requests


from django.db.models import Q
from django.shortcuts import render
import csv
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student,Song
from .serializers import StudentSerializer,LoginSerializer,SongSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

BASE_API_URL = "https://music-recommendation-system-qirr.onrender.com"

class RecommendSongsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        song_title = request.data.get("song")
        if not song_title:
            return Response({
                "status": False,
                "message": "Song title is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(f"{BASE_API_URL}/recommend", json={"song": song_title})
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({
                "status": False,
                "message": f"Error communicating with the recommendation API: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AddFavoriteSongAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        song_title = request.data.get("song")
        if not song_title:
            return Response({
                "status": False,
                "message": "Song title is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(f"{BASE_API_URL}/add_favorite", json={"song": song_title})
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({
                "status": False,
                "message": f"Error communicating with the favorite API: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetNextSongAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            response = requests.post(f"{BASE_API_URL}/next_song")
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({
                "status": False,
                "message": f"Error communicating with the next song API: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
            user = User.objects.create_user(username=name, password=password, email=email)
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
    

class SearchSongAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({
                "status": False,
                "message": "Search query is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        search_query = Q(title__icontains=query) | Q(artists__icontains=query)
        songs =  Song.objects.filter(search_query)

        print(f"Query: {query}")  
        print(f"Songs found: {songs}")
        
        serializer = SongSerializer(songs, many=True)

        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    
class UploadSongsCSVAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file', None)

        if not file:
            return Response({
                "status": False,
                "message": "No file provided."
            }, status=status.HTTP_400_BAD_REQUEST)
        file_path = default_storage.save(f"uploads/{file.name}", file)

        try:
            with open(default_storage.path(file_path), mode="r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                songs_created = 0

                for row in reader:
                    if not row.get("Song-Name") or not row.get("Singer/Artists"):
                        continue

                    song, created = Song.objects.get_or_create(
                        title=row["Song-Name"],
                        defaults={
                            "artists": row["Singer/Artists"],
                            "genre": row.get("Genre", ""),
                            "album_or_movie": row.get("Album/Movie", ""),
                            "user_rating": row.get("User-Rating", None),
                             
                        },
                    )
                    if created:
                        songs_created += 1

            default_storage.delete(file_path)

            return Response({
                "status": True,
                "message": f"CSV processed successfully. {songs_created} songs added."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            default_storage.delete(file_path)
            return Response({
                "status": False,
                "message": f"Error processing CSV: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

