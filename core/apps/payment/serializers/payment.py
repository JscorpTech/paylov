from rest_framework import serializers


class PaylovAccountSerializer(serializers.Serializer):
    order_id = serializers.CharField()


class PaylovParamsSerializer(serializers.Serializer):
    account = PaylovAccountSerializer()
    amount = serializers.CharField()
    amount_tiyin = serializers.CharField()
    currency = serializers.IntegerField()


class PaylovCallbackSerializers(serializers.Serializer):
    METHODS = (
        ("transaction.check", "Check"),
        ("transaction.perform", "Perform"),
    )
    jsonrpc = serializers.CharField()
    method = serializers.ChoiceField(choices=METHODS)
    params = PaylovParamsSerializer()
    id = serializers.IntegerField()
