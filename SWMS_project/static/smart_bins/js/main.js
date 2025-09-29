// ===================== INITIALIZATION =====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM fully loaded - initializing SmartBin system...');
    
    // Initialize all components
    initAllComponents();
    
    // Fallback check for counters
    setTimeout(() => {
        const firstMetric = document.querySelector('.metric-data');
        if (firstMetric && firstMetric.textContent === '0%') {
            console.log('🔄 Primary counter method may need fallback...');
            initMetricCountersSimple();
        }
    }, 4000);
});

function initAllComponents() {
    console.log('🔧 Initializing all components...');
    initBackgroundSlider();
    initMetricCounters();
    initBinDemo();
    initUploadAndCamera();
    initDashboard();
}

// ===================== BACKGROUND IMAGE SLIDER =====================
function initBackgroundSlider() {
    const bgImages = document.querySelectorAll('.hero-bg-image');
    let currentImage = 0;

    function changeBackgroundImage() {
        bgImages.forEach(img => img.classList.remove('active'));
        bgImages[currentImage].classList.add('active');
        currentImage = (currentImage + 1) % bgImages.length;
    }

    if (bgImages.length > 0) {
        bgImages[0].classList.add('active');
        currentImage = 1;
        setInterval(changeBackgroundImage, 5000);
        console.log('🎨 Background slider initialized');
    }
}

// ===================== METRIC COUNTERS =====================
function initMetricCounters() {
    const metricElements = document.querySelectorAll('.metric-data');
    console.log('🔢 Found metric elements:', metricElements.length);
    
    if (metricElements.length === 0) {
        console.error('❌ No .metric-data elements found');
        return;
    }
    
    // Reset all to 0%
    metricElements.forEach(metric => {
        metric.textContent = '0%';
        metric.classList.remove('animated');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const metricData = entry.target;
                const targetValue = parseInt(metricData.getAttribute('data-value'));
                console.log('👀 Element in viewport, animating to:', targetValue + '%');
                
                animateMetricValue(metricData, 0, targetValue, 2000);
                observer.unobserve(metricData);
            }
        });
    }, { 
        threshold: 0.3,
        rootMargin: '0px 0px -100px 0px'
    });
    
    metricElements.forEach(metric => {
        observer.observe(metric);
    });
}

function animateMetricValue(element, start, end, duration) {
    let startTime = null;
    
    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const progress = Math.min((timestamp - startTime) / duration, 1);
        
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const value = Math.floor(easeOut * (end - start) + start);
        
        element.textContent = value + '%';
        
        // Visual feedback
        element.style.opacity = 0.7 + (0.3 * progress);
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.style.opacity = '1';
            element.classList.add('animated');
            console.log('✅ Counter completed:', end + '%');
        }
    }
    
    window.requestAnimationFrame(step);
}

// Simple fallback counter
function initMetricCountersSimple() {
    const metricElements = document.querySelectorAll('.metric-data');
    console.log('🔄 Using simple counter method');
    
    metricElements.forEach((element, index) => {
        const targetValue = parseInt(element.getAttribute('data-value'));
        let currentValue = 0;
        const stepTime = 1500 / targetValue;
        
        const counter = setInterval(() => {
            currentValue += 1;
            element.textContent = currentValue + '%';
            
            if (currentValue >= targetValue) {
                element.classList.add('animated');
                clearInterval(counter);
            }
        }, stepTime);
    });
}

// Enhanced Interactive Bin Demo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🗑️ Initializing Smart Bin Demo...');
    
    // DOM Elements
    const wasteLevel = document.querySelector('.waste-level');
    const fillLevelText = document.querySelector('.fill-level');
    const lastEmptiedText = document.querySelector('.last-emptied');
    const statusAlert = document.getElementById('statusAlert');
    const buttons = document.querySelectorAll('.control-btn');
    
    // State Management
    let currentLevel = 50;
    let lastEmptied = new Date(Date.now() - (2 * 24 * 60 * 60 * 1000));
    let alertActive = false;
    
    // Configuration
    const config = {
        alertThreshold: 80,
        criticalThreshold: 90,
        emptyThreshold: 10,
        animationSpeed: 500,
        alertDuration: 3000
    };
    
    // Initialize
    updateDisplay();
    
    // Event Listeners
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.getAttribute('data-action');
            handleAction(action);
        });
    });
    
    // Core Functions
    function handleAction(action) {
        switch(action) {
            case 'increase':
                currentLevel = Math.min(currentLevel + 15, 100);
                break;
            case 'decrease':
                currentLevel = Math.max(currentLevel - 15, 0);
                if (currentLevel <= config.emptyThreshold) {
                    lastEmptied = new Date();
                }
                break;
            case 'alert':
                triggerAlert();
                return;
            case 'reset':
                currentLevel = 50;
                lastEmptied = new Date(Date.now() - (2 * 24 * 60 * 60 * 1000));
                hideAlert();
                break;
        }
        
        updateDisplay();
        checkAlerts();
    }
    
    function updateDisplay() {
        wasteLevel.style.height = currentLevel + '%';
        wasteLevel.style.background = getWasteColor();
        fillLevelText.textContent = `${currentLevel}% Full`;
        lastEmptiedText.textContent = `Last emptied: ${formatLastEmptied()}`;
    }
    
    function getWasteColor() {
        if (currentLevel >= config.criticalThreshold) return 'linear-gradient(to top, #c0392b, #e74c3c)';
        if (currentLevel >= config.alertThreshold) return 'linear-gradient(to top, #d35400, #f39c12)';
        if (currentLevel > 30) return 'linear-gradient(to top, #27ae60, #2ecc71)';
        return 'linear-gradient(to top, #229954, #27ae60)';
    }
    
    function formatLastEmptied() {
        const now = new Date();
        const diffMs = now - lastEmptied;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        
        if (diffDays === 0 && diffHours === 0) return 'Just now';
        if (diffDays === 0) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
        if (diffDays === 1) return '1 day ago';
        return `${diffDays} days ago`;
    }
    
    function checkAlerts() {
        if (currentLevel >= config.criticalThreshold) {
            showAlert('🚨 CRITICAL: Bin is almost full! Immediate collection needed!', 'critical');
        } else if (currentLevel >= config.alertThreshold) {
            showAlert('⚠️ Alert: Bin is getting full. Schedule collection soon.', 'warning');
        } else {
            hideAlert();
        }
    }
    
    function triggerAlert() {
        let message, type;
        
        if (currentLevel >= config.criticalThreshold) {
            message = '🚨 EMERGENCY ALERT: Bin overflow imminent!';
            type = 'critical';
        } else if (currentLevel >= config.alertThreshold) {
            message = '⚠️ ALERT: Bin requires attention';
            type = 'warning';
        } else {
            message = 'ℹ️ Bin status is normal';
            type = 'info';
        }
        
        showAlert(message, type);
    }
    
    function showAlert(message, type) {
        statusAlert.textContent = message;
        statusAlert.style.display = 'block';
        
        switch(type) {
            case 'critical':
                statusAlert.style.background = '#e74c3c';
                break;
            case 'warning':
                statusAlert.style.background = '#f39c12';
                break;
            case 'info':
                statusAlert.style.background = '#3498db';
                break;
        }
        
        alertActive = true;
        
        if (type !== 'critical') {
            setTimeout(() => {
                if (alertActive) hideAlert();
            }, config.alertDuration);
        }
    }
    
    function hideAlert() {
        statusAlert.style.display = 'none';
        alertActive = false;
    }
    
    console.log('🗑️ Smart Bin Demo initialized successfully!');
});
// ===================== FILE UPLOAD & CAMERA =====================
function initUploadAndCamera() {
    const uploadTab = document.getElementById('upload-tab');
    const cameraTab = document.getElementById('camera-tab');
    
    if (!uploadTab || !cameraTab) {
        console.log('📷 Upload/camera tabs not found');
        return;
    }

    const uploadContent = document.getElementById('upload-content');
    const cameraContent = document.getElementById('camera-content');
    const fileInput = document.getElementById('image-upload');
    const dropZone = document.getElementById('drop-zone');
    const selectedFile = document.getElementById('selected-file');
    const analyzeBtn = document.getElementById('analyze-btn');
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-btn');
    const retakeBtn = document.getElementById('retake-btn');
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    
    let stream = null;

    // Tab switching
    uploadTab.addEventListener('click', () => switchTab('upload'));
    cameraTab.addEventListener('click', () => switchTab('camera'));

    function switchTab(tab) {
        if (tab === 'upload') {
            uploadTab.classList.add('active');
            cameraTab.classList.remove('active');
            uploadContent.classList.remove('hidden');
            cameraContent.classList.add('hidden');
        } else {
            cameraTab.classList.add('active');
            uploadTab.classList.remove('active');
            cameraContent.classList.remove('hidden');
            uploadContent.classList.add('hidden');
        }
    }

    // File handling
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }

    function handleFileSelect() {
        if (this.files.length > 0) {
            selectedFile.textContent = this.files[0].name;
            if (analyzeBtn) analyzeBtn.disabled = false;
        }
    }

    // Drag and drop
    if (dropZone) {
        dropZone.addEventListener('dragover', e => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });
        
        dropZone.addEventListener('drop', e => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                selectedFile.textContent = e.dataTransfer.files[0].name;
                if (analyzeBtn) analyzeBtn.disabled = false;
            }
        });
    }

    // Camera functionality
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', startCamera);
    }
    
    if (captureBtn) {
        captureBtn.addEventListener('click', captureImage);
    }
    
    if (retakeBtn) {
        retakeBtn.addEventListener('click', retakePhoto);
    }

    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            startCameraBtn.classList.add('hidden');
            captureBtn.classList.remove('hidden');
        } catch (err) {
            alert('Error accessing camera: ' + err.message);
        }
    }

    function captureImage() {
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        
        captureBtn.classList.add('hidden');
        retakeBtn.classList.remove('hidden');
    }

    function retakePhoto() {
        retakeBtn.classList.add('hidden');
        startCameraBtn.classList.remove('hidden');
        if (selectedFile) selectedFile.textContent = '';
        if (analyzeBtn) analyzeBtn.disabled = true;
    }
    
    console.log('📷 Upload/camera system initialized');
}

// ===================== DASHBOARD & MAPS =====================
let map;
let directionsService;
let directionsRenderer;
let binMarkers = [];
let vehicleMarkers = [];
let liveTrackingInterval;
let isTracking = false;

function initDashboard() {
    if (!document.getElementById('map')) {
        console.log('🗺️ Map container not found - skipping dashboard');
        return;
    }
    
    console.log('📊 Initializing dashboard...');
    initMap();
    initCharts();
    setupEventListeners();
    loadDashboardData();
    startDataUpdates();
}

function setupEventListeners() {
    // Route optimization
    const recalcBtn = document.getElementById('recalcBtn');
    if (recalcBtn) {
        recalcBtn.addEventListener('click', recalculateRoutes);
    }
    
    // Live tracking
    const trackBtn = document.getElementById('trackBtn');
    if (trackBtn) {
        trackBtn.addEventListener('click', toggleLiveTracking);
    }
    
    // Map controls
    const viewAll = document.getElementById('view-all');
    const viewCritical = document.getElementById('view-critical');
    const viewRoute = document.getElementById('view-route');
    
    if (viewAll) viewAll.addEventListener('click', () => filterBins('all'));
    if (viewCritical) viewCritical.addEventListener('click', () => filterBins('critical'));
    if (viewRoute) viewRoute.addEventListener('click', showOptimalRoute);
}

function initMap() {
    const defaultCenter = { lat: 40.7128, lng: -74.0060 };
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: defaultCenter,
        mapTypeControl: true,
        streetViewControl: false,
        styles: [{ featureType: 'poi', stylers: [{ visibility: 'off' }] }]
    });
    
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true,
        polylineOptions: {
            strokeColor: '#2E86AB',
            strokeOpacity: 0.8,
            strokeWeight: 5
        }
    });
    
    loadBinData();
    console.log('🗺️ Google Maps initialized');
}

function loadBinData() {
    const binData = [
        { id: 1, lat: 40.7128, lng: -74.0060, status: 'critical', capacity: 95, address: '123 Main St' },
        { id: 2, lat: 40.7218, lng: -74.0160, status: 'warning', capacity: 78, address: '456 Oak Ave' },
        { id: 3, lat: 40.7028, lng: -74.0110, status: 'normal', capacity: 45, address: '789 Pine St' },
        { id: 4, lat: 40.7328, lng: -74.0260, status: 'critical', capacity: 92, address: '321 Elm St' },
        { id: 5, lat: 40.6928, lng: -74.0210, status: 'normal', capacity: 35, address: '654 Maple Ave' }
    ];
    
    binData.forEach(bin => addBinToMap(bin));
    calculateOptimalRoute(binData);
}

function addBinToMap(bin) {
    const icon = {
        url: getBinIcon(bin.status),
        scaledSize: new google.maps.Size(30, 30),
        anchor: new google.maps.Point(15, 15)
    };
    
    const marker = new google.maps.Marker({
        position: { lat: bin.lat, lng: bin.lng },
        map: map,
        icon: icon,
        title: `Bin #${bin.id} - ${bin.status}`
    });
    
    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div class="bin-info-window">
                <h6>Smart Bin #${bin.id}</h6>
                <p><strong>Status:</strong> <span class="status-${bin.status}">${bin.status.toUpperCase()}</span></p>
                <p><strong>Capacity:</strong> ${bin.capacity}%</p>
                <p><strong>Address:</strong> ${bin.address}</p>
                <button class="btn btn-sm btn-primary mt-2" onclick="focusOnBin(${bin.id})">Focus</button>
            </div>
        `
    });
    
    marker.addListener('click', () => infoWindow.open(map, marker));
    binMarkers.push({ marker, bin, infoWindow });
}

function getBinIcon(status) {
    const colors = { critical: '#C73E1D', warning: '#F18F01', normal: '#1F9C6B' };
    
    const svg = `
        <svg width="30" height="30" xmlns="http://www.w3.org/2000/svg">
            <circle cx="15" cy="15" r="12" fill="${colors[status]}" stroke="white" stroke-width="2"/>
            <text x="15" y="20" text-anchor="middle" fill="white" font-size="12">♻</text>
        </svg>
    `;
    
    return 'data:image/svg+xml;base64,' + btoa(svg);
}

function calculateOptimalRoute(bins) {
    const prioritizedBins = [...bins].sort((a, b) => {
        const priority = { critical: 3, warning: 2, normal: 1 };
        return priority[b.status] - priority[a.status];
    });
    
    const routeBins = prioritizedBins.filter(bin => bin.status !== 'normal').slice(0, 5);
    if (routeBins.length === 0) return;
    
    const depot = { lat: 40.7058, lng: -74.0080 };
    const waypoints = routeBins.map(bin => ({
        location: { lat: bin.lat, lng: bin.lng },
        stopover: true
    }));
    
    const request = {
        origin: depot,
        destination: depot,
        waypoints: waypoints,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING
    };
    
    directionsService.route(request, (result, status) => {
        if (status === 'OK') {
            directionsRenderer.setDirections(result);
            updateRouteStats(result);
        }
    });
}

function updateRouteStats(routeResult) {
    const route = routeResult.routes[0];
    const legs = route.legs;
    
    let totalDistance = 0;
    let totalDuration = 0;
    
    legs.forEach(leg => {
        totalDistance += leg.distance.value;
        totalDuration += leg.duration.value;
    });
    
    const distanceKm = (totalDistance / 1000).toFixed(1);
    const durationHours = (totalDuration / 3600).toFixed(1);
    const fuelSaved = calculateFuelSavings(distanceKm);
    
    updateElementText('total-distance', `${distanceKm} km`);
    updateElementText('estimated-time', `${durationHours} hrs`);
    updateElementText('fuel-savings', `${fuelSaved.percentage}%`);
    updateElementText('co2-reduction', `${calculateCO2Reduction(distanceKm)} kg`);
}

function calculateFuelSavings(distance) {
    const previousAvgConsumption = 0.15;
    const optimizedConsumption = 0.12;
    const previousFuel = distance * previousAvgConsumption;
    const optimizedFuel = distance * optimizedConsumption;
    const savings = ((previousFuel - optimizedFuel) / previousFuel) * 100;
    
    return {
        percentage: Math.round(savings),
        liters: (previousFuel - optimizedFuel).toFixed(1)
    };
}

function calculateCO2Reduction(distance) {
    const fuelSaved = calculateFuelSavings(distance).liters;
    return (fuelSaved * 2.68).toFixed(1);
}

function updateElementText(id, text) {
    const element = document.getElementById(id);
    if (element) element.textContent = text;
}

// ===================== CHARTS =====================
function initCharts() {
    initEfficiencyChart();
    initFuelChart();
}

function initEfficiencyChart() {
    const ctx = document.getElementById('efficiency-chart')?.getContext('2d');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [72, 75, 78, 82, 85, 80, 83],
                borderColor: '#2E86AB',
                backgroundColor: 'rgba(46, 134, 171, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: getChartOptions()
    });
}

function initFuelChart() {
    const ctx = document.getElementById('fuel-chart')?.getContext('2d');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                data: [420, 380, 350, 320],
                backgroundColor: '#A23B72',
                borderRadius: 5
            }]
        },
        options: getChartOptions()
    });
}

function getChartOptions() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: { grid: { color: 'rgba(0, 0, 0, 0.05)' } },
            x: { grid: { display: false } }
        }
    };
}

// ===================== DASHBOARD FUNCTIONS =====================
function recalculateRoutes() {
    const btn = document.getElementById('recalcBtn');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Calculating...';
    btn.disabled = true;
    
    setTimeout(() => {
        const newData = {
            distance: (Math.random() * 5 + 30).toFixed(1),
            time: (Math.random() * 0.5 + 2.5).toFixed(1),
            fuelSavings: Math.floor(Math.random() * 5) + 20
        };
        
        updateOptimizationResults(newData);
        showNotification('Routes optimized successfully!', 'success');
        
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 2000);
}

function toggleLiveTracking() {
    const btn = document.getElementById('trackBtn');
    if (!btn) return;
    
    if (!isTracking) {
        isTracking = true;
        btn.innerHTML = '<i class="fas fa-stop me-2"></i> Stop Tracking';
        btn.classList.replace('btn-success', 'btn-danger');
        liveTrackingInterval = setInterval(updateLiveTracking, 5000);
        showNotification('Live tracking started', 'success');
    } else {
        isTracking = false;
        btn.innerHTML = '<i class="fas fa-satellite-dish me-2"></i> Start Tracking';
        btn.classList.replace('btn-danger', 'btn-success');
        clearInterval(liveTrackingInterval);
        showNotification('Live tracking stopped', 'info');
    }
}

function filterBins(filter) {
    binMarkers.forEach(({ marker, bin }) => {
        marker.setMap(filter === 'all' || bin.status === filter ? map : null);
    });
}

function showOptimalRoute() {
    directionsRenderer.setMap(map);
}

// ===================== UTILITY FUNCTIONS =====================
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function startDataUpdates() {
    setInterval(loadDashboardData, 30000);
}

function loadDashboardData() {
    // Simulate data loading
    console.log('📈 Updating dashboard data...');
}

// ===================== GLOBAL FUNCTIONS =====================
window.focusOnBin = function(binId) {
    const binMarker = binMarkers.find(marker => marker.bin.id === binId);
    if (binMarker) {
        map.panTo(binMarker.marker.getPosition());
        map.setZoom(16);
        binMarker.infoWindow.open(map, binMarker.marker);
    }
};

window.recalculateRoutes = recalculateRoutes;
window.toggleLiveTracking = toggleLiveTracking;

// ===================== DEBUG HELPERS =====================
window.debugCounters = function() {
    console.log('🔍 DEBUG: Manual counter test');
    const metrics = document.querySelectorAll('.metric-data');
    metrics.forEach((metric, index) => {
        const target = parseInt(metric.getAttribute('data-value'));
        console.log(`Metric ${index + 1}: target=${target}%, current=${metric.textContent}`);
    });
};

window.forceCounters = function() {
    console.log('⚡ FORCE: Starting counters manually');
    initMetricCountersSimple();
};