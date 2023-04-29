from django.db import models
from django.contrib.auth.models import User

class Soru(models.Model):
    baslik = models.CharField(max_length=200)
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.baslik

class Yorum(models.Model):
    soru = models.ForeignKey(Soru, on_delete=models.CASCADE)
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    icerik = models.TextField()  # Alan adını 'yorum' yerine 'icerik' olarak değiştirin
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.icerik

