from .models import Category

def menu_link(request): #dia buat fx. baru menu link .... menu_link= nama fx
    links = Category.objects.all()  #nak fecth all categories dari DATABASE----objects.all sebab die nak panggil semua kategori
    return dict(links=links) # dia akan return akan bawak semua Category list dan akan simpan dalam LINKs
