from django.contrib import admin
from .models import office,Gardner,Dweller,appointments,bookedappointments,pending_Gardners,Admin
admin.site.register(office)
admin.site.register(Gardner)
admin.site.register(Dweller)
admin.site.register(appointments)
admin.site.register(bookedappointments)

admin.site.register(pending_Gardners)
admin.site.register(Admin)

# Register your models here.
