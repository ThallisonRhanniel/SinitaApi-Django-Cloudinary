from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CommentSerializer
from .models import EventComments
from rest_framework.authtoken.models import Token
from random import randint
from rest_framework.parsers import MultiPartParser, FormParser
from cloudinary.templatetags import cloudinary
from django.http import JsonResponse


class CommentListView(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = CommentSerializer

    def get(self, request, format=None):
        comments = EventComments.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, image_name):
        cloudinary.uploader.upload(
            request.FILES['imagem'],
            public_id=image_name,
            crop='limit',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                 'crop': 'thumb', 'gravity': 'face',
                 'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ],
            tags=['icon_perfil', 'sinitaApi']
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                imageName = '{0}_v{1}'.format(request.FILES['imagem'].name.split('.')[0],
                                              randint(0, 100))
                self.upload_image_cloudinary(request, imageName)
                serializer.save(icon_perfil=imageName)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response({'imagem': 'Envie uma imagem valida'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messagem": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):  # filter by ID
    serializer_class = CommentSerializer

    def get_object(self, pk):
        get_object_or_404(EventComments, pk=pk)

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = self.serializer_class(comment)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = self.serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            comment = EventComments.objects.get(pk=pk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as message:
            return Response(status=status.HTTP_404_NOT_FOUND)


def token_request(request):
    try:
        new_token = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': new_token[0].key}, status=status.HTTP_200_OK)
    except Exception as message:
        return JsonResponse({'messagem': 'você não tem permissão.'}, status=status.HTTP_401_UNAUTHORIZED)
