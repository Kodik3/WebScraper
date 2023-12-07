from django.contrib import admin
from .models import (
    CastomUser,
    PageRequests,
    DataPageRequest,
    Subscription
)


admin.site.register(CastomUser)
admin.site.register(PageRequests)
admin.site.register(DataPageRequest)
admin.site.register(Subscription)