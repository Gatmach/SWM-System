import cv2
import numpy as np
from PIL import Image
import io

def is_valid_bin_image(image_path, confidence_threshold=0.6):
    """
    Determine if an image contains a recognizable waste bin
    Returns: (is_valid, confidence_score, message)
    """
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return False, 0.0, "Invalid image file"
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Check image quality metrics
        quality_score = assess_image_quality(image)
        if quality_score < 0.4:
            return False, quality_score, "Poor image quality - too blurry or dark"
        
        # 2. Detect geometric features that resemble bins
        bin_features_score = detect_bin_features(image)
        
        # 3. Check color distribution (bins often have specific colors)
        color_score = analyze_bin_colors(image)
        
        # 4. Look for circular/rectangular shapes (bin openings)
        shape_score = detect_bin_shapes(image)
        
        # 5. Edge detection for structural features
        edge_score = analyze_edges(image)
        
        # Combine scores with weights
        confidence_score = (
            quality_score * 0.1 +
            bin_features_score * 0.4 +
            color_score * 0.2 +
            shape_score * 0.2 +
            edge_score * 0.1
        )
        
        if confidence_score >= confidence_threshold:
            return True, confidence_score, "Image appears to contain a waste bin"
        else:
            return False, confidence_score, "Image doesn't appear to contain a recognizable waste bin"
            
    except Exception as e:
        return False, 0.0, f"Error processing image: {str(e)}"

def assess_image_quality(image):
    """Check if image is clear enough for analysis"""
    # Calculate image blurriness using Laplacian variance
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Check brightness
    brightness = np.mean(gray)
    
    # Normalize scores (higher is better)
    blur_score = min(fm / 100, 1.0)  # Assume 100 is good, cap at 1.0
    brightness_score = min(abs(brightness - 127) / 127, 1.0)  # Closer to middle gray is better
    
    return (blur_score + brightness_score) / 2

def detect_bin_features(image):
    """Detect features that are characteristic of waste bins"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Use HAAR cascade for object detection (you can train a custom one for bins)
    # For now, we'll use basic feature detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0.0
    
    # Look for large, regular shapes that might be bins
    large_contours = [c for c in contours if cv2.contourArea(c) > 1000]
    
    if not large_contours:
        return 0.0
    
    # Calculate regularity score based on contour properties
    regularity_scores = []
    for contour in large_contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Regular shapes have lower perimeter-to-area ratios
        if perimeter > 0:
            compactness = 4 * np.pi * area / (perimeter * perimeter)
            regularity_scores.append(compactness)
    
    if regularity_scores:
        return min(max(regularity_scores) * 2, 1.0)  # Scale to 0-1 range
    return 0.0

def analyze_bin_colors(image):
    """Check if image contains colors commonly found in waste bins"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Common bin colors: green, blue, gray, black
    color_ranges = [
        # Green bins (common for recycling)
        ([35, 50, 50], [85, 255, 255]),
        # Blue bins
        ([90, 50, 50], [130, 255, 255]),
        # Gray/black bins (dark colors)
        ([0, 0, 0], [180, 50, 150])
    ]
    
    total_pixels = image.shape[0] * image.shape[1]
    color_score = 0.0
    
    for lower, upper in color_ranges:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower, upper)
        colored_pixels = np.sum(mask > 0)
        color_ratio = colored_pixels / total_pixels
        
        if color_ratio > 0.1:  # At least 10% of image has bin colors
            color_score = max(color_score, min(color_ratio * 3, 1.0))
    
    return color_score

def detect_bin_shapes(image):
    """Look for circular or rectangular shapes that might be bin openings"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect circles (bin openings)
    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=50,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=100
    )
    
    circle_score = 0.0
    if circles is not None:
        circle_score = min(len(circles[0]) / 5, 1.0)  # Up to 5 circles max
    
    # Detect rectangles (bin structures)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rectangle_score = 0.0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Only consider large contours
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            if len(approx) == 4:  # Rectangle has 4 vertices
                rectangle_score = 0.5
                break
    
    return max(circle_score, rectangle_score)

def analyze_edges(image):
    """Analyze edge patterns characteristic of bins"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Calculate edge density
    edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
    
    # Bins typically have moderate edge density (not too busy, not too plain)
    if 0.05 < edge_density < 0.3:
        return 0.7
    else:
        return 0.2

def detect_bin_status(image_path):
    """
    Detect if a bin is full or empty using OpenCV
    Returns: 'Full' or 'Empty'
    """
    # First check if this is a valid bin image
    is_valid, confidence, message = is_valid_bin_image(image_path)
    
    if not is_valid:
        raise ValueError(f"Invalid bin image: {message} (confidence: {confidence:.2f})")
    
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Apply threshold to create a binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return "Empty"
    
    # Find the largest contour (assuming it's the bin)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Calculate the area of the largest contour
    area = cv2.contourArea(largest_contour)
    
    # Get the image area for comparison
    image_area = image.shape[0] * image.shape[1]
    
    # Calculate the percentage of the image occupied by the bin
    fill_percentage = (area / image_area) * 100
    
    # Determine status based on fill percentage
    if fill_percentage > 60:  # Adjust this threshold as needed
        return "Full"
    else:
        return "Empty"

def estimate_fill_percentage(image_path):
    """
    Estimate the fill percentage of a waste bin (0-100%)
    This is a more advanced version that tries to estimate actual fill level
    """
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            return 0
        
        # Convert to HSV color space for better color segmentation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for waste (adjust based on your bins)
        # These are example ranges - you'll need to calibrate them
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([20, 255, 255])
        
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])
        
        # Create masks for different waste colors
        mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
        mask_black = cv2.inRange(hsv, lower_black, upper_black)
        
        # Combine masks
        combined_mask = cv2.bitwise_or(mask_brown, mask_black)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours in the combined mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0
        
        # Calculate total area of waste
        waste_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Filter out small noise
                waste_area += area
        
        # Calculate percentage (you might need to adjust this based on your bin size)
        total_area = image.shape[0] * image.shape[1]
        fill_percentage = (waste_area / total_area) * 100
        
        # Cap at 100%
        return min(100, max(0, int(fill_percentage * 2)))  # Multiply by 2 for more visible results
        
    except Exception as e:
        print(f"Error estimating fill percentage: {e}")
        return 0

def estimate_fill_percentage_simple(image_path):
    """
    A simpler approach to estimate fill percentage
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return 0
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Calculate the percentage of white pixels (which represent waste)
    white_pixels = np.sum(thresh == 255)
    total_pixels = thresh.shape[0] * thresh.shape[1]
    
    fill_percentage = (white_pixels / total_pixels) * 100
    
    return min(100, int(fill_percentage * 1.5))  # Adjust multiplier as needed