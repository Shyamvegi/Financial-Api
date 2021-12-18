from django.contrib import admin

# Register your models here.
from django.contrib import admin 
from .models import *   

# Register your models here.
admin.site.register(LogsModel)
admin.site.register(ItemModel)
admin.site.register(TransactionsModel)
admin.site.register(ItemMetadata)
admin.site.register(AccountDetails)