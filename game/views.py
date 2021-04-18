from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'game/index.html')


def day_archive(request, day):
    print(request, day)
    return render(request, 'game/indexday.html')
