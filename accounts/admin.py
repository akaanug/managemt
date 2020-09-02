from django.contrib import admin

# Register your models here.

from .models import Product
from .models import Invoice
from .models import Logs

from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(Invoice, SimpleHistoryAdmin)
admin.site.register(Logs, SimpleHistoryAdmin)
