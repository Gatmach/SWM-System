from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .utils import detect_bin_status, estimate_fill_percentage, estimate_fill_percentage_simple, is_valid_bin_image
from notification.notifications import send_email_notification, send_sms_notification
from .models import WasteBin
import json

def update_bin_status(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Save uploaded image to a temporary file
        image = request.FILES['image']
        image_path = f'/tmp/{image.name}'
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Get location from form if provided
        location = request.POST.get('location', 'Unknown Location')
        
        try:
            # Validate the image first
            is_valid, confidence, message = is_valid_bin_image(image_path)
            if not is_valid:
                return JsonResponse({
                    'error': message,
                    'confidence': confidence,
                    'valid_image': False
                }, status=400)
            
            # Process the image if valid
            status = detect_bin_status(image_path)
            
            # Try the advanced fill estimation first, fall back to simple if it fails
            try:
                fill_percentage = estimate_fill_percentage(image_path)
            except:
                fill_percentage = estimate_fill_percentage_simple(image_path)
                
        except Exception as e:
            return JsonResponse({'error': f'Error analyzing image: {str(e)}'}, status=500)
        
        # Create or update bin record
        bin_instance, created = WasteBin.objects.get_or_create(
            location=location,
            defaults={'status': status, 'fill_level': fill_percentage}
        )
        
        if not created:
            bin_instance.status = status
            bin_instance.fill_level = fill_percentage
            bin_instance.last_updated = timezone.now()
            bin_instance.save()
        
        # Send notifications if bin is full
        if status == 'Full' and fill_percentage >= 90:
            send_email_notification(location, f"Bin is {fill_percentage}% full")
            send_sms_notification(location, f"Bin is {fill_percentage}% full")
        
        # Return detailed analysis results
        return JsonResponse({
            'status': status,
            'fill_level': fill_percentage,
            'location': location,
            'bin_id': bin_instance.id if not created else 'new',
            'confidence': confidence,
            'valid_image': True,
            'message': 'Analysis completed successfully'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def dashboard(request):
    bins = WasteBin.objects.all().order_by('-last_updated')
    return render(request, 'bins/dashboard.html', {'bins': bins})

def home(request):
    return render(request, 'smart_bins/home.html')

def about_us(request):
    return render(request, 'smart_bins/about_us.html')