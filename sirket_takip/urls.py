from django.contrib.auth import views as auth_views
from django.urls import path
from personel.views import personel_giris_cikis_view,admin_izin_atama,giris_cikis_yap,personel_giris,izin_talep_et,personel_izinler,izin_yonetimi,izin_onayla,izin_reddet,yonetici_giris,personel_cikis_view,personel_giris_view, yonetici_paneli,home


urlpatterns = [
    # Personel ve Yetkili Login ve Logout
    path('personel/login/', auth_views.LoginView.as_view(template_name='personel_login.html'), name='personel_login'),
    path('yonetici/login/', auth_views.LoginView.as_view(template_name='yonetici_login.html'), name='yonetici_login'),
    
    # Personel Logout işlemi
    # Personel Logout işlemi
    path('personel/logout/', auth_views.LogoutView.as_view(next_page='/personel/login/'), name='personel_logout'),

    path('giris-cikis/', giris_cikis_yap, name='giris_cikis'),
    # Personel İşlemleri
    path('giris/<int:personel_id>/', personel_giris_view, name='personel_giris'),
    path('cikis/<int:giris_cikis_id>/', personel_cikis_view, name='personel_cikis'),

    # Yönetici Paneli (Yalnızca Yöneticiler erişebilir)
    path('yonetici/', yonetici_paneli, name='yonetici_paneli'),

    # Ana Sayfa (Home)
    path('', home, name='home'),
    path('personel/izinler/', personel_izinler, name='personel_izinler'),
    path('yonetici/izinler/', izin_yonetimi, name='izin_yonetimi'),
    path('yonetici/izinler/onayla/<int:izin_id>/', izin_onayla, name='izin_onayla'),
    path('yonetici/izinler/reddet/<int:izin_id>/', izin_reddet, name='izin_reddet'),
    path('personel/izin_talep/', izin_talep_et, name='izin_talep_et'),
    path('personel/giris_cikis/', personel_giris_cikis_view, name='personel_giris_cikis'),

    path('admin-izin-atama/', admin_izin_atama, name='admin_izin_atama'),
]
