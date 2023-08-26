<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Reserva</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 500px;
            margin: 45px auto;
            padding: 25px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #fff;
        }

        .form-group {
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }

        .form-group label {
            margin-right: 10px;
			font-weight: bold;

        }

        .form-group input[type="date"] {
            margin-right: 10px;
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
            background-color: #2196f3;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
        }

        .form-group textarea {
            height: 43px;
        }

        .form-group select {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            padding-right: 25px;
            background-image: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/svgs/solid/chevron-down.svg");
            background-repeat: no-repeat;
            background-position: right 8px center;
            background-size: 14px;
        }

        .title {
            font-size: 24px;
            margin-right: 20px;
            color: #00CED1;
        }

        .save-btn {
            background-color: #ccc;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
        }

        .save-btn.active {
            background-color: #00CED1;
            cursor: pointer;
        }

        .back-btn {
            display: inline-block;
            padding: 8px 20px;
            background-color: #808080;
            color: #fff;
            border: none;
            border-radius: 5px;
            margin-left: 10px;
            text-decoration: none;
        }

        .back-btn:hover {
            background-color: #555;
        }

        .auto-resize-textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: none;
            overflow: hidden;
        }

		/* Estilo para el fondo semitransparente */
		.overlay {
		    display: none;
		    position: fixed;
		    top: 0;
		    left: 0;
		    width: 100%;
		    height: 100%;
		    background-color: rgba(128, 128, 128, 0.5); /* Semitransparente gris claro */
		    z-index: 1000; /* Asegura que el fondo esté por encima de otros elementos */
		}
		
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
		    z-index: 1001; /* Asegura que el popup esté por encima del fondo */
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
    </style>
    <style>
        /* ... (estilos existentes) ... */

        /* Estilo para la notificación de error */
        .error-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
            display: none;
        }

        .error-icon {
            font-size: 24px;
            margin-right: 10px;
            color: #f44336; /* Color rojo */
        }

        .error-content {
            font-size: 14px;
            color: #333;
        }

        .error-icon,
        .error-content {
            display: inline-block;
            vertical-align: middle;
        }

        .error-notification.show {
            display: block;
            animation: slideInUp 0.3s ease-in-out;
        }
    </style>
</head>
  <jsp:include page="menu.jsp" />
<body>
    <div class="container">
        <h1 class="title">Editar Reserva</h1>
        <form action="guardarEdicionReserva.jsp" method="POST" accept-charset="UTF-8">
           <%
                Connection con = null;
                PreparedStatement pstmt = null;
                ResultSet rs = null;

                try {
                    // Establecer la conexión con SQL Server
                    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
                    con = DriverManager.getConnection(url);

                    // Obtener el ID de la reserva de la URL
                    int id = Integer.parseInt(request.getParameter("id"));

                    // Consulta para obtener los datos de la reserva con el ID proporcionado
                    String query = "SELECT r.id, CONCAT(p.last_name, ', ', p.names) AS person_name, r.date_reservation, r.date_available, r.date_return, r.status, r.observations, r.person_id " +
                            "FROM reservation r " +
                            "INNER JOIN person p ON r.person_id = p.id " +
                            "WHERE r.id = ?";
                    pstmt = con.prepareStatement(query);
                    pstmt.setInt(1, id);
                    rs = pstmt.executeQuery();

                    if (rs.next()) {
                        // Obtener los datos de la reserva
                        Timestamp dateReservation = rs.getTimestamp("date_reservation");
                        Date dateAvailable = rs.getDate("date_available");
                        Date dateReturn = rs.getDate("date_return");
                        String status = rs.getString("status");
                        String observations = rs.getString("observations");
                        int personId = rs.getInt("person_id");

                        // Formatear fechas
                        SimpleDateFormat dateTimeFormat = new SimpleDateFormat("dd/MM/yyyy, HH:mm");
                        String formattedDateReservation = dateTimeFormat.format(dateReservation);
                        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
                        String formattedDateAvailable = dateFormat.format(dateAvailable);
                        String formattedDateReturn = dateFormat.format(dateReturn);

                        // Formatear el estado para mostrar el texto deseado
                        String formattedStatus = "";
                        if (status.equals("P")) {
                            formattedStatus = "Pendiente";
                        } else if (status.equals("C")) {
                            formattedStatus = "Confirmada";
                        }

                        // Obtener la lista de personas activas para mostrar en el select
                        String personQuery = "SELECT id, CONCAT(last_name, ', ', names) AS full_name FROM person WHERE active = 'A'";
                        PreparedStatement personStmt = con.prepareStatement(personQuery);
                        ResultSet personRs = personStmt.executeQuery();
            %>
            <input type="hidden" name="id" value="<%= id %>">
				<div class="form-group">
				    <label for="person">ID de Persona:</label>
				    <select id="person" name="person" required>
				        <option value="" disabled>Seleccionar Persona</option>
				        <% while (personRs.next()) { %>
				            <option value="<%= personRs.getInt("id") %>" <%= personRs.getInt("id") == personId ? "selected" : "" %>><%= personRs.getString("full_name") %></option>
				        <% } %>
				    </select>
				</div>
            <div class="form-group">
                <label for="dateReservation">Fecha y Hora de la Reserva:</label>
                <input type="text" id="dateReservation" name="dateReservation" value="<%= formattedDateReservation %>" disabled>
            </div>
            <div class="form-group">
                <label for="dateAvailable">Fecha Disponible:</label>
                <input type="date" id="dateAvailable" name="dateAvailable" value="<%= formattedDateAvailable %>" required>
                <label for="dateReturn">Fecha de Devolución:</label>
                <input type="date" id="dateReturn" name="dateReturn" value="<%= formattedDateReturn %>" required>
            </div>
            <div class="form-group">
                <label for="status">Estado:</label>
                <input type="text" id="status" name="status" value="<%= formattedStatus %>" disabled>
            </div>
            <div class="form-group">
                <label for="observations">Observaciones:</label>
                <textarea id="observations" name="observations" class="auto-resize-textarea" oninput="adjustTextareaHeight(this)"><%= observations %></textarea>
            </div>
            <div class="form-group">
                <button type="submit" id="saveBtn" class="save-btn" disabled>Guardar Cambios</button>
                <button type="button" class="back-btn" onclick="window.history.back()">Volver Atrás</button>
            </div>

		    <script>
		        // Función para ajustar la altura del textarea automáticamente
		        function adjustTextareaHeight(element) {
		            element.style.height = "auto";
		            element.style.height = (element.scrollHeight) + "px";
		        }
		    </script> 

            <% 
                    } else {
                        out.println("<p>Reserva no encontrada.</p>");
                    }
                } catch (Exception e) {
                    out.println("<p>Error al obtener los datos de la reserva: " + e.getMessage() + "</p>");
                } finally {
                    // Cerrar la conexión y la declaración
                    if (rs != null) {
                        rs.close();
                    }
                    if (pstmt != null) {
                        pstmt.close();
                    }
                    if (con != null) {
                        con.close();
                    }
                }
            %>
        </form>
       <!-- Notificación de error -->
        <div class="error-notification" id="errorNotification">
            <div class="error-icon">!</div>
            <div class="error-content"></div>
        </div>

		<div class="overlay" id="overlay"></div>
		
		<div id="successPopup" class="success-popup">
		    <img src="https://img.freepik.com/vector-premium/gato-enojado-trabajando-ilustracion-ordenador-portatil_138676-305.jpg?w=360" alt="Success Icon">
		    <h4>Registro exitoso!</h4>
		    <p>Los cambios se han guardado correctamente.</p>
		</div>	
	    <script>
	        const form = document.querySelector("form");
	        const saveBtn = document.querySelector(".save-btn");
	        const errorNotification = document.getElementById("errorNotification");
	
	        form.addEventListener("change", () => {
	            saveBtn.classList.add("active");
	            saveBtn.removeAttribute("disabled");
	            clearTimeout(successPopupTimeout);
	        });
	
	        saveBtn.addEventListener("click", function (event) {
	            event.preventDefault();
	
	            const dateAvailableInput = document.getElementById("dateAvailable");
	            const dateReturnInput = document.getElementById("dateReturn");
	
	            if (dateAvailableInput.value === "" || dateReturnInput.value === "") {
	                showErrorNotification("Por favor, completa las fechas de inicio y devolución.");
	                return;
	            }
	
	            overlay.style.display = "block";
	            successPopup.style.display = "block";
	
	            setTimeout(function () {
	                overlay.style.display = "none";
	                successPopup.style.display = "none";
	                form.submit();
	            }, 5000); // Oculta el popup después de 5 segundos y envía el formulario
	        });
	
	        function showErrorNotification(message) {
	            errorNotification.querySelector(".error-content").textContent = message;
	            errorNotification.classList.add("show");
	
	            setTimeout(function () {
	                errorNotification.classList.remove("show");
	            }, 3000); // Oculta la notificación después de 3 segundos
	        }
	    </script>
    </div>
</body>
</html>