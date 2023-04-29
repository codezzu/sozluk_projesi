from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Soru, Yorum
from .forms import SoruForm, YorumForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator


def anasayfa(request):
    sorular = Soru.objects.all().order_by('-tarih')
    return render(request, 'sorular/anasayfa.html', {'sorular': sorular})

def soru_detay(request, soru_id):
    soru = get_object_or_404(Soru, pk=soru_id)
    yorumlar_listesi = soru.yorum_set.order_by("-tarih")

    # Yorumlar için sayfalama
    paginator = Paginator(yorumlar_listesi, 10)  # Her sayfada 10 yorum göster
    page = request.GET.get("page")
    yorumlar = paginator.get_page(page)

    return render(
        request,
        "sorular/soru_detay_ajax.html",
        {"soru": soru, "yorumlar": yorumlar},
    )
@login_required
def soru_ekle(request):
    if request.method == 'POST':
        form = SoruForm(request.POST)
        if form.is_valid():
            yeni_soru = form.save(commit=False)
            yeni_soru.kullanici = request.user
            yeni_soru.save()
            return redirect('soru_detay', soru_id=yeni_soru.id)
    else:
        form = SoruForm()
    return render(request, 'sorular/soru_ekle.html', {'form': form})

@login_required
def yorum_ekle(request, soru_id):
    soru = get_object_or_404(Soru, id=soru_id)
    if request.method == 'POST':
        form = YorumForm(request.POST)
        if form.is_valid():
            yeni_yorum = form.save(commit=False)
            yeni_yorum.kullanici = request.user
            yeni_yorum.soru = soru
            yeni_yorum.save()
            return redirect('soru_detay', soru_id=soru.id)
    else:
        form = YorumForm()
    return render(request, 'sorular/yorum_ekle.html', {'form': form, 'soru': soru})

def arama(request):
    arama_sorgusu = request.GET.get('q')
    eslesen_sorular = Soru.objects.filter(baslik__icontains=arama_sorgusu)

    tam_eslesme = Soru.objects.filter(baslik=arama_sorgusu).first()
    if tam_eslesme:
        return redirect('soru_detay', soru_id=tam_eslesme.id)
    else:
        return render(request, 'sorular/arama_sonuclari.html', {'sorular': eslesen_sorular, 'arama_sorgusu': arama_sorgusu})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anasayfa')
    else:
        form = UserCreationForm()
    return render(request, 'sorular/signup.html', {'form': form})

@login_required
def baslik_olustur(request):
    if request.method == 'POST':
        baslik = request.POST.get('soru')
        yeni_baslik = Soru.objects.create(baslik=baslik, kullanici=request.user)
        return redirect('soru_detay', soru_id=yeni_baslik.id)
    else:
        return redirect('anasayfa')


def yorum_ekle(request, soru_id):
    if request.method == "POST":
        form = YorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.kullanici = request.user
            yorum.soru = get_object_or_404(Soru, pk=soru_id)
            yorum.save()

            # JSON response oluşturma
            return JsonResponse({
    'success': True,
    'kullanici': request.user.username,
    'yorum': yorum.icerik,  # 'yorum' yerine 'icerik' kullanın
    'tarih': yorum.tarih.strftime('%Y-%m-%d %H:%M')
})

    return HttpResponseRedirect(reverse("soru_detay", args=(soru_id,)))

