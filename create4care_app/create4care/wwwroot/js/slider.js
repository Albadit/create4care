// wwwroot/js/slider‐init.js
window.initializeInstructionSlider = () => {
  const pages = [
    { image: 'images/step_1.png', title: 'Monteer de MeetMaatje', 
    content: 'Kies een stevige binnendeur en hang de haak van het meetapparaat goed over de bovenkant. Zorg dat de haak volledig vastzit en het apparaat recht naar beneden hangt.' },
    { image: 'images/step_2.png', title: 'Connect met MeetMaatje', 
    content: 'Zet Bluetooth aan op je smartphone of tablet en open de app. Selecteer het meetapparaat in de lijst met beschikbare apparaten en wacht tot de app bevestigt dat de koppeling gelukt is.' },
    { image: 'images/step_3.png', title: 'Kalibreer de MeetMaatje', 
    content: 'Volg de instructies in de app om het apparaat te kalibreren. Zorg dat er niemand onder staat. De kalibratie duurt slechts enkele seconden en zorgt voor een nauwkeurige meting.' },
    { image: 'images/step_4.png', title: 'Controleer het postuur via een foto', 
    content: 'Maak via de app een foto van het kind in meetpositie. Zorg dat het recht staat met kin vooruit, schouders ontspannen en voeten onder het lichaam. Pas de houding aan als dat nodig is.' }
];
  const fadeDuration = 500;
  const gapDuration = 100;
  const slidesContainer = document.querySelector('.slides');
  const indicatorsContainer = document.querySelector('.indicators');
  const prevBtn = document.getElementById('prev');
  const nextBtn = document.getElementById('next');
  let currentIndex = 0;

  // Build slides + indicators
  pages.forEach((page, i) => {
    const slide = document.createElement('div');
    slide.className = 'slide';
    slide.innerHTML = `
      <img src="${page.image}" alt="${page.title}">
      <h2>${page.title}</h2>
      <p>${page.content}</p>
    `;
    slidesContainer.appendChild(slide);
    const dot = document.createElement('div');
    dot.className = 'indicator';
    dot.addEventListener('click', () => transitionTo(i));
    indicatorsContainer.appendChild(dot);
  });

  const slides = slidesContainer.querySelectorAll('.slide');
  const dots = indicatorsContainer.querySelectorAll('.indicator');

  function updateButtons() {
    const atStart = currentIndex === 0;
    prevBtn.disabled = atStart;
    prevBtn.style.opacity = atStart ? '0' : '1';
    nextBtn.disabled = false;
    nextBtn.style.opacity = '1';
  }

  function transitionTo(nextIndex) {
    if (nextIndex < 0 || nextIndex >= pages.length || nextIndex === currentIndex) return;
    dots[currentIndex].classList.remove('active');
    dots[nextIndex].classList.add('active');
    const dir = nextIndex > currentIndex ? -20 : 20;

    slidesContainer.style.transition = `opacity ${fadeDuration}ms ease, transform ${fadeDuration}ms ease`;
    slidesContainer.style.opacity = '0';
    slidesContainer.style.transform = `translateX(${dir}px)`;
    prevBtn.disabled = nextBtn.disabled = true;

    if (currentIndex === 0 && nextIndex > 0) prevBtn.style.opacity = '1';
    else if (currentIndex >= 1 && nextIndex === 0) prevBtn.style.opacity = '0';

    setTimeout(() => {
      slides[currentIndex].classList.remove('active');
      currentIndex = nextIndex;
      slides[currentIndex].classList.add('active');

      slidesContainer.style.transition = 'none';
      slidesContainer.style.transform = `translateX(${-dir}px)`;
      slidesContainer.style.opacity = '0';

      setTimeout(() => {
        slidesContainer.style.transition = `opacity ${fadeDuration}ms ease, transform ${fadeDuration}ms ease`;
        slidesContainer.style.opacity = '1';
        slidesContainer.style.transform = 'translateX(0)';
        setTimeout(updateButtons, fadeDuration);
      }, gapDuration);
    }, fadeDuration);
  }

  nextBtn.addEventListener('click', () => {
    if (currentIndex === pages.length - 1) {
      window.location.href = '/measuring';
    } else {
      transitionTo(currentIndex + 1);
    }
  });
  prevBtn.addEventListener('click', () => transitionTo(currentIndex - 1));

  slides[currentIndex].classList.add('active');
  dots[currentIndex].classList.add('active');
  updateButtons();
};
