from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Home page"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Auth"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Group"),
                "icon": "group",
                "link": reverse_lazy("admin:auth_group_changelist"),
            },
            {
                "title": _("User"),
                "icon": "accessibility",
                "link": reverse_lazy("admin:accounts_user_changelist"),
            },
        ],
    },
    {
        "title": _("Dashboard"),
        "separator": True,
        "items": [
            {
                "title": _("Product"),
                "icon": "add_shopping_cart",
                "link": reverse_lazy("admin:api_productmodel_changelist"),
            },
            {
                "title": _("Order"),
                "icon": "box",
                "link": reverse_lazy("admin:api_ordermodel_changelist"),
            },
            {
                "title": _("Basket"),
                "icon": "garden_cart",
                "link": reverse_lazy("admin:api_cartmodel_changelist"),
            },
        ],
    },
    {
        "title": _("Payment"),
        "separator": True,
        "items": [
            {
                "title": _("Transactions"),
                "icon": "account_balance_wallet",
                "link": reverse_lazy("admin:payment_transactionmodel_changelist"),
            },
            
        ],
    },
]
