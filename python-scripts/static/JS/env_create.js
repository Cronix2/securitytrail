
const dropZone = document.getElementById('dropZone');
// je veux que ça fonctionne si je survole la page entière

document.body.addEventListener('dragover', (event) => {
    event.preventDefault();
    event.stopPropagation();
    dropZone.classList.add('drag-over'); // Ajoute l'effet visuel
});

document.body.addEventListener('drop', (event) => {
    event.preventDefault();
    event.stopPropagation();

    dropZone.classList.remove('drag-over'); // Retire l'effet visuel après le drop
    
    const file = event.dataTransfer.files[0];

    if (file) {
        validateEnvFile(file);
    }
});

document.body.addEventListener('dragleave', (event) => {
    if (!event.relatedTarget || !dropZone.contains(event.relatedTarget)) {
        dropZone.classList.remove('drag-over'); // Retire l'effet uniquement si la souris sort complètement
    }
});



document.getElementById("infoButton").addEventListener("click", function (event) {
    event.preventDefault(); // Empêche un éventuel comportement inattendu

    const tooltip = document.getElementById("tooltip");

    if (tooltip.style.display === "block") {
        tooltip.style.display = "none"; // Cache si déjà affiché
    } else {
        tooltip.style.display = "block"; // Affiche la bulle
        setTimeout(() => {
            tooltip.style.display = "none"; // La cache après 3 secondes
        }, 3000);
    }
});



document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Récupérer le fichier sélectionné
    if (file) {
        validateEnvFile(file); // Valide le fichier
    } else {
        createNotification("error", "Aucun fichier sélectionné !");
    }
});


function createNotification(type, message) {
    const container = document.getElementById("notificationsContainer");

    // Création de l'élément du bandeau
    const notification = document.createElement("div");
    notification.classList.add("notification-banner");

    // Définition du style en fonction du type (info, warning, error, success)
    switch (type) {
        case "info":
            notification.style.background = "#509AF8"; // Bleu
            break;
        case "warning":
            notification.style.background = "#F4C430"; // Jaune
            break;
        case "error":
            notification.style.background = "#E74C3C"; // Rouge
            break;
        case "success":
            notification.style.background = "#4CAF50"; // Vert
            break;
    }

    // Icône en fonction du type (mis à jour avec tes SVG)
    let iconSVG;
    if (type === "success") {
        iconSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                    <path fill="#ffffff" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/>
                </svg>`;
    } else if (type === "error") {
        iconSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                    <path fill="#ffffff" d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24l0 112c0 13.3-10.7 24-24 24s-24-10.7-24-24l0-112c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/>
                </svg>`;
    } else if (type === "warning") {
        iconSVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                    <path fill="#ffffff" d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480L40 480c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24l0 112c0 13.3 10.7 24 24 24s24-10.7 24-24l0-112c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z"/>
                </svg>`;
    } else {
        iconSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path fill="#ffffff" d="M12 2.25C6.20156 2.25 1.5 6.95156 1.5 12.75C1.5 18.5484 6.20156 23.25 12 23.25C17.7984 23.25 22.5 18.5484 22.5 12.75C22.5 6.95156 17.7984 2.25 12 2.25ZM10.5 17.25L5.625 12.375L7.125 10.875L10.5 14.25L16.875 7.875L18.375 9.375L10.5 17.25Z"></path>
                </svg>`;
    }

    // Contenu du bandeau
    notification.innerHTML = `
        <div class="notification-icon">${iconSVG}</div>
        <div class="notification-title">${message}</div>
        <div class="notification-close" onclick="removeNotification(this)">
            <svg height="20" width="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path d="m15.8333 5.34166-1.175-1.175-4.6583 4.65834-4.65833-4.65834-1.175 1.175 4.65833 4.65834-4.65833 4.6583 1.175 1.175 4.65833-4.6583 4.6583 4.6583 1.175-1.175-4.6583-4.6583z" fill="#ffffff"></path>
            </svg>
        </div>
    `;

    // Ajout du bandeau en haut de la pile
    container.insertBefore(notification, container.firstChild);
}

// Fonction pour supprimer un bandeau et faire remonter les autres
function removeNotification(closeButton) {
    const notification = closeButton.parentElement;
    notification.classList.add("slideout");

    // Supprime le bandeau après l'animation
    setTimeout(() => {
        notification.remove();
    }, 500);
}

// Gestion du bandeau d'information
document.addEventListener("DOMContentLoaded", function () {
    const infoBanner = document.getElementById("infoBanner");
    const closeBanner = document.getElementById("closeBanner");

    setTimeout(() => { infoBanner.classList.add("slideout");}, 10000);

    closeBanner.addEventListener("click", () => {infoBanner.classList.add("slideout");});
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/info-env")
        .then(response => {
            if (!response.ok) {
                createNotification("warning", "Aucun fichier .env trouvé, veuillez en créer un.");
                throw new Error("Fichier .env introuvable");
            }
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                const envValues = data[0]; // Récupérer le premier objet du tableau

                // Vérifie si les clés existent et met à jour les placeholders
                if (envValues.API_KEY) {
                    document.getElementById("apiKey").placeholder = envValues.API_KEY;
                }
                if (envValues.DB_USER) {
                    document.getElementById("dbUser").placeholder = envValues.DB_USER;
                }
                if (envValues.DB_PASSWORD) {
                    document.getElementById("dbPassword").placeholder = envValues.DB_PASSWORD;
                }
                if (envValues.DB_HOST) {
                    document.getElementById("dbHost").placeholder = envValues.DB_HOST;
                }
            }
        })
        .catch(error => {
            console.warn("Impossible de récupérer le fichier .env :", error);
        });
});

document.getElementById("toggleApiKey").addEventListener("click", function () {
    const apiKeyInput = document.getElementById("apiKey");
    const eyeIcon = document.getElementById("toggleApiKey");

    if (apiKeyInput.type === "password") {
        apiKeyInput.type = "text"; // Montre la clé API
        eyeIcon.innerHTML = `
            <path d="M1 12C2.5 7 7 3.5 12 3.5C17 3.5 21.5 7 23 12C21.5 17 17 20.5 12 20.5C7 20.5 2.5 17 1 12Z" stroke="#ffffff" stroke-width="2"></path>
            <circle cx="12" cy="12" r="3" stroke="#ffffff" stroke-width="2"></circle>
            <path d="M3 3L21 21" stroke="#ffffff" stroke-width="2"></path>
        `; // Icône barrée
    } else {
        apiKeyInput.type = "password"; // Cache la clé API
        eyeIcon.innerHTML = `
            <path d="M1 12C2.5 7 7 3.5 12 3.5C17 3.5 21.5 7 23 12C21.5 17 17 20.5 12 20.5C7 20.5 2.5 17 1 12Z" stroke="#ffffff" stroke-width="2"></path>
            <circle cx="12" cy="12" r="3" stroke="#ffffff" stroke-width="2"></circle>
        `; // Icône ouverte
    }
});

document.getElementById("togglepassword").addEventListener("click", function () {
    const passwordInput = document.getElementById("dbPassword");
    const eyeIcon = document.getElementById("togglepassword");

    if (passwordInput.type === "password") {
        passwordInput.type = "text"; // Affiche le mot de passe
        eyeIcon.innerHTML = `
            <path d="M1 12C2.5 7 7 3.5 12 3.5C17 3.5 21.5 7 23 12C21.5 17 17 20.5 12 20.5C7 20.5 2.5 17 1 12Z" stroke="#ffffff" stroke-width="2"></path>
            <circle cx="12" cy="12" r="3" stroke="#ffffff" stroke-width="2"></circle>
            <line x1="3" y1="3" x2="21" y2="21" stroke="#ffffff" stroke-width="2"></line>
        `; // Icône barrée
    } else {
        passwordInput.type = "password"; // Cache le mot de passe
        eyeIcon.innerHTML = `
            <path d="M1 12C2.5 7 7 3.5 12 3.5C17 3.5 21.5 7 23 12C21.5 17 17 20.5 12 20.5C7 20.5 2.5 17 1 12Z" stroke="#ffffff" stroke-width="2"></path>
            <circle cx="12" cy="12" r="3" stroke="#ffffff" stroke-width="2"></circle>
        `; // Icône ouverte
    }
});



function generateEnvFile() {
    const apiKey = document.getElementById('apiKey');
    const dbUser = document.getElementById('dbUser');
    const dbPassword = document.getElementById('dbPassword');
    const dbHost = document.getElementById('dbHost');

    // Regex pour validation des champs
    const validRegex = /^[a-zA-Z0-9\s\-_,.@=]+$/;

    // Réinitialisation des erreurs
    let isValid = true;
    document.querySelectorAll('.error-message').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.input-container').forEach(el => el.classList.remove('input-error'));

    // Fonction pour afficher un message d'erreur sous un champ et ajouter la bordure rouge
    function showError(input, message) {
        isValid = false;
        const inputContainer = input.parentElement; // Récupère le parent contenant l'input
        inputContainer.classList.add('input-error'); // Ajoute la classe de bordure rouge
        const errorElement = inputContainer.nextElementSibling; // L'erreur est sous le conteneur
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    // Vérification des champs avec regex et présence
    if (apiKey.value.trim() === "" || !validRegex.test(apiKey.value)) {
        showError(apiKey, "Seuls les caractères alphanumériques et spéciaux classiques sont autorisés.");
        createNotification("error", "Une erreur s'est produite lors de la validation du champ API Key.");
    }
    if (dbUser.value.trim() === "" || !validRegex.test(dbUser.value)) {
        showError(dbUser, "Seuls les caractères alphanumériques et spéciaux classiques sont autorisés.");
        createNotification("error", "Une erreur s'est produite lors de la validation du champ Username.");
    }
    if (dbPassword.value.trim() === "" || !validRegex.test(dbPassword.value)) {
        showError(dbPassword, "Seuls les caractères alphanumériques et spéciaux classiques sont autorisés.");
        createNotification("error", "Une erreur s'est produite lors de la validation du champ Password.");
    }
    if (dbHost.value.trim() === "" || !validRegex.test(dbHost.value)) {
        showError(dbHost, "Seuls les caractères alphanumériques et spéciaux classiques sont autorisés.");
        createNotification("error", "Une erreur s'est produite lors de la validation du champ Host.");
    }

    // Si toutes les valeurs sont valides, on génère le fichier
    if (isValid) {
        const envContent = `API_KEY=\"${apiKey.value}\"\nDB_USER=\"${dbUser.value}\"\nDB_PASSWORD=\"${dbPassword.value}\"\nDB_HOST=\"${dbHost.value}\"`;

        const blob = new Blob([envContent], { type: 'text/plain' });
        const formData = new FormData();
        formData.append("env_file", blob, ".env");
        try {
            createNotification("info", "Envoi du fichier .env en cours...");
            sendFileToServer(formData.get("env_file"));
            createNotification("success", "Fichier .env généré avec succès !");
        } catch (error) {
            console.error("Erreur lors de l'envoi du fichier : ", error);
        }
    }
}




function validateEnvFile(file) {
    const fileStatusIcon = document.getElementById('fileStatusIcon');
    const errorMessage = document.getElementById('errorMessage');
    fileStatusIcon.innerHTML = '';
    errorMessage.textContent = '';
    
    if (!file) {
        console.error("Aucun fichier fourni à validateEnvFile !");
        createNotification("error", "Aucun fichier fourni à validateEnvFile !");
        return;
    }

    // Renommer le fichier s'il n'est pas nommé correctement
    const renamedFile = new File([file], ".env", { type: file.type });
    file = renamedFile;
    
    const reader = new FileReader();
    reader.onload = function(event) {
        const lines = event.target.result.split("\n");
        if (lines.length !== 4) {
            errorMessage.style.color = "red";
            fileStatusIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="red" stroke-width="2" fill="none" /><line x1="8" y1="8" x2="16" y2="16" stroke="red" stroke-width="2" /><line x1="16" y1="8" x2="8" y2="16" stroke="red" stroke-width="2" /></svg>';
            errorMessage.textContent = "Le fichier doit contenir exactement 4 lignes.";
            createNotification("error", "Le fichier ne convient pas aux éxigences.");
            return;
        }
        const regex = /^[a-zA-Z0-9\s\-_,.=@"]+$/;
        const expectedKeys = ["API_KEY=", "DB_USER=", "DB_PASSWORD=", "DB_HOST="];
        for (let i = 0; i < 4; i++) {
            if (!lines[i].startsWith(expectedKeys[i])){
                errorMessage.style.color = "red";
                fileStatusIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="red" stroke-width="2" fill="none" /><line x1="8" y1="8" x2="16" y2="16" stroke="red" stroke-width="2" /><line x1="16" y1="8" x2="8" y2="16" stroke="red" stroke-width="2" /></svg>';
                errorMessage.textContent = "Format incorrect à la ligne " + (i + 1) + " erreur 1";
                createNotification("error", "Le fichier ne convient pas aux éxigences.");
                return;
            }
            if (lines[i].length > 200){
                errorMessage.style.color = "red";
                fileStatusIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="red" stroke-width="2" fill="none" /><line x1="8" y1="8" x2="16" y2="16" stroke="red" stroke-width="2" /><line x1="16" y1="8" x2="8" y2="16" stroke="red" stroke-width="2" /></svg>';
                errorMessage.textContent = "Format incorrect à la ligne " + (i + 1) + " erreur 2";
                createNotification("error", "Le fichier ne convient pas aux éxigences.");
                return;
            }
            if (!regex.test(lines[i].substring(expectedKeys[i].length))) {
                errorMessage.style.color = "red";
                fileStatusIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="red" stroke-width="2" fill="none" /><line x1="8" y1="8" x2="16" y2="16" stroke="red" stroke-width="2" /><line x1="16" y1="8" x2="8" y2="16" stroke="red" stroke-width="2" /></svg>';
                errorMessage.textContent = "Format incorrect à la ligne " + (i + 1) + " erreur 3";
                createNotification("error", "Le fichier ne convient pas aux éxigences.");
                return;
            }
        }
        sendFileToServer(file);
        fileStatusIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="green" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="green" stroke-width="2" fill="none" /><path d="M8 12l3 3l5 -5" stroke="green" stroke-width="2" fill="none" /></svg>';
        errorMessage.textContent = "Fichier .env valide !";
        errorMessage.style.color = "green";
        createNotification("success", "Le fichier .env est valide !");
    };
    reader.readAsText(file);
}



function sendFileToServer(file) {
    const formData = new FormData();
    formData.append('file', file);

    console.log("Envoi du fichier : ", file.name);

    fetch('/upload-env', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        mainContainer.classList.add("success-effect");
        
        // Supprime l'effet après 3 secondes
        setTimeout(() => {
            mainContainer.classList.remove("success-effect");
        }, 10000);
        console.log(data.message);
        document.getElementById('errorMessage').textContent = data.message;
    })
    .catch(error => console.error('Error:', error));
}



document.getElementById("closeBanner").addEventListener("click", function () {
    document.getElementById("infoBanner").classList.add("slideout");
    setTimeout(() => {
        document.getElementById("infoBanner").classList.add("hidden");
    }, 800);
});

document.getElementById("closeWarning").addEventListener("click", function () {
    document.getElementById("warningBanner").classList.add("slideout");
    setTimeout(() => {
        document.getElementById("warningBanner").classList.add("hidden");
    }, 800);
});

document.getElementById("closeError").addEventListener("click", function () {
    document.getElementById("errorBanner").classList.add("slideout");
    setTimeout(() => {
        document.getElementById("errorBanner").classList.add("hidden");
    }, 800);
});

document.getElementById("closeSuccess").addEventListener("click", function () {
    document.getElementById("successBanner").classList.add("slideout");
    setTimeout(() => {
        document.getElementById("successBanner").classList.add("hidden");
    }, 800);
});
