from django.shortcuts import render, HttpResponse

def heythere(request):
    return render(request, 'kevins_demo.html')


    return HttpResponse("Hey there!")