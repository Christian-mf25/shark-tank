from ideas.models import Idea
from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.views import APIView

from investments.models import Investment
from investments.permissions import IsInvestor
from investments.serializers import InvestmentSerializer


class InvestmentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInvestor]

    def post(self, request: Request):
        serializer = InvestmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        idea = Idea.objects.filter(id=serializer.idea_id).first()

        if not idea:
            return Response({"error": "idea not found."}, HTTP_404_NOT_FOUND)

        if not idea.is_activated:
            return Response({"error": "idea not active."}, HTTP_422_UNPROCESSABLE_ENTITY)

        collected_plus_investment = serializer["value"] + idea["value"]
        if collected_plus_investment > idea["value"]:
            return Response(
                {"error": f"can not invest more than {idea.value - idea.amount_collected}"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )

        idea.amount_collected += serializer["value"]
        idea.save()

        serializer["percentage"] = (serializer["value"] * 100) / idea["value"]
        serializer["user_id"] = request.user.id

        investment = Investment.objects.create(**serializer.validated_data)

        serializer = InvestmentSerializer(investment)

        return Response(serializer.data, HTTP_200_OK)
