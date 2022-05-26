from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND,
                                   HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED)
from rest_framework.views import APIView

from ideas.models import Idea
from investments.models import Investment
from investments.permissions import IsInvestor
from investments.serializers import InvestmentSerializer


class InvestmentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInvestor]

    def post(self, request: Request):
        serializer = InvestmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idea = Idea.objects.filter(id=request.data["idea_id"])
       
        if not idea:
            return Response({"error": "idea not found."}, HTTP_404_NOT_FOUND)
        
        if idea[0].finished:
            return Response({"message":"This idea already have finished"}, HTTP_422_UNPROCESSABLE_ENTITY)

        if not idea[0].is_activated:
            return Response({"error": "idea not active."}, HTTP_422_UNPROCESSABLE_ENTITY)

        if request.data["value"]> (idea[0].value - idea[0].amount_collected):
            return Response({"error":f"Your investment can't be bigger than {idea[0].value-idea[0].amount_collected}"}, HTTP_422_UNPROCESSABLE_ENTITY)

        pr = f'{(request.data["value"]*100/idea[0].value):.1f}'

        investment = Investment.objects.create(value = request.data["value"], percentage = pr, user_id = request.user.uuid, idea_id = request.data["idea_id"])

        idea.update(amount_collected = idea[0].amount_collected + request.data["value"])
        if idea[0].value == idea[0].amount_collected:
            idea.update(finished=True, is_activated=False)

        serializer = InvestmentSerializer(investment)

        return Response(serializer.data, HTTP_201_CREATED)