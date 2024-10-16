// script.js

// Ouvre le panneau latéral
document.getElementById("hamburger").onclick = function() {
    document.getElementById("side-panel").style.width = "100%";
}

// Ferme le panneau latéral
document.getElementById("close-btn").onclick = function() {
    document.getElementById("side-panel").style.width = "0";
}



// Gérer l'ouverture des sous-menus
const dropdownLinks = document.querySelectorAll('.nav-links > li > a');

dropdownLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        const parentLi = this.parentElement;
        const dropdown = parentLi.querySelector('.dropdown');
        
        if (dropdown) {
            e.preventDefault(); // Empêche le lien de rediriger
            parentLi.classList.toggle('active'); // Active ou désactive l'état
            dropdown.classList.toggle('show'); // Affiche ou masque le sous-menu
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Sélectionner les liens du menu dans le header
    const headerNavLinks = document.querySelector('#nav-links').innerHTML;

    // Sélectionner l'élément dans lequel on veut copier les liens (dans le panneau latéral)
    const sideNavLinks = document.querySelector('#side-nav-links');

    // Copier le contenu des liens du header dans le panneau latéral
    sideNavLinks.innerHTML = headerNavLinks;
});

document.querySelectorAll('.side-panel .nav-links li a').forEach(link => {
    link.addEventListener('click', function (e) {
        const dropdown = this.nextElementSibling;
        if (dropdown && dropdown.classList.contains('dropdown')) {
            e.preventDefault();
            dropdown.classList.toggle('active');
        }
    });
});

