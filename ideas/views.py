from datetime import datetime, timedelta

from django.forms import ValidationError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response
from users.models import User

from ideas.models import Idea
from ideas.permissions import CreateOrRead, OwnerRead
from ideas.serializers import IdeaInvestmentsSerializer, IdeaSerializer, IdeaUpdateSerializer
from investments.models import Investment
from users.models import User



class IdeasView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateOrRead]

    def post(self, request: Request):
        serializer = IdeaSerializer(data=request.data)
        serializer.is_valid(True)

        
        userIdeas = Idea.objects.filter(user_id=request.user.uuid).all()
        user = User.objects.get(uuid=request.user.uuid)
        activated_idea = True
        for ea_idea in userIdeas:
            if ea_idea.is_activated:
                activated_idea = False

        idea = Idea.objects.create(
            **serializer.validated_data,
            deadline=datetime.now() + timedelta(days=1),
            user_id=user.uuid,
            is_activated=activated_idea
        )

        serializer = IdeaSerializer(idea)

        return Response(serializer.data)

    def get(self, request: Request, idea_id=""):
        if idea_id:
            idea = Idea.objects.filter(id=idea_id)
            idea.first()
            if not idea:
                return Response({"error": "Idea is not found"}, status.HTTP_404_NOT_FOUND)
            if not request.user.is_superuser:
                if not idea[0].is_activated:
                    return Response({"message": "This proposal is not activated"}, status.HTTP_422_UNPROCESSABLE_ENTITY)
            now = datetime.now()
            if str(now) > str(idea[0].deadline)[:-6] and idea[0].finished == False:
                idea.update(amount_collected=0, deadline=datetime.now() + timedelta(days=1))
                investments= Investment.objects.filter(idea_id=idea[0].id)
                investments.delete()
            serializer = IdeaSerializer(idea[0], request.user)
            return Response(serializer.data, status.HTTP_200_OK)

        ideas = Idea.objects.filter(is_activated=True).all()
        if request.user.is_superuser:
            ideas = Idea.objects.all()

        for ea_idea in ideas:
            now = datetime.now()
            idea = Idea.objects.filter(id=ea_idea.id)
            idea.first()
            if str(now) > str(ea_idea.deadline)[:-6] and ea_idea.finished == False:
                idea.update(amount_collected=0, deadline=datetime.now() + timedelta(days=1))
                investments = Investment.objects.filter(idea_id=ea_idea.id)
                investments.delete()
        serializer = IdeaSerializer(ideas, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, idea_id=""):
        serializer = IdeaUpdateSerializer(data=request.data)
        serializer.is_valid(True)

        idea = Idea.objects.filter(id=idea_id)
        idea.first()
        user_idea = Idea.objects.filter(id=idea_id, user_id=request.user.uuid)

        if not idea:
            return Response({"error": "Idea does not exists"}, status.HTTP_404_NOT_FOUND)

        if not user_idea:
            return Response({"error": "This idea does not belong to you"}, status.HTTP_401_UNAUTHORIZED)

        if "is_activated" in request.data:
            if not request.data["is_activated"]:
                if idea[0].amount_collected > 0:
                    return Response(
                        {"error": "This proposal have investments. Can't be deactivated"}, status.HTTP_401_UNAUTHORIZED
                    )
                else:
                    idea.update(**serializer.validated_data)
                    serializer = IdeaSerializer(idea[0])
                    return Response(serializer.data, status.HTTP_200_OK)
            else:
                this_idea = Idea.objects.filter(is_activated=True, user_id=request.user.uuid, id=idea_id)
                if this_idea:
                    return Response({"message": "This proposal is already activated"}, status.HTTP_200_OK)
                activated_idea = Idea.objects.filter(is_activated=True, user_id=request.user.uuid)
                if activated_idea:
                    return Response({"message": "Already have an active proposal"}, status.HTTP_401_UNAUTHORIZED)
                else:
                    idea.update(**serializer.validated_data)
                    serializer = IdeaSerializer(idea[0])
                    return Response(serializer.data, status.HTTP_200_OK)
        idea.update(**serializer.validated_data)
        serializer = IdeaSerializer(idea[0])
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, idea_id=""):

        idea = Idea.objects.filter(id=idea_id)
        idea.first()
        user_idea = Idea.objects.filter(id=idea_id, user_id=request.user.uuid)

        if not idea:
            return Response({"error": "Idea does not exists"}, status.HTTP_404_NOT_FOUND)

        if not user_idea:
            return Response({"error": "You can't perform this action"}, status.HTTP_401_UNAUTHORIZED)

        if idea[0].amount_collected > 0:
            return Response(
                {"error": "This proposal have investments. Can't be deleted"}, status.HTTP_401_UNAUTHORIZED
            )
        investments = Investment.objects.filter(idea_id=idea_id)
        investments.delete()
        idea.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class IdeaOwnerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerRead]

    def get(self, request: Request, idea_id=""):
        try:
            if idea_id:
                idea = Idea.objects.filter(id=idea_id, user_id=request.user.uuid)
                idea.first()
                if not idea:
                    return Response({"error": "Proposal not found"}, status.HTTP_404_NOT_FOUND)

                idea_investments= Investment.objects.filter(idea_id = idea[0].id).all()
    
                serializer_idea_investment = IdeaInvestmentsSerializer(idea_investments, many= True)

                now = datetime.now()
                if str(now) > str(idea[0].deadline)[:-6] and idea[0].finished == False:
                    idea.update(amount_collected=0, deadline = datetime.now()+timedelta(days=1))
                    investments = Investment.objects.filter(idea_id=idea[0].id)
                    investments.delete()

                serializer = IdeaSerializer(idea[0])
                return Response({"idea":serializer.data, "investors":serializer_idea_investment.data}, status.HTTP_200_OK)

            ideas = Idea.objects.filter(user_id=request.user.uuid).all()
            for ea_idea in ideas:
                now = datetime.now()  
                idea = Idea.objects.filter(id = ea_idea.id)
                idea.first()
                if str(now) > str(ea_idea.deadline)[:-6] and ea_idea.finished == False:
                    idea.update(amount_collected=0, deadline= datetime.now()+timedelta(days=1))
                    investments = Investment.objects.filter(idea_id = ea_idea.id)
                    investments.delete()

            serializer = IdeaSerializer(ideas, many=True)

            return Response(serializer.data, status.HTTP_200_OK)
        except ValidationError:
            return Response({"error": "Proposal not found"}, status.HTTP_404_NOT_FOUND)
