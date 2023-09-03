<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>
<%@ page import="java.util.Calendar" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Crear Reserva</title>
    <link rel="stylesheet" href="css/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 500px;
            margin: 20px auto;
            padding: 25px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #fff;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            font-weight: bold;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .form-group .btn {
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            border: none;
        }

        .form-group .btn-create {
            background-color: #00CED1; /* Celeste */
            color: #fff;
            margin-right: 10px;
            border-top: 2px solid #00CED1; /* Línea divisoria */
        }

        .form-group .btn-back {
            background-color: #808080; /* Plomo */
            color: #fff;
        }	
        
        .title {
            font-size: 24px;
            margin-right: 20px;
            color: #00CED1;
        }

        /* Ajuste para hacer el textarea más alto automáticamente */
        .form-group textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            min-height: 43px;
            resize: vertical;
            height: 1px; /* Tamaño inicial del campo de observaciones */
            overflow-y: hidden; /* Oculta las barras de desplazamiento vertical */
		}
		
		/* Style for the semi-transparent overlay */
		.overlay {
		    display: none;
		    position: fixed;
		    top: 0;
		    left: 0;
		    width: 100%;
		    height: 100%;
		    background-color: rgba(128, 128, 128, 0.5); /* Semi-transparent gray color */
		    z-index: 1000; /* Ensure the overlay is above other elements */
		}
		
		/* Style for the success popup */
		.success-popup {
		    display: none;
		    position: fixed;
		    top: 50%;
		    left: 50%;
		    transform: translate(-50%, -50%);
		    background-color: #fff;
		    border-radius: 10px;
		    padding: 20px;
		    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
		    text-align: center;
		    z-index: 1001; /* Ensure the popup is above the overlay */
		}
		
		.success-popup h4 {
		    color: #00CED1;
		    font-size: 24px;
		    margin: 0;
		}
		
		.success-popup p {
		    font-size: 18px;
		    margin-top: 10px;
		}

	    /* Estilo para las notificaciones */
	    .notification {
	        position: fixed;
	        top: 20px;
	        right: 20px;
	        padding: 10px;
	        background-color: #fff;
	        border-radius: 5px;
	        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
	        display: none;
	    }	

	    .notification-icon {
	        font-size: 24px;
	        margin-right: 10px;
	        color: #1877F2; /* Color de Facebook */
	    }
	
	    .notification-content {
	        font-size: 14px;
	        color: #333;
	    }
	
	    .notification-icon {
	        /* Estilo existente */
	        display: inline-block; /* Agrega esta línea para que el icono esté en la misma línea */
	        vertical-align: middle; /* Alinea verticalmente el icono con el contenido */
	    }
	
	    .notification-content {
	        /* Estilo existente */
	        display: inline-block; /* Agrega esta línea para que el contenido del mensaje esté en la misma línea */
	        vertical-align: middle; /* Alinea verticalmente el contenido con el icono */
	    }

	    .notification.show {
	        display: block;
	        animation: slideInUp 0.3s ease-in-out;
	    }
	
	    @keyframes slideInUp {
	        from {
	            transform: translateY(100%);
	        }
	        to {
	            transform: translateY(0);
	        }
	    }
	</style>
    <script>
        // Función para hacer que el campo de observaciones crezca automáticamente
        function adjustTextareaHeight(textarea) {
        	  textarea.style.height = "auto"; /* Restaura la altura predeterminada */
        	  textarea.style.height = textarea.scrollHeight + "px"; /* Ajusta la altura al contenido */
        	}
    </script>
</head>
<jsp:include page="menu.jsp" />
<body>
    <div class="container">
	    <h1 class="title">Crear Reserva</h1>
        <form action="guardarReserva.jsp" method="POST" accept-charset="UTF-8">
            <div class="form-group">
                <label for="person">Apellidos y Nombres de Persona:</label>
                <select id="person" name="person" required>
                    <option value="" disabled selected>Seleccionar Persona</option>                
					<% 
					Connection con = null;
					Statement stmt = null;
					
					try {
					    // Establecer la conexión con SQL Server
					    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
					    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
					    con = DriverManager.getConnection(url);
					
					    // Consulta para obtener los datos de las personas activas
					    String query = "SELECT id, CONCAT(last_name, ', ', names) AS full_name FROM person WHERE active = 'A'";
					    stmt = con.createStatement();
					    ResultSet rs = stmt.executeQuery(query);
					
					    // Iterar sobre los resultados y mostrar las opciones en el select
					    while (rs.next()) {
					        int personId = rs.getInt("id");
					        String fullName = rs.getString("full_name");
					%>
					<option value="<%= personId %>"><%= fullName %></option>
					<% 
					    }
					} catch (Exception e) {
					    out.println("<option value=\"\">Error al obtener los datos de las personas</option>");
					} finally {
					    // Cerrar la conexión y la declaración
					    if (stmt != null) {
					        stmt.close();
					    }
					    if (con != null) {
					        con.close();
					    }
					}
					%>
                </select>
            </div>
            <div class="form-group">
                <label for="dateAvailable">Fecha de Inicio:</label>
                <input type="date" id="dateAvailable" name="dateAvailable" value="<%= new SimpleDateFormat("yyyy-MM-dd").format(new Date()) %>" required>
            </div>
            <div class="form-group">
				<label for="dateReturn">Fecha de Devolución:</label>
				<%
				    Calendar calendar = Calendar.getInstance();
				    calendar.add(Calendar.DAY_OF_MONTH, 30); // Agregar 30 días
				    String returnDate = new SimpleDateFormat("yyyy-MM-dd").format(calendar.getTime());
				%>
				<input type="date" id="dateReturn" name="dateReturn" value="<%= returnDate %>" required>
            </div>
			<div class="form-group">
			    <label for="observations">Observaciones: <span id="charCount" style="font-size: 12px; color: #999;"></span></label>
			    <textarea id="observations" name="observations" maxlength="100" oninput="adjustTextareaHeight(this)">{{defaultText}}</textarea>
			</div>
			
			<script>
			    const observationsTextarea = document.getElementById("observations");
			    const charCountSpan = document.getElementById("charCount");
			    
			    // Randomly choose default text with an 80% probability
			    const useDefaultText = Math.random() < 0.8;
			    const defaultTextOptions = [
			        "Si no logro llegar para la fecha acordada, le ruego cancelar la reserva a mi nombre.",
			        "De no poder llegar en la fecha reservada, les pido que cancelen la reserva, por favor.",
			        "En el caso de que no pueda asistir en la fecha establecida, le solicito que cancele la reserva.",
			        "En el caso de que no me presente en la fecha indicada, le solicito que elimine la reserva.",
			        "En caso de incumplir la fecha, le solicito que cancele la reserva correspondiente.",
			        "Si no me presento para la fecha acordada, agradecería que anulara la reserva.",
			        "Si no llego en la fecha prevista, le pido que elimine la reserva correspondiente."
			    ];
			    const defaultText = useDefaultText ? defaultTextOptions[Math.floor(Math.random() * defaultTextOptions.length)] : "";
			
			    observationsTextarea.value = defaultText;
			    charCountSpan.textContent = defaultText.length + " / 100 characters";
			
			    observationsTextarea.addEventListener("input", function() {
			        const charCount = observationsTextarea.value.length;
			        charCountSpan.textContent = charCount + " / 100 characters";
			    });
			</script>
			
			<div class="form-group">
			    <button type="submit" class="btn btn-create" onclick="showSuccessPopup()">Crear Reserva</button>
			    <button type="button" class="btn btn-back" onclick="window.history.back();">Volver</button>
			</div>

        </form>
		<div class="overlay" id="overlay"></div>
		
		<div id="successPopup" class="success-popup">
		    <img src="https://img.freepik.com/vector-premium/gato-enojado-trabajando-ilustracion-ordenador-portatil_138676-305.jpg?w=360" alt="Success Icon">
		    <h4>Registro exitoso!</h4>
		    <p>La reserva ha sido creada correctamente.</p>
		</div>
		
		<script>
		    const createReservaButton = document.querySelector(".btn-create");
		    const personSelect = document.getElementById("person");
		    const dateAvailableInput = document.getElementById("dateAvailable");
		    const dateReturnInput = document.getElementById("dateReturn");
		    const notification = document.createElement("div");
		
		    notification.classList.add("notification");
		    notification.innerHTML = `
		        <div class="notification-icon">&#x1F514;</div>
		        <div class="notification-content"></div>
		    `;
		    document.body.appendChild(notification);
		
		    createReservaButton.addEventListener("click", function(event) {
		        event.preventDefault();
		
		        if (personSelect.value === "") {
		            showNotification("Por favor, selecciona una persona.");
		            return;
		        }
		        if (dateAvailableInput.value === "" || dateReturnInput.value === "") {
		            showNotification("Por favor, completa las fechas de inicio y devolución.");
		            return;
		        }
		
		        // Si la validación es exitosa, muestra el mensaje de éxito y envía el formulario
		        overlay.style.display = "block";
		        successPopup.style.display = "block";
		
		        setTimeout(function() {
		            overlay.style.display = "none";
		            successPopup.style.display = "none";
		            createReservaButton.closest("form").submit();
		        }, 3000);
		    });
		
		    function showNotification(message) {
		        notification.querySelector(".notification-content").textContent = message;
		        notification.classList.add("show");
		
		        setTimeout(function() {
		            notification.classList.remove("show");
		        }, 3000);
		    }
		</script>

    </div>
</body>
</html>