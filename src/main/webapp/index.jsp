<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head>
  <title>Inicia sesión</title>
  	<link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
  <style>
    /* Estilos adicionales específicos para esta página */
    body {
      background-color: #f2f2f2;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }
    h1 {
      color: #333;
      text-align: center;
      font-size: 24px;
      margin-bottom: 10px;
    }
    h2 {
      color: #666;
      text-align: center;
      font-size: 12px;
      margin-bottom: 29px;
    }
    form {
      background-color: #fff;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 30px;
      width: 330px;
      margin: auto -40px;
      padding-left: 40px;
      padding-right: 40px;
    }
    label {
      display: block;
      margin-bottom: 7px;
      color: #333;
      font-size: 14px;
    }
	    
	    .help-links {
	      display: flex;
	      justify-content: flex-end;
	      align-items: center;
	    }
	    
	    .help-links a {
	      color: #000;
	      text-decoration: none;
	      font-size: 14px;
	      display: inline-block;
	      padding: 2px 6px;
	      border-radius: 4px;
	      transition: background-color 0.3s;
	      margin-left: 10px;
	    }
	    
	    .help-links a:hover {
	      background-color: #ccc;
	    }
	    
	input[type="text"],
	input[type="tel"] {
	  width: 100%;
	  padding: 10px;
	  border: 1px solid #ccc;
	  border-radius: 3px;
	  font-size: 14px;
	}
	
	input[type="submit"] {
	  background-color: #4CAF50;
	  color: #fff;
	  border: none;
	  padding: 10px 20px;
	  margin-top: 10px;
	  cursor: pointer;
	  width: 100%;
	  font-size: 14px;
	  border-radius: 0.25rem;
	}
	
	input[type="submit"]:hover {
	  background-color: #45a049;
	}
	
	p {
	  text-align: center;
	  margin-top: 10px;
	  font-size: 14px;
	}
	
	.forgot-link {
	  color: #1a73e8;
	  text-decoration: none;
	  font-size: 14px;
	  display: inline-block;
	  padding: 2px 6px;
	  border-radius: 4px;
	  transition: background-color 0.3s;
	}
	
	.forgot-link:hover {
	  background-color: #e1e8f0;
	}
	
	.guest-link {
	  color: #1a73e8;
	  text-decoration: none;
	  font-size: 14px;
	  display: inline-block;
	  padding: 2px 6px;
	  border-radius: 4px;
	  transition: background-color 0.3s;
	}
	
	.guest-link:hover {
	  background-color: #e1e8f0;
	}
	
	.create-account {
	  margin-top: 20px;
	  text-align: left;
	  display: flex;
	  justify-content: space-between;
	  align-items: center;
	}
	
	.create-account a {
	  color: #1a73e8;
	  text-decoration: none;
	  font-size: 14px;
	  display: inline-block;
	  padding: 2px 6px;
	  border-radius: 4px;
	  transition: background-color 0.3s;
	}
	
	.create-account a:hover {
	  background-color: #e1e8f0;
	}
	
	.next-button {
	  display: inline-block;
	  padding: 2px 6px;
	  border-radius: 4px;
	  transition: background-color 0.3s;
	}
	
	.next-button input[type="submit"] {
	  background-color: #1a73e8;
	  color: #fff;
	  font-size: 14px;
	}
	
	.next-button input[type="submit"]:hover {
	  background-color: #0f4ab6;
	}
	
	/* Estilos para el campo de selección de idioma */
	.language-select {
	  display: flex;
	  justify-content: space-between;
	  align-items: center;
	  margin-top: 20px;
	  margin-bottom: 20px;
	}
	
	.language-select label {
	  margin-right: 10px;
	}
	
	.language-select select {
	  padding: 6px 10px;
	  border: 1px solid #ccc;
	  border-radius: 4px;
	  font-size: 14px;
	}
	
	/* Estilos para los enlaces de Ayuda, Privacidad y Términos */
	.footer-links {
	  display: flex;
	  justify-content: flex-end;
	  margin-top: 20px;
	}
	
	.footer-links a {
	  color: #1a73e8;
	  text-decoration: none;
	  font-size: 14px;
	  display: inline-block;
	  padding: 2px 6px;
	  border-radius: 4px;
	  transition: background-color 0.3s;
	  margin-left: 10px;
	}
	
	.footer-links a:hover {
	  background-color: #e1e8f0;
	}
	
    .logo-container {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;
    }
    .logo-container img {
      width: 67px;
      height: 20px;
    }
	  </style>
  <style>
    /* Estilos para la ventana emergente */
    .popup-container {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #fff;
      border: 1px solid #ccc;
      padding: 20px;
      text-align: center;
    }
    .popup-image {
      width: 150px;
      height: 150px;
      margin-bottom: 10px;
    }
  </style>
  <script>
    // Función para mostrar la ventana emergente
    function showPopup(imageUrl, message) {
      var popupContainer = document.getElementById("popup-container");
      var popupImage = document.getElementById("popup-image");
      var popupMessage = document.getElementById("popup-message");

      popupImage.src = imageUrl;
      popupMessage.textContent = message;

      popupContainer.style.display = "block";

      // Redirigir al usuario después de 3 segundos
      setTimeout(function() {
        window.location.href = "edit.jsp";
      }, 3000);
    }
  </script>
	</head>
	<body>
	  <form action="#" method="post">
	      <div class="logo-container">
		    <img src="https://grow-up.cl/wp-content/uploads/2020/04/Logo-GrowUP.png" alt="Logo">
	  </div>
	    <h1 id="login-heading">Inicia sesión</h1>
	    <h2 id="drive-heading">Por favor, ingresa tus datos</h2>
	<label for="email-phone" id="email-phone-label">Correo electrónico o teléfono:</label>
	<input type="text" id="email-phone" name="emailPhone" style="width: 310px;" pattern="(\d{9})|(([\w\.]+@[\w]+\.\w+(\.\w+)?)|)" required title="Ingrese un email válido o un número de celular válido (9 dígitos)">

    <label for="document-number" id="document-number-label" style="margin-top: 16px;">Número de Documento:</label>
	<input type="text" id="document-number" name="documentNumber" pattern="\d{8}|\d{10}|\d{15}" required title="Ingrese un número de documento válido de 8, 10 o 15 dígitos" style="width: 310px; margin-bottom: 5px;">
    	
	<p style="text-align: left;"><a href="#" class="forgot-link" id="forgot-link">¿Has olvidado tu correo electrónico?</a></p>
	
	<p style="margin-top: 35px; margin-bottom: 35px; color: #333;"><span id="guest-link">¿No es tu ordenador? Usa el modo Invitado para iniciar sesión de forma privada.<a href="https://support.google.com/chrome/answer/6130773?hl=es" class="guest-link">Más información</a></span></p>
	
	<div class="create-account">
	  <a href="create.jsp" style="color: #1a73e8; text-decoration: none; font-size: 14px;" id="create-account-link">Crear cuenta</a>
	  <div class="next-button">
	    <input type="submit" value="Siguiente" style="background-color: #1a73e8; color: #fff; font-size: 14px;" id="submit-button">
	  </div>
	</div>
	  </form>
	<div class="language-select">
	  <label for="language">Idioma :</label>
	  <select id="language" onchange="changeLanguage(this.value)">
	    <option value="es" selected>Español</option>
	    <option value="en">Inglés</option>
	    <option value="fr">Francés</option>
	    <option value="de">Alemán</option>
	  </select>
	</div>
	    <div class="help-links">
	      <a href="https://support.google.com/accounts?hl=es&p=account_iph" id="help-link">Ayuda</a>
	      <a href="https://accounts.google.com/TOS?loc=PE&hl=es&privacy=true" id="privacy-link">Privacidad</a>
	      <a href="https://accounts.google.com/TOS?loc=PE&hl=es" id="terms-link">Términos</a>
	    </div>
	  <script>
	    function changeLanguage() {
	      var language = document.getElementById("language").value;
	      
	      if (language === "es") {
	        document.getElementById("login-heading").innerHTML = "Inicia sesión";
	        document.getElementById("drive-heading").innerHTML = "Por favor, ingresa tus datos";
	        document.getElementById("email-phone-label").innerHTML = "Correo electrónico o teléfono:";
	        document.getElementById("document-number-label").innerHTML = "Número de Documento:";
	        document.getElementById("forgot-link").innerHTML = "¿Has olvidado tu correo electrónico?";
	        document.getElementById("guest-link").innerHTML = "¿No es tu ordenador? Usa el modo Invitado para iniciar sesión de forma privada.<a href='https://support.google.com/chrome/answer/6130773?hl=es' class='guest-link'>Más información</a>";
	        document.getElementById("create-account-link").innerHTML = "Crear cuenta";
	        document.getElementById("submit-button").value = "Siguiente";
	        document.getElementById("help-link").innerHTML = "Ayuda";
	        document.getElementById("privacy-link").innerHTML = "Privacidad";
	        document.getElementById("terms-link").innerHTML = "Términos";
	      } else if (language === "en") {
	        document.getElementById("login-heading").innerHTML = "Sign In";
	        document.getElementById("drive-heading").innerHTML = "Please, enter your data";
	        document.getElementById("email-phone-label").innerHTML = "Email or phone:";
	        document.getElementById("document-number-label").innerHTML = "Document Number:";
	        document.getElementById("forgot-link").innerHTML = "Forgot your email?";
	        document.getElementById("guest-link").innerHTML = "Not your computer? Use Guest mode to sign in privately.<a href='https://support.google.com/chrome/answer/6130773?hl=en-US' class='guest-link'>Learn more</a>";
	        document.getElementById("create-account-link").innerHTML = "Create account";
	        document.getElementById("submit-button").value = "Next";
	        document.getElementById("help-link").innerHTML = "Help";
	        document.getElementById("privacy-link").innerHTML = "Privacy";
	        document.getElementById("terms-link").innerHTML = "Terms";
	      } else if (language === "fr") {
	        document.getElementById("login-heading").innerHTML = "Connexion";
	        document.getElementById("drive-heading").innerHTML = "Veuillez entrer vos données";
	        document.getElementById("email-phone-label").innerHTML = "Adresse e-mail ou téléphone :";
	        document.getElementById("document-number-label").innerHTML = "Numéro de document :";
	        document.getElementById("forgot-link").innerHTML = "Vous avez oublié votre adresse e-mail ?";
	        document.getElementById("guest-link").innerHTML = "Pas votre ordinateur ? Utilisez le mode Invité pour vous connecter en privé.<a href='https://support.google.com/chrome/answer/6130773?hl=fr' class='guest-link'>En savoir plus</a>";
	        document.getElementById("create-account-link").innerHTML = "Créer un compte";
	        document.getElementById("submit-button").value = "Suivant";
	        document.getElementById("help-link").innerHTML = "Aide";
	        document.getElementById("privacy-link").innerHTML = "Confidentialité";
	        document.getElementById("terms-link").innerHTML = "Conditions";
	      } else if (language === "de") {
	        document.getElementById("login-heading").innerHTML = "Anmelden";
	        document.getElementById("drive-heading").innerHTML = "Bitte geben Sie Ihre Daten ein";
	        document.getElementById("email-phone-label").innerHTML = "E-Mail oder Telefon:";
	        document.getElementById("document-number-label").innerHTML = "Dokumentennummer:";
	        document.getElementById("forgot-link").innerHTML = "Haben Sie Ihre E-Mail-Adresse vergessen?";
	        document.getElementById("guest-link").innerHTML = "Nicht Ihr Computer? Verwenden Sie den Gastmodus, um sich privat anzumelden.<a href='https://support.google.com/chrome/answer/6130773?hl=de' class='guest-link'>Weitere Informationen</a>";
	        document.getElementById("create-account-link").innerHTML = "Konto erstellen";
	        document.getElementById("submit-button").value = "Weiter";
	        document.getElementById("help-link").innerHTML = "Hilfe";
	        document.getElementById("privacy-link").innerHTML = "Datenschutz";
	        document.getElementById("terms-link").innerHTML = "Nutzungsbedingungen";
	      }
	    }
	  </script>

  <div id="popup-container" class="popup-container" style="display: none;">
    <img id="popup-image" class="popup-image" src="" alt="Success">
    <p id="popup-message"></p>
  </div>

  <% 
  // Procesamiento del formulario
  if (request.getMethod().equalsIgnoreCase("POST")) {
    String emailPhone = request.getParameter("emailPhone");
    String documentNumber = request.getParameter("documentNumber");

    // Realizar la autenticación en la base de datos
	    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;";
	    String username = "sa";
	    String password = "miguelangel";

	    try (Connection conn = DriverManager.getConnection(url, username, password)) {
	    	  String query = "SELECT * FROM dbo.person WHERE (email = ? OR cell_phone = ?) AND number_document = ? AND active = 'A'";
	    	  PreparedStatement pstmt = conn.prepareStatement(query);
	    	  pstmt.setString(1, emailPhone);
	    	  pstmt.setString(2, emailPhone);
	    	  pstmt.setString(3, documentNumber);
	    	  ResultSet rs = pstmt.executeQuery();

	    	  if (rs.next()) {
	    		    // El usuario está autenticado, muestra la ventana emergente
	    		    out.println("<script>showPopup('https://static.vecteezy.com/system/resources/thumbnails/011/360/570/small/cute-cat-working-on-computer-with-coffee-cup-cartoon-icon-illustration-animal-technology-icon-concept-isolated-premium-flat-cartoon-style-vector.jpg', 'Se ha iniciado sesión correctamente.');</script>");
	    		  } else {
	    		    // El usuario no está autenticado, muestra un mensaje de error y redirige después de 2 segundos
	    		    out.println("<script>showPopup('https://static.vecteezy.com/system/resources/previews/011/251/769/non_2x/cute-cat-working-on-laptop-with-coffee-cartoon-icon-illustration-animal-technology-icon-concept-isolated-premium-flat-cartoon-style-vector.jpg', 'Usuario no válido.'); setTimeout(function() { window.location.href = 'index.jsp'; }, 2000);</script>");
	    		  }
	    		} catch (SQLException e) {
	    		  // Manejo de errores
	    		  e.printStackTrace();
	    		}
    }
    %>
</body>
</html>