<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<%@ page import="javax.sql.*" %>
<%@ page import="javax.naming.*" %>
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>
  	<link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
    <!-- Custom CSS -->
    <style>
        .container {
            max-width: 800px;
            position: relative;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            display: flex;
            align-items: center;
        }

        .registration-image {
            flex: 1;
            text-align: right;
        }

        .registration-image img {
            max-width: 100%;
        }

        .registration-image p {
            font-size: 14px;
        }

        .registration-form {
            flex: 1;
            padding-right: 20px;
        }

        .form-group-inline {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .form-group-inline .form-control {
            flex: 1;
        }
    </style>
        <style>
        .success-popup {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            justify-content: center;
            position: fixed;
            padding: 20px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            background-color: #fff;
            z-index: 9999;
        }
    </style>
    <style>
    a:active {
        background-color: lightgray;
        padding: 5px 10px; /* Ajusta los valores según tus preferencias */
        border-radius: 5px; /* Opcional: agrega bordes redondeados */
    }
	</style>
    <script>
        // Show success popup
        function showSuccessPopup() {
            const successPopup = document.getElementById('successPopup');
            successPopup.style.display = 'flex';
            // Hide the popup after 2 seconds
            setTimeout(function() {
                successPopup.style.display = 'none';
                // Redirect to another JSP page
                window.location.href = 'index.jsp';
            }, 2000);
        }
    </script>
</head>
<body>
	<div class="container mt-5">
	    <div class="registration-form">
	        <h1 style="font-size: 24px; font-weight: 400;">Crea una cuenta de GrowUp</h1>
	        <h2 class="mb-4" style="font-size: 16px; font-weight: normal;">Ir a Biblioteca Web Educativo</h2>
	        <form action="create.jsp" method="POST">
	            <div class="form-group-inline mb-3">
	                <input type="text" class="form-control" id="names" name="names" placeholder="Nombres" pattern="[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+" required title="Ingrese un nombre válido (solo letras y espacios)">
	                <input type="text" class="form-control" id="last_name" name="last_name" placeholder="Apellidos" pattern="[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+" required title="Ingrese apellidos válidos (solo letras y espacios)">
	            </div>
				<div class="form-group-inline mb-3">
				    <select class="form-control" id="type_document" name="type_document" required onchange="updateDocumentPattern()">
				        <option value="">Tipo de Documento</option>
				        <option value="DNI">DNI</option>
				        <option value="CNT">Carnet</option>
				        <option value="PPE">Pasaporte</option>
				    </select>
				    <input type="text" class="form-control" id="number_document" name="number_document" placeholder="Número de Documento" required title="Ingrese un número de documento válido" onblur="trimInput()">
				</div>
	            <div class="mb-3">
	                <label for="email" class="form-label">Email</label>
	                <input type="email" class="form-control" id="email" name="email" required>
	            </div>
	            <div class="mb-3">
	                <label for="cell_phone" class="form-label">Teléfono Celular</label>
	                <input type="text" class="form-control" id="cell_phone" name="cell_phone" pattern="\d{9}" required title="Ingrese un número de teléfono celular válido (mínimo 9 dígitos)">

	            </div>
	            <div class="mb-3">
	                <label for="rol" class="form-label">Rol</label>
	                <select class="form-select" id="rol" name="rol" required>
	                    <option value="ES">Estudiante</option>
	                    <option value="AP">Apoderado</option>
	                    <option value="PR">Profesor</option>
	                    <option value="PA">Personal</option>
	                </select>
	            </div>
		       <button type="submit" class="btn btn-primary">Registrar</button>
		        <a href="index.jsp" class="btn btn-secondary">Volver</a>            
		    </form>
		
		    <div id="successPopup" class="success-popup" style="display: none;">
		        <img src="https://img.freepik.com/vector-premium/gato-enojado-trabajando-ilustracion-ordenador-portatil_138676-305.jpg?w=360" alt="Success Icon">
		        <h4>Registro exitoso!</h4>
		        <p>La persona ha sido registrada correctamente.</p>
		    </div>
    </div>
    <div class="registration-image" style="margin-top: 20px;">
        <div style="text-align: center;">
            <img src="https://img.freepik.com/vector-premium/linda-mujer-leyo-ilustracion-dibujos-animados-libro_97231-2220.jpg" alt="Imagen de registro">
            <p style="margin-top: 10px;">Una cuenta. Todo GrowUp a tu disposición.</p>
        </div>
		<div style="position: absolute; bottom: -40px; left: 0;">
		    <div class="dropdown">
		        <a href="#" class="dropdown-toggle" id="languageDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false" style="text-decoration: none; color: black; font-size: 14px; padding: 5px;">Español (España)</a>
		        <ul class="dropdown-menu" aria-labelledby="languageDropdown">
		            <li><a class="dropdown-item" href="#" onclick="changeLanguage('Inglés')">Inglés</a></li>
		            <li><a class="dropdown-item" href="#" onclick="changeLanguage('Francés')">Francés</a></li>
		            <li><a class="dropdown-item" href="#" onclick="changeLanguage('Alemán')">Alemán</a></li>
		            <li><a class="dropdown-item" href="#" onclick="changeLanguage('Español (España)')">Español (España)</a></li>
		            <!-- Agrega más idiomas aquí -->
		        </ul>
		    </div>
		</div>
		<div style="position: absolute; bottom: -40px; right: 0;">
		    <a href="https://support.google.com/accounts?hl=es&p=account_iph" target="_blank" style="margin-right: 20px; text-decoration: none; color: black; font-size: 14px; padding: 5px;">Ayuda</a>
		    <a href="https://accounts.google.com/TOS?loc=PE&hl=es&privacy=true" target="_blank" style="margin-right: 20px; text-decoration: none; color: black; font-size: 14px; padding: 5px;">Privacidad</a>
		    <a href="https://accounts.google.com/TOS?loc=PE&hl=es" target="_blank" style="text-decoration: none; color: black; font-size: 14px; padding: 5px;">Términos</a>
		</div>
	</div>
</div>    
  
    <%!
    public void insertPerson(String names, String lastName, String typeDocument, String numberDocument, String email, String cellPhone, String rol) throws Exception {
	    // Establecer la conexión con la base de datos
	    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;";
	    String username = "sa";
	    String password = "miguelangel";
        Connection con = DriverManager.getConnection(url, username, password);

        // Preparar la consulta SQL para insertar los datos en la tabla "person"
        String query = "INSERT INTO dbo.person (names, last_name, type_document, number_document, email, cell_phone, rol) VALUES (?, ?, ?, ?, ?, ?, ?)";
        PreparedStatement pstmt = con.prepareStatement(query);
        pstmt.setString(1, names);
        pstmt.setString(2, lastName);
        pstmt.setString(3, typeDocument);
        pstmt.setString(4, numberDocument);
        pstmt.setString(5, email);
        pstmt.setString(6, cellPhone);
        pstmt.setString(7, rol);

        // Ejecutar la consulta
        pstmt.executeUpdate();

        pstmt.close();
        con.close();
    }
    %>

    <%
    try {
        if (request.getMethod().equals("POST")) {
            // Obtener los datos del formulario
            String names = request.getParameter("names");
            String lastName = request.getParameter("last_name");
            String typeDocument = request.getParameter("type_document");
            String numberDocument = request.getParameter("number_document");
            String email = request.getParameter("email");
            String cellPhone = request.getParameter("cell_phone");
            String rol = request.getParameter("rol");

            // Insertar los datos en la base de datos
            insertPerson(names, lastName, typeDocument, numberDocument, email, cellPhone, rol);
    %>
            <script>
                // Simulate form submission success
                showSuccessPopup();
            </script>
    <%
        }
    } catch (Exception e) {
        out.println("<p>Error: " + e.getMessage() + "</p>");
    }
    %>


    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>

<script>
    function changeLanguage(language) {
        const languageLink = document.getElementById('languageDropdown');
        languageLink.textContent = language;

        // Actualizar los textos en la página según el idioma seleccionado
        const languageStrings = {
            'Español (España)': {
                'createAccount': 'Crea una cuenta de GrowUp',
                'goToGoogleDrive': 'Ir a Google Drive',
                'firstName': 'Nombres',
                'lastName': 'Apellidos',
                'documentType': 'Tipo de Documento',
                'DNI': 'DNI',
                'Carnet': 'Carnet',
                'Pasaporte': 'Pasaporte',
                'email': 'Email',
                'cellPhone': 'Teléfono Celular',
                'rol': 'Rol',
                'student': 'Estudiante',
                'guardian': 'Apoderado',
                'teacher': 'Profesor',
                'staff': 'Personal',
                'registerButton': 'Registrar',
                'backButton': 'Volver',
                'successMessage': 'Registro exitoso!',
                'successPopupMessage': 'La persona ha sido registrada correctamente.',
                'accountDescription': 'Una cuenta. Todo GrowUp a tu disposición.',
                'helpLink': 'Ayuda',
                'privacyLink': 'Privacidad',
                'termsLink': 'Términos'     
            },
            'Inglés': {
                'createAccount': 'Create a GrowUp account',
                'goToGoogleDrive': 'Go to Google Drive',
                'firstName': 'First Names',
                'lastName': 'Last Names',
                'documentType': 'Document Type',
                'DNI': 'DNI',
                'Carnet': 'ID',
                'Pasaporte': 'Passport',
                'email': 'Email',
                'cellPhone': 'Cell Phone',
                'rol': 'Role',
                'student': 'Student',
                'guardian': 'Guardian',
                'teacher': 'Teacher',
                'staff': 'Staff',
                'registerButton': 'Register',
                'backButton': 'Back',
                'successMessage': 'Registration successful!',
                'successPopupMessage': 'The person has been registered successfully.',
                'accountDescription': 'One account. All of GrowUp at your fingertips.',
                'helpLink': 'Help',
                'privacyLink': 'Privacy',
                'termsLink': 'Terms'
            },
            'Francés': {
                'createAccount': 'Créez un compte GrowUp',
                'goToGoogleDrive': 'Accéder à Google Drive',
                'firstName': 'Prénoms',
                'lastName': 'Noms de famille',
                'documentType': 'Type de document',
                'DNI': 'Carte d\'identité',
                'Carnet': 'ID',
                'Pasaporte': 'Passeport',
                'email': 'Email',
                'cellPhone': 'Téléphone portable',
                'rol': 'Rôle',
                'student': 'Étudiant',
                'guardian': 'Tuteur',
                'teacher': 'Professeur',
                'staff': 'Personnel',
                'registerButton': 'S\'inscrire',
                'backButton': 'Retour',
                'successMessage': 'Inscription réussie !',
                'successPopupMessage': 'La personne a été enregistrée avec succès.',
                'accountDescription': 'Un compte. Tout GrowUp à votre disposition.',
                'helpLink': 'Aide',
                'privacyLink': 'Confidentialité',
                'termsLink': 'Conditions'
            },
            'Alemán': {
                'createAccount': 'Erstellen Sie ein GrowUp-Konto',
                'goToGoogleDrive': 'Zu Google Drive gehen',
                'firstName': 'Vorname',
                'lastName': 'Nachname',
                'documentType': 'Dokumententyp',
                'DNI': 'Personalausweis',
                'Carnet': 'ID',
                'Pasaporte': 'Reisepass',
                'email': 'Email',
                'cellPhone': 'Handynummer',
                'rol': 'Rolle',
                'student': 'Schüler',
                'guardian': 'Erziehungsberechtigter',
                'teacher': 'Lehrer',
                'staff': 'Personal',
                'registerButton': 'Registrieren',
                'backButton': 'Zurück',
                'successMessage': 'Registrierung erfolgreich!',
                'successPopupMessage': 'Die Person wurde erfolgreich registriert.',
                'accountDescription': 'Ein Konto. Alles von GrowUp zur Verfügung.',
                'helpLink': 'Hilfe',
                'privacyLink': 'Datenschutz',
                'termsLink': 'Bedingungen'
            }
            // Agrega más idiomas aquí
        };

        const languageStringsSelected = languageStrings[language];

        // Actualizar los textos en la página con los valores correspondientes al idioma seleccionado
        document.querySelector('h1').textContent = languageStringsSelected['createAccount'];
        document.querySelector('h2').textContent = languageStringsSelected['goToGoogleDrive'];
        document.querySelector('#names').placeholder = languageStringsSelected['firstName'];
        document.querySelector('#last_name').placeholder = languageStringsSelected['lastName'];
        document.querySelector('#type_document option[value=""]').textContent = languageStringsSelected['documentType'];
        document.querySelector('#type_document option[value="DNI"]').textContent = languageStringsSelected['DNI'];
        document.querySelector('#type_document option[value="Carnet"]').textContent = languageStringsSelected['Carnet'];
        document.querySelector('#type_document option[value="Pasaporte"]').textContent = languageStringsSelected['Pasaporte'];
        document.querySelector('#number_document').placeholder = languageStringsSelected['number_document'];
        document.querySelector('label[for="email"]').textContent = languageStringsSelected['email'];
        document.querySelector('#email').placeholder = languageStringsSelected['email'];
        document.querySelector('label[for="cell_phone"]').textContent = languageStringsSelected['cellPhone'];
        document.querySelector('#cell_phone').placeholder = languageStringsSelected['cellPhone'];
        document.querySelector('label[for="rol"]').textContent = languageStringsSelected['rol'];
        document.querySelector('#rol option[value="ES"]').textContent = languageStringsSelected['student'];
        document.querySelector('#rol option[value="AP"]').textContent = languageStringsSelected['guardian'];
        document.querySelector('#rol option[value="PR"]').textContent = languageStringsSelected['teacher'];
        document.querySelector('#rol option[value="PA"]').textContent = languageStringsSelected['staff'];
        document.querySelector('button[type="submit"]').textContent = languageStringsSelected['registerButton'];
        document.querySelector('a.btn-secondary').textContent = languageStringsSelected['backButton'];
        document.querySelector('#successPopup h4').textContent = languageStringsSelected['successMessage'];
        document.querySelector('#successPopup p').textContent = languageStringsSelected['successPopupMessage'];
        document.querySelector('.registration-image p').textContent = languageStringsSelected['accountDescription'];

        // Actualizar los enlaces de Ayuda, Privacidad y Términos
        document.querySelector('a[href="https://support.google.com/accounts?hl=es&p=account_iph"]').textContent = languageStringsSelected['helpLink'];
        document.querySelector('a[href="https://accounts.google.com/TOS?loc=PE&hl=es&privacy=true"]').textContent = languageStringsSelected['privacyLink'];
        document.querySelector('a[href="https://accounts.google.com/TOS?loc=PE&hl=es"]').textContent = languageStringsSelected['termsLink'];
    }
</script>
<script>
	function updateDocumentPattern() {
	    var typeDocument = document.getElementById("type_document").value;
	    var numberDocumentInput = document.getElementById("number_document");
	
	    if (typeDocument === "DNI") {
	        numberDocumentInput.pattern = "\\d{8}";
	        numberDocumentInput.title = "Ingrese un número de DNI válido (8 dígitos)";
	    } else if (typeDocument === "CNT") {
	        numberDocumentInput.pattern = "\\d{10}";
	        numberDocumentInput.title = "Ingrese un número de carné válido (10 dígitos)";
	    } else if (typeDocument === "PPE") {
	        numberDocumentInput.pattern = "\\d{15}";
	        numberDocumentInput.title = "Ingrese un número de pasaporte válido (15 dígitos)";
	    } else {
	        numberDocumentInput.pattern = "";
	        numberDocumentInput.title = "Ingrese un número de documento válido";
	    }
	}
	
	function trimInput() {
	    var numberDocumentInput = document.getElementById("number_document");
	    numberDocumentInput.value = numberDocumentInput.value.trim();
	}
</script>
</body>
</html>