import heapq
import math
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# ------------------------
# ROUTE DASHBOARD VIEW
# ------------------------
def route_dashboard_view(request):
    context = {
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    }
    """Render the route optimization dashboard page"""
    return render(request, 'routes/route_dashboard.html', context)


# ------------------------
# HELPER FUNCTION
# ------------------------
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth"""
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


# ------------------------
# ROUTE OPTIMIZATION LOGIC
# ------------------------
def optimize_route_advanced(start_coords, bins_data):
    """
    Enhanced route optimization with real GPS coordinates and fill-level weighting
    """
    graph = {}
    all_nodes = [('start', start_coords[0], start_coords[1], 0)] + bins_data

    # Build weighted graph
    for i, (node_id, lat1, lon1, fill_level) in enumerate(all_nodes):
        graph[node_id] = {}
        for j, (other_id, lat2, lon2, other_fill) in enumerate(all_nodes):
            if i != j:
                distance = haversine_distance(lat1, lon1, lat2, lon2)
                weight = distance * (1 - (fill_level / 200))  # prioritize fuller bins
                graph[node_id][other_id] = weight

    # Dijkstra’s Algorithm
    distances = {node[0]: float("inf") for node in all_nodes}
    distances['start'] = 0
    previous = {node[0]: None for node in all_nodes}
    queue = [(0, 'start')]

    while queue:
        current_dist, current_node = heapq.heappop(queue)

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct optimal path (end at last bin)
    last_bin = bins_data[-1][0] if bins_data else "start"
    optimal_path = []
    current = last_bin
    while current:
        optimal_path.insert(0, current)
        current = previous[current]

    # Compute total distance along path
    total_distance = 0
    for i in range(len(optimal_path) - 1):
        total_distance += graph[optimal_path[i]][optimal_path[i + 1]]

    return optimal_path, total_distance


# ------------------------
# API ENDPOINT
# ------------------------
@method_decorator(csrf_exempt, name='dispatch')
class OptimizeRouteView(View):
    """API endpoint for route optimization"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            start_coords = data.get('start_coords')
            bins_data = data.get('bins_data')

            if not start_coords or not bins_data:
                return JsonResponse({'error': 'Missing required data'}, status=400)

            if len(start_coords) != 2:
                return JsonResponse({'error': 'Start coordinates must be [lat, lng]'}, status=400)

            for i, bin_data in enumerate(bins_data):
                if len(bin_data) != 4:
                    return JsonResponse({'error': f'Bin data {i} must be [id, lat, lng, fill_level]'}, status=400)

            # Run optimization
            optimal_path, total_distance = optimize_route_advanced(start_coords, bins_data)

            estimated_time = total_distance / 25 * 60  # avg speed 25 km/h
            fuel_saved = total_distance * 0.3  # 0.3 L/km savings

            return JsonResponse({
                'optimal_path': optimal_path,
                'total_distance': round(total_distance, 2),
                'estimated_time': round(estimated_time, 2),
                'fuel_saved': round(fuel_saved, 2),
                'co2_reduction': round(fuel_saved * 2.7, 2)  # 2.7kg CO2 per liter
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
