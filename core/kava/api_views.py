from rest_framework.views import APIView
from .models import Exchange
from .serializers import ExchangeSerializer
from rest_framework.response import Response


class ExchangeList(APIView):
    """
    List all Exchanges
    """
    def get(self, request, format=None):
        snippets = Exchange.objects.all()
        serializer = ExchangeSerializer(snippets, many=True)
        return Response(serializer.data)

