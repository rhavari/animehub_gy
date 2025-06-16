/*!
* Start Bootstrap - One Page Wonder v6.0.6 (https://startbootstrap.com/theme/one-page-wonder)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-one-page-wonder/blob/master/LICENSE)
*/

document.addEventListener("DOMContentLoaded", () => {
    const follower = document.createElement("div");
    follower.id = "cursor-follower";
    document.body.appendChild(follower);
    
    let mouseX = 0, mouseY = 0;
    let currentX = 0, currentY = 0;
    
    document.addEventListener("mousemove", e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });
    
    function animate() {
      currentX += (mouseX - currentX) * 0.3;
      currentY += (mouseY - currentY) * 0.3;
      
      follower.style.left = currentX + "px";
      follower.style.top = currentY + "px";
      requestAnimationFrame(animate);
    }
    
    animate();
});

document.addEventListener("click", (e) => {
  const burst = document.createElement("span");
  burst.className = "click-burst";
  burst.style.left = `${e.clientX}px`;
  burst.style.top = `${e.clientY}px`;
  document.body.appendChild(burst);
  setTimeout(() => burst.remove(), 500);
});
      
