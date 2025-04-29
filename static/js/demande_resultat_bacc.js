// ✅ Fonction pour récupérer le CSRF Token (Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ✅ Exécuter après le chargement du DOM
document.addEventListener("DOMContentLoaded", function () {
  // Afficher l'année en cours dans l'interface
  document.getElementById("year").textContent = new Date().getFullYear();

  // Sélection des boutons radio pour le choix du programme
  document.querySelectorAll('input[name="programme"]').forEach((radio) => {
    radio.addEventListener("click", function () {
      // Récupérer les valeurs des champs du formulaire
      const matricule = document
        .querySelector('[name="matricule"]')
        .value.trim();
      const dateNaissance = document
        .querySelector('[name="date_naissance"]')
        .value.trim();
      const programme = this.value; // Programme sélectionné

      console.log("📌 Programme sélectionné:", programme);
      console.log("📌 Matricule:", matricule);
      console.log("📌 Date de naissance:", dateNaissance);

      // Vérifier si les champs sont bien remplis
      if (!matricule.match(/^\d{10}$/)) {
        alert("⚠️ Le matricule doit contenir exactement 10 chiffres.");
        return;
      }

      if (!dateNaissance) {
        alert("⚠️ Veuillez entrer votre date de naissance.");
        return;
      }

      // ✅ Envoi de la requête AJAX vers Django
      fetch("/api/demande-resultat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // Protection CSRF Django
        },
        body: JSON.stringify({
          matricule: matricule,
          date_naissance: dateNaissance,
          programme: programme,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          console.log("✅ Réponse reçue:", data);

          if (data.error) {
            alert(`❌ Erreur : ${data.error}`);
          } else {
            alert(
              `🎉 Résultat trouvé !\n\nNom: ${data.nom}\nMoyenne: ${data.moyenne}\nMention: ${data.mention}`
            );

            // Créer l'URL correcte
            const downloadLink = document.createElement("a");
            downloadLink.href = `/api/generate-csv/${matricule}/${dateNaissance}/${programme}/`; // Utilisation des paramètres dans l'URL
            downloadLink.textContent = "Télécharger les résultats (CSV)";
            downloadLink.classList.add("btn", "btn-info", "d-block", "mt-4");
            document
              .querySelector("#baccalaureat-form")
              .appendChild(downloadLink);
          }
        })

        .catch((error) => {
          console.error("❌ Erreur de requête:", error);
          alert(
            "⚠️ Une erreur est survenue lors de la récupération des résultats."
          );
        });
    });
  });
});
