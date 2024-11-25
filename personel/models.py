# from django.db import models
# from django.contrib.auth.models import User
# from datetime import time

# class Personel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     giris_saati = models.DateTimeField(null=True, blank=True)
#     cikis_saati = models.DateTimeField(null=True, blank=True)
#     kalan_izin_gunu = models.IntegerField(default=15)
#     aylik_calisma_saati = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

#     def __str__(self):
#         return self.user.username

# class IzinTalebi(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="izin_talepleri")
#     baslangic_tarihi = models.DateField()
#     bitis_tarihi = models.DateField()
#     onaylandi = models.BooleanField(default=False)
#     reddedildi = models.BooleanField(default=False)

#     def izin_suresi(self):
#         return (self.bitis_tarihi - self.baslangic_tarihi).days

# class GecikmeKaydi(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="gecikmeler")
#     gecikme_saati = models.TimeField(default=time(0, 0))
#     gecikme_tarihi = models.DateField(auto_now_add=True)


# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime, time

# # Personel Modeli
# class Personel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personel")
#     pozisyon = models.CharField(max_length=100, default="Personel")
#     kalan_izin = models.PositiveIntegerField(default=15)  # Başlangıçta 15 gün izin
#     aylik_calisma_saati = models.FloatField(default=0)  # Toplam çalışma saatleri (aylık)

#     def __str__(self):
#         return self.user.username

# # Giriş-Çıkış Kaydı Modeli
# class GirisCikis(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="giris_cikislar")
#     giris_saati = models.DateTimeField()
#     cikis_saati = models.DateTimeField(null=True, blank=True)
#     tarih = models.DateField(auto_now_add=True)

#     def gecikme_suresi(self):
#         is_baslangic_saati = time(8, 0)  # Şirket başlangıç saati: 08:00
#         if self.giris_saati.time() > is_baslangic_saati:
#             delta = datetime.combine(self.tarih, self.giris_saati.time()) - datetime.combine(self.tarih, is_baslangic_saati)
#             return delta.total_seconds() / 60  # Dakika cinsinden
#         return 0

#     def calisma_suresi(self):
#         if self.cikis_saati:
#             delta = self.cikis_saati - self.giris_saati
#             return delta.total_seconds() / 3600  # Saat cinsinden
#         return 0

# # İzin Talebi Modeli
# class IzinTalebi(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="izin_talepleri")
#     baslangic_tarihi = models.DateField()
#     bitis_tarihi = models.DateField()
#     onaylandi = models.BooleanField(default=False)

#     def izin_suresi(self):
#         return (self.bitis_tarihi - self.baslangic_tarihi).days


# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime, time

# # Personel Modeli
# class Personel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personel")
#     pozisyon = models.CharField(max_length=100, default="Personel")
#     kalan_izin = models.PositiveIntegerField(default=15)  # Başlangıçta 15 gün izin
#     aylik_calisma_saati = models.FloatField(default=0)  # Toplam çalışma saati (aylık)

#     def __str__(self):
#         return self.user.username

# # Giriş-Çıkış Kaydı Modeli
# class GirisCikis(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="giris_cikislar")
#     giris_saati = models.DateTimeField()
#     cikis_saati = models.DateTimeField(null=True, blank=True)
#     tarih = models.DateField(auto_now_add=True)

#     def calisma_suresi(self):
#         """Çalışma süresini hesapla"""
#         if self.cikis_saati:
#             delta = self.cikis_saati - self.giris_saati
#             return delta.total_seconds() / 3600  # Saat cinsinden
#         return 0

#     def gecikme_suresi(self):
#         """Geç kalma süresi hesapla"""
#         is_baslangic_saati = time(8, 0)  # Şirket başlangıç saati: 08:00
#         if self.giris_saati.time() > is_baslangic_saati:
#             delta = datetime.combine(self.tarih, self.giris_saati.time()) - datetime.combine(self.tarih, is_baslangic_saati)
#             return delta.total_seconds() / 60  # Dakika cinsinden
#         return 0

# # İzin Talebi Modeli
# class IzinTalebi(models.Model):
#     personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="izin_talepleri")
#     baslangic_tarihi = models.DateField()
#     bitis_tarihi = models.DateField()
#     onaylandi = models.BooleanField(default=False)

#     def izin_suresi(self):
#         return (self.bitis_tarihi - self.baslangic_tarihi).days



from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time

# Personel Modeli

class Personel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personel")
    pozisyon = models.CharField(max_length=100, default="Personel")
    personel_id = models.CharField(max_length=100, unique=False)  # personel_id burada tanımlanmış
    kalan_izin = models.PositiveIntegerField(default=15)  # Başlangıçta 15 gün izin
    aylik_calisma_saati = models.FloatField(default=0)  # Toplam çalışma saati (aylık)

    def __str__(self):
        return self.user.username
    
# class Personel(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personel")
#     pozisyon = models.CharField(max_length=100, default="Personel")
#     kalan_izin = models.PositiveIntegerField(default=15)  # Başlangıçta 15 gün izin
#     aylik_calisma_saati = models.FloatField(default=0)  # Toplam çalışma saati (aylık)
#     personel_id = models.CharField(max_length=100, unique=False)  # Yeni kolon: Personel ID

#     def __str__(self):
#         return self.user.username

class GirisCikis(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="giris_cikislar")
    giris_saati = models.DateTimeField(auto_now_add=True)  # Otomatik olarak giriş saatini alır
    cikis_saati = models.DateTimeField(null=True, blank=True, auto_now=True)  # Çıkış saati de otomatik alır
    tarih = models.DateField(auto_now_add=True)  # Tarih de otomatik olarak kaydedilir

    def calisma_suresi(self):
        """Çalışma süresi hesaplama"""
        if self.cikis_saati:
            delta = self.cikis_saati - self.giris_saati
            return delta.total_seconds() / 3600  # Saat cinsinden
        return 0

    def gecikme_suresi(self):
        """Geç kalma süresi hesaplama"""
        is_baslangic_saati = time(8, 0)  # Şirket başlangıç saati: 08:00
        if not self.tarih:
            self.tarih = datetime.today().date()  # Eğer tarih None ise, bugünün tarihi alınıyor

        if self.giris_saati.time() > is_baslangic_saati:
            delta = datetime.combine(self.tarih, self.giris_saati.time()) - datetime.combine(self.tarih, is_baslangic_saati)
            return delta.total_seconds() / 60  # Dakika cinsinden
        return 0

    def save(self, *args, **kwargs):
        if not self.pk:  # Yeni bir giriş kaydı oluşturuluyorsa
            gecikme = self.gecikme_suresi()
            if gecikme > 0:
                kesilecek_izin = int(gecikme // 60)  # Saat cinsinden izin kesimi
                self.personel.kalan_izin -= kesilecek_izin
                self.personel.save()
        super().save(*args, **kwargs)
# İzin Talebi Modeli
class IzinTalebi(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="izin_talepleri")
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    onaylandi = models.BooleanField(default=False)
    reddedildi = models.BooleanField(default=False)

    def izin_suresi(self):
        return (self.bitis_tarihi - self.baslangic_tarihi).days

class AdminIzinAtama(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name="admin_izinleri")
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()

    def __str__(self):
        return f"{self.personel.user.username} - {self.baslangic_tarihi} to {self.bitis_tarihi}"