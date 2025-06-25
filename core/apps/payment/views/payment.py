from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class PaymentViewset(ViewSet):
    permission_classes = [AllowAny]
    
    @action(methods=["POST"], detail=False, url_name="paylov", url_path="paylov")
    def paylov(self, request):
        data = request.data
        print(data)
        return Response(data={"jsonrpc": "2.0", "id": data.get("id"), "result": {"status": "0", "statusText": "OK"}})
