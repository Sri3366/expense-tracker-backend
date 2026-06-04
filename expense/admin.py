from django.contrib import admin # type: ignore
from .models import UserDetail,Expense
#from .models import * 

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Expense)