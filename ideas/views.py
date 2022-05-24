from datetime import datetime, timedelta
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response
from rest_framework import status
from ideas.models import Idea

from ideas.permissions import CreateOrRead
from ideas.serializers import IdeaSerializer

class IdeasView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[CreateOrRead]
    def post(self, request:Request):
        serializer = IdeaSerializer(data = request.data)
        serializer.is_valid(True)
        try:
            userIdea = Idea.objects.filter(user_id=request.user.id).last()
            if userIdea:
                if userIdea.finished:
                    idea = Idea.objects.create(**serializer.validated_data, limited_date= datetime.now()+timedelta(days=1), user_id = request.user.id)
                    serializer = IdeaSerializer(idea)
                else: 
                    raise IntegrityError
            else: 
                idea = Idea.objects.create(**serializer.validated_data, limited_date= datetime.now()+timedelta(days=1), user_id = request.user.id)
                serializer = IdeaSerializer(idea)
        except IntegrityError:
            return Response({"error":"User already have an active proposal"}, status.HTTP_409_CONFLICT)
        return Response(serializer.data, status.HTTP_201_CREATED)