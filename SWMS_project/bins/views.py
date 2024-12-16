from django.shortcuts import render
from django.http import JsonResponse
from .utils import detect_bin_status
from notification.notifications import send_email_notification, send_sms_notification
from .models import WasteBin

def update_bin_status(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Save uploaded image to a temporary file
        image = request.FILES['image']
        image_path = f'/tmp/{image.name}'
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Detect bin status using OpenCV
        try:
            status = detect_bin_status(image_path)  # Ensure this returns a valid 'status'
        except Exception as e:
            return JsonResponse({'error': f'Error detecting bin status: {str(e)}'}, status=500)

        # Send notifications if bin is full
        if status == 'Full':
            send_email_notification('Some Location', status)
            send_sms_notification('Some Location', status)

        return JsonResponse({'status': status})  # Return the detected status

    return JsonResponse({'error': 'Invalid request'}, status=400)

def dashboard(request):
    bins = WasteBin.objects.all()  # Query all bins
    return render(request, 'bins/dashboard.html', {'bins': bins})

def home(request):
    return render(request, 'smart_bins/home.html')  # Updated template path

def about_us(request):
    return render(request, 'smart_bins/about_us.html')






