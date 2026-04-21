from django.contrib import admin
from .models import Branch, Member, Trainer, GymClass, Equipment, DamagedEquipment

admin.site.register(Branch)
admin.site.register(Member)
admin.site.register(Trainer)
admin.site.register(GymClass)
admin.site.register(Equipment)

@admin.register(DamagedEquipment)
class DamagedEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'is_damaged')
    list_filter = ('branch',)
    
    def has_add_permission(self, request):
        return False