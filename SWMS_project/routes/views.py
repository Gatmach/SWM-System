from django.shortcuts import render
from django.http import JsonResponse
from .route_optimizer import optimize_route

def get_optimized_route(request):
    if request.method == 'POST':
        start = request.POST.get('start')  # Start point of the route
        end = request.POST.get('end')  # End point of the route
        locations = request.POST.getlist('locations')  # List of bin locations

        route, distance = optimize_route(start, end, locations)
        return JsonResponse({'route': route, 'distance': distance})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def route_dashboard(request):
    return render(request, 'routes/route_dashboard.html')
