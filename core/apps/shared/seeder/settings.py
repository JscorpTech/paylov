from core.apps.shared.models import SettingsModel, OptionsModel


class SettingsSeeder:

    def run(self):
        config = {
            "currency": {
                "exchange_rate": [12631.45],
            }
        }
        for key, value in config.items():
            settings = SettingsModel.objects.get_or_create(key=key, defaults={"is_public": True})
            for item_key, item_value in value.items():
                OptionsModel.objects.get_or_create(key=item_key, settings=settings, defaults={"value": item_value})
