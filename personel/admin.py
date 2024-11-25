from django.contrib import admin
from .models import Personel,AdminIzinAtama, GirisCikis, IzinTalebi

@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ('user', 'pozisyon', 'kalan_izin', 'aylik_calisma_saati')

@admin.register(GirisCikis)
class GirisCikisAdmin(admin.ModelAdmin):
    list_display = ('personel', 'giris_saati', 'cikis_saati', 'gecikme_suresi', 'calisma_suresi')

@admin.register(IzinTalebi)
class IzinTalebiAdmin(admin.ModelAdmin):
    list_display = ('personel', 'baslangic_tarihi', 'bitis_tarihi', 'onaylandi')
class AdminIzinAtamaAdmin(admin.ModelAdmin):
    list_display = ('personel', 'baslangic_tarihi', 'bitis_tarihi')
    search_fields = ['personel__user__username']

admin.site.register(AdminIzinAtama, AdminIzinAtamaAdmin)