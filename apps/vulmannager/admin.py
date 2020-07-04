from django.contrib import admin
from apps.vulmannager.models import (
    Vulnerability, PenetrationTestTicketResult, PenetrationTestTicket,
    VulWorkflow, PenetrationTestTicketSubWorkflow, VulSubWorkflow, Asset, Port)


admin.site.register([Vulnerability,
                     VulWorkflow,
                     VulSubWorkflow,
                     PenetrationTestTicketResult,
                     PenetrationTestTicket,
                     PenetrationTestTicketSubWorkflow,
                     Asset,
                     Port])
