from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden , HttpResponse
from django.contrib.auth.models import Group
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Personel, GirisCikis, IzinTalebi

@login_required
def giris_cikis_yap(request):
    if not request.user.groups.filter(name="Personel").exists():
        return HttpResponseForbidden("Bu işlemi yalnızca personel yapabilir.")
    
    if request.method == "POST":
        # Giriş ve çıkış saatini otomatik olarak alıyoruz
        current_datetime = datetime.now()

        GirisCikis.objects.create(
            personel=request.user.personel,
            giris_saati=current_datetime,
            cikis_saati=current_datetime
        )
        return redirect("dashboard")  # Dashboard yönlendirmesi
    
    return render(request, "giris_cikis_form.html")
@login_required
def personel_giris(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Personel').exists():
            login(request, user)
            return redirect('personel_giris_cikis')  # Giriş-çıkış sayfasına yönlendir
        elif user is not None and user.groups.filter(name='Yonetici').exists():
            return HttpResponseForbidden("Yönetici olarak giriş yapamazsınız.")
    return render(request, 'personel_login.html')

@login_required
def yonetici_giris(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Yonetici').exists():
            login(request, user)
            return redirect('yonetici_paneli')  # Yönetici paneline yönlendir
        elif user is not None and user.groups.filter(name='Personel').exists():
            return HttpResponseForbidden("Personel olarak giriş yapamazsınız.")
    return render(request, 'yonetici_login.html')

@login_required
def personel_giris_cikis_view(request):
    # Kullanıcıya ait personel kaydını alıyoruz
    personel = request.user.personel  # Kullanıcıya bağlı personel kaydını alıyoruz

    # Personel'in giriş çıkış kayıtlarını alıyoruz
    giris_cikislar = GirisCikis.objects.filter(personel=personel)

    return render(request, 'personel_giris_cikis.html', {'giris_cikislar': giris_cikislar})

@login_required
def personel_giris_view(request, personel_id):
    personel = get_object_or_404(Personel, id=personel_id)
    
    # Giriş işlemi için yeni bir kayıt oluşturuluyor
    giris_kaydi = GirisCikis.objects.create(personel=personel, giris_saati=now())

    # Geç kalma süresi hesaplanıyor ve izin kesintisi yapılması gerekiyorsa, yapılır
    gecikme = giris_kaydi.gecikme_suresi()
    if gecikme > 0:
        kesilecek_izin = int(gecikme // 60)  # Geç kalma dakikaları üzerinden saat cinsinden izin kesimi
        personel.kalan_izin -= kesilecek_izin
        personel.save()

    return redirect('personel_giris_cikis')  # Giriş-Çıkış işlemleri sayfasına yönlendir
@login_required
def personel_cikis_view(request, giris_cikis_id):
    kayit = get_object_or_404(GirisCikis, id=giris_cikis_id)

    # Çıkış saati kaydediliyor
    kayit.cikis_saati = now()
    kayit.save()

    # Çalışma saati hesaplanıyor
    calisma_saati = kayit.calisma_suresi()
    kayit.personel.aylik_calisma_saati += calisma_saati
    kayit.personel.save()

    # Geç kalma cezası uygulanıyor
    gecikme = kayit.gecikme_suresi()
    if gecikme > 0:
        kayit.personel.kalan_izin -= int(gecikme // 60)  # Geç kalma cezası kadar izin kesintisi
        kayit.personel.save()

    return HttpResponse(f"{kayit.personel.user.username} için çıkış işlemi tamamlandı. Çalışma süresi: {calisma_saati:.2f} saat.")
@login_required
def yonetici_paneli(request):
    if not request.user.groups.filter(name='Yonetici').exists():
        return HttpResponseForbidden("Bu sayfayı görüntüleme yetkiniz yok.")

    personeller = Personel.objects.all()
    uyarilar = []
    personel_bilgileri = []

    for personel in personeller:
        son_kayit = personel.giris_cikislar.last()
        gecikme = son_kayit.gecikme_suresi() if son_kayit else None
        calisma_suresi = son_kayit.calisma_suresi() if son_kayit else 0

        if personel.kalan_izin < 3:
            uyarilar.append(f"{personel.user.username} adlı personelin yıllık izni 3 günden az!")

        personel_bilgileri.append({
            'personel': personel,
            'gecikme': gecikme,
            'calisma_suresi': calisma_suresi
        })

    return render(request, 'yonetici_paneli.html', {
        'personel_bilgileri': personel_bilgileri,
        'uyarilar': uyarilar
    })

@login_required
def home(request):
    # Kullanıcının 'Yonetici' grubunda olup olmadığını kontrol et
    is_yonetici = request.user.groups.filter(name='Yonetici').exists()
    
    # Kullanıcının 'Personel' grubunda olup olmadığını kontrol et
    is_personel = request.user.groups.filter(name='Personel').exists()

    return render(request, 'home.html', {
        'is_yonetici': is_yonetici,
        'is_personel': is_personel
    })
    
@login_required
def personel_izinler(request):
    if not request.user.groups.filter(name='Personel').exists():
        return HttpResponseForbidden("Bu sayfayı yalnızca personeller görebilir.")
    
    izinler = request.user.personel.izin_talepleri.all()
    return render(request, 'personel_izinler.html', {'izinler': izinler})

# Yetkili izin yönetim sayfası
@login_required
def izin_yonetimi(request):
    if not request.user.groups.filter(name='Yonetici').exists():
        return HttpResponseForbidden("Bu sayfayı yalnızca yöneticiler görebilir.")
    
    izin_talepleri = IzinTalebi.objects.filter(onaylandi=False, reddedildi=False)
    return render(request, 'izin_yonetimi.html', {'izin_talepleri': izin_talepleri})

# Yetkili izin onaylama
@login_required
def izin_onayla(request, izin_id):
    if not request.user.groups.filter(name='Yonetici').exists():
        return HttpResponseForbidden("Bu işlemi yalnızca yöneticiler yapabilir.")
    
    izin = IzinTalebi.objects.get(id=izin_id)
    izin.onaylandi = True
    izin.save()

    izin.personel.kalan_izin -= izin.izin_suresi()
    izin.personel.save()
    
    return redirect('izin_yonetimi')

# Yetkili izin reddetme
@login_required
def izin_reddet(request, izin_id):
    if not request.user.groups.filter(name='Yonetici').exists():
        return HttpResponseForbidden("Bu işlemi yalnızca yöneticiler yapabilir.")
    
    izin = IzinTalebi.objects.get(id=izin_id)
    izin.reddedildi = True
    izin.save()
    return redirect('izin_yonetimi')

@login_required
def izin_talep_et(request):
    if not request.user.groups.filter(name='Personel').exists():
        return HttpResponseForbidden("Bu işlemi yalnızca personel yapabilir.")
    
    personel = getattr(request.user, 'personel', None)  # Personel kaydını al

    if personel is None:
        return HttpResponseForbidden("Personel kaydınız bulunmamaktadır.")

    if request.method == "POST":
        baslangic = request.POST.get('baslangic_tarihi')
        bitis = request.POST.get('bitis_tarihi')

        # Yeni izin talebi oluştur
        IzinTalebi.objects.create(
            personel=personel,
            baslangic_tarihi=baslangic,
            bitis_tarihi=bitis
        )
        return redirect('personel_izinler')  # Talep listesine yönlendir

    return render(request, 'izin_talep_et.html')


# views.py

from django.shortcuts import render, redirect
from .forms import AdminIzinAtamaForm
from django.contrib.auth.decorators import login_required

@login_required
def admin_izin_atama(request):
    if request.user.is_staff:  # Eğer kullanıcı adminse
        if request.method == 'POST':
            form = AdminIzinAtamaForm(request.POST)
            if form.is_valid():
                form.save()  # Veritabanına kaydet
                return redirect('admin_izin_listesi')  # İzin listesine yönlendir
        else:
            form = AdminIzinAtamaForm()
        return render(request, 'admin_izin_atama.html', {'form': form})
    else:
        return redirect('home') 