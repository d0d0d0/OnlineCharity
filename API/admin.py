from django.contrib import admin

# Register your models here.
from django.contrib import admin
from API.models import Charity,Person

admin.site.register(Charity)
admin.site.register(Person)