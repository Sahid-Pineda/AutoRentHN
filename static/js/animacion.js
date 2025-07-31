document.addEventListener("DOMContentLoaded", () => {
  const title = document.getElementById("title");
  const originalText = "AutoRentHN";

  // Limpiar contenido
  title.innerHTML = "";

  const highlightStart = 4; // "RentHN" empieza en el índice 4

  originalText.split("").forEach((char, i) => {
    const span = document.createElement("span");
    span.classList.add("letter");
    if (i >= highlightStart) {
      span.classList.add("text-cyan-500");
    }
    span.textContent = char;
    title.appendChild(span);
  });

  anime({
    targets: "#title .letter",
    translateY: [
      { value: "-2rem", duration: 300, easing: "easeOutExpo" },
      { value: "0", duration: 500, easing: "easeOutBounce", delay: 100 },
    ],
    rotate: {
      from: "-1turn",
      delay: 0,
    },
    delay: anime.stagger(100),
    loop: false,
    loopDelay: 1000,
  });
});

document.addEventListener("DOMContentLoaded", () => {
  tsParticles.load("tsparticles", {
    background: { color: "#0f172a" },
    particles: {
      color: { value: "#38bdf8" },
      links: { enable: true, distance: 120, color: "#38bdf8" },
      move: { enable: true, speed: 1 },
      number: { value: 60 },
      opacity: { value: 0.5 },
      size: { value: 3 },
    },
  });
});
