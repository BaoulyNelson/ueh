// Fonction pour récupérer le CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("year").textContent = new Date().getFullYear();
  
    document.querySelectorAll(".program").forEach((button) => {
      button.addEventListener("click", function () {
        const matricule = document.getElementById("matricule").value;
        const dateNaissance = document.getElementById("date-naissance").value;
        const programme = this.getAttribute("data-programme");
  
        if (matricule && dateNaissance) {
          fetch("/api/demande-resultat/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
              matricule: matricule,
              date_naissance: dateNaissance,
              programme: programme,
            }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.error) {
                alert(data.error);
              } else {
                alert(`Nom: ${data.nom}, Moyenne: ${data.moyenne}, Mention: ${data.mention}`);
              }
            })
            .catch((error) => console.error("Erreur:", error));
        } else {
          alert("Veuillez remplir tous les champs.");
        }
      });
    });
  });
  