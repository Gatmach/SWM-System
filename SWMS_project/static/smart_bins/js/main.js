const images = document.querySelectorAll('.hero-image');
let currentIndex = 0;

// Show first image immediately
images[currentIndex].classList.add('active');

function showNextImage() {
  images[currentIndex].classList.remove('active');
  currentIndex = (currentIndex + 1) % images.length;
  images[currentIndex].classList.add('active');
}

// Cycle images every 5 seconds
setInterval(showNextImage, 5000);
