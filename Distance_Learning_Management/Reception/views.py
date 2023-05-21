from django.shortcuts import render

# Create your views here.
def registerars_landing_page(request):
    return render(request, 'Reception/dashboard_for_reception_display_page.html')