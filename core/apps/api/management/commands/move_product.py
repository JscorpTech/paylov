import json
from uuid import uuid4

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.db import transaction

from core.apps.api.models.product import ProductModel


class Command(BaseCommand):

    def handle(self, *args, **options) -> str | None:
        with open("products.json", "r") as file:
            products = json.load(file)
            with transaction.atomic():
                for product in products:
                    product_obj = ProductModel.objects.create(
                        name=product["title"],
                        price=product["price"] or 0,
                        description=product["description"],
                        quantity=10000,
                    )
                    if len(product["images"]) <= 0:
                        continue
                    response = requests.get(product["images"][0])
                    file_name = str(uuid4()) + "." + product["images"][0].split(".")[-1]
                    product_obj.image.save(file_name, ContentFile(response.content), save=False)
                    product_obj.save()
