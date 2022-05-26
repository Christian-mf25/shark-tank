from ideas.models import Idea
from ideas.serializers import IdeaSerializer
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
        idea = Idea.objects.filter(id=serializer.data["idea_id"])
        # serializer.validated_data.pop("idea_id")
        print("serializeeeeerrr ->", serializer.validated_data)

        if not idea[0]:
            return Response({"error": "idea not found."}, HTTP_404_NOT_FOUND)

        if not idea[0].is_activated:
            return Response({"error": "idea not active."}, HTTP_422_UNPROCESSABLE_ENTITY)

        collected_plus_investment = serializer.data["value"] + idea[0].amount_collected
        if collected_plus_investment > idea[0].value:
            return Response(
                {"error": f"can not invest more than {idea[0].value - idea[0].amount_collected}"},
                HTTP_422_UNPROCESSABLE_ENTITY,
            )
        idea.update(amount_collected=idea[0].amount_collected + request.data["value"])

        investment = Investment.objects.create(
            **serializer.validated_data,
            percentage=(serializer.data["value"] * 100) / idea[0].value,
            user_id=request.user.uuid,
        )

        serializer = InvestmentSerializer(investment)

        return Response(serializer.data, HTTP_200_OK)
