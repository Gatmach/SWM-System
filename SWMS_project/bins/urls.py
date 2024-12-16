from django.urls import path
from bins.views import home, dashboard, update_bin_status, about_us

urlpatterns = [
    path('', home, name='smart_bins_home'),  # Home page
    path('update-bin-status/', update_bin_status, name='update_bin_status'),
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard page URL
    path('about-us/', about_us, name='about_us'),  # Add the About Us page
]

