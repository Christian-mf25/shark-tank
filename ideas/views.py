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
        userIdeas = Idea.objects.filter(user_id = request.user.id).all()
        activated_idea=True
        for ea_idea in userIdeas:
            if ea_idea.is_activated:
                activated_idea = False 
        
        idea = Idea.objects.create(**serializer.validated_data, limited_date = datetime.now()+timedelta(days=1), user_id = request.user.id, is_activated = activated_idea)
        
        serializer = IdeaSerializer(idea)

        return Response(serializer.data)

    
    def get(self, _:Request, idea_id=""):
        if idea_id:
            idea= Idea.objects.filter(id = idea_id)
            idea.first()
            if not idea:
                return Response({"error":"Idea is not found"}, status.HTTP_404_NOT_FOUND)
            if not idea[0].is_activated:
                return Response({"message":"This proposal is not activated"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            now = datetime.now()
            if str(now) > str(idea[0].limited_date)[:-6] and idea[0].finished == False:
                idea.update(amount_collected=0, limited_date = datetime.now()+timedelta(days=1))
                # investments= Investment.objects.filter(idea_id=idea[0].id)
                # investments.delete()
               
            
            serializer = IdeaSerializer(idea[0])
            return Response(serializer.data, status.HTTP_200_OK)
               
        ideas = Idea.objects.filter(is_activated=True).all()
        for ea_idea in ideas:
            now = datetime.now()  
            idea = Idea.objects.filter(id = ea_idea.id)
            idea.first()
            if str(now) > str(ea_idea.limited_date)[:-6] and ea_idea.finished == False:
                idea.update(amount_collected=0, limited_date= datetime.now()+timedelta(days=1))
                # investments = Investment.objects.filter(idea_id=ea_idea.id)
                # investments.delete()
            

        serializer = IdeaSerializer(ideas, many= True)

        return Response(serializer.data, status.HTTP_200_OK)