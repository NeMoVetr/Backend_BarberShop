from django.contrib import admin

from .models import Hall, Service, Client, Employee, Visit
from .time_slots import update_status_visits


# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'date_of_birth', 'gender')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'phone_number', 'date_of_birth', 'gender')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'position', 'get_halls', 'get_services')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'phone_number', 'position', 'halls__name', 'services__name')

    def get_halls(self, obj):
        return ', '.join([hall.name for hall in obj.halls.all()]) if obj.halls.exists() else "Нет залов"
    get_halls.short_description = 'Залы'

    def get_services(self, obj):
        return ', '.join([service.name for service in obj.services.all()]) if obj.services.exists() else "Нет услуг"
    get_services.short_description = 'Услуги'


class HallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'capacity', 'location', 'start_time', 'end_time')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description', 'capacity', 'location', 'start_time', 'end_time')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'duration')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description', 'price', 'duration')


class VisitAdmin(admin.ModelAdmin):
    update_status_visits()
    list_display = ('id', 'client', 'employee', 'hall', 'service', 'date', 'time', 'status')
    list_display_links = ('id', 'employee')
    search_fields = ('client', 'employee', 'hall', 'service', 'date', 'time', 'status')


admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Visit, VisitAdmin)
