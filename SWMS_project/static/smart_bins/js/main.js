
let slideIndex = 0;
document.addEventListener("DOMContentLoaded", function () {
  const images = document.querySelectorAll(".hero-image-container img");
  let currentIndex = 0;

  function showNextImage() {
    images.forEach((img, index) => {
      img.classList.remove("active");
      if (index === currentIndex) {
        img.classList.add("active");
      }
    });

    currentIndex = (currentIndex + 1) % images.length;
  }

  if (images.length > 0) {
    showNextImage(); 
    setInterval(showNextImage, 4000); 
  }
});


function showSlides() {
  let slides = document.querySelectorAll('.hero-image-container img');

  slides.forEach((slide, i) => {
    slide.style.display = (i === slideIndex) ? 'block' : 'none';
  });

  slideIndex = (slideIndex + 1) % slides.length;
  setTimeout(showSlides, 3000); // Change image every 3 seconds
}

document.addEventListener('DOMContentLoaded', showSlides);

document.querySelectorAll('.fancy-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.boxShadow = '0 0 20px rgba(0, 168, 132, 0.4)';
  });
  card.addEventListener('mouseleave', () => {
    card.style.boxShadow = '0 10px 30px rgba(0, 168, 132, 0.25)';
  });
});

