from django.conf import settings

from django.shortcuts import render

def construction(request):
    """ Website Turn Off """
    construction_info = settings.CONSTRUCTION_INFO

    return render(request, 'construction.html',{'construction_info': construction_info} ,status=404)

def page_not_found_view(request, exception):
    if settings.CONSTRUCTION == True:
        return render(request, 'construction.html', status=404)
    else:
        return render(request, '404.html', status=404)

