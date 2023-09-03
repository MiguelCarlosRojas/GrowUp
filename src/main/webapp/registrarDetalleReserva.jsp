<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Registrar Detalle de Reserva</title>
    <link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 500px;
            margin: 65px auto;
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
            font-weight: bold;
            margin-right: 10px;
        }

        .form-group select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            padding-right: 25px;
            background-image: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/svgs/solid/chevron-down.svg");
            background-repeat: no-repeat;
            background-position: right 8px center;
            background-size: 14px;
        }

        .form-group button {
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
        }

        /* Estilos para el botón "Volver" */
        .back-button {
            background-color: #b1b0b0; /* Color inicial */
            color: #333;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
            margin-left: 10px;
            transition: background-color 0.3s;
        }

        .back-button:hover {
            background-color: #999; /* Color al pasar el cursor por encima */
        }

        .back-button:focus::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.1); /* Color al hacer clic */
            border-radius: 5px;
        }

        /* Estilos para el botón "Guardar Detalle de Reserva" */
        .save-button {
            background-color: #00aaff; /* Cambiar al color celeste deseado */
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .save-button:hover {
            background-color: #0088cc; /* Cambiar al color celeste deseado para el estado hover */
        }

        .title {
            font-size: 24px;
            margin-right: 20px; /* Puedes ajustar este valor para cambiar la distancia a la derecha */
            color: #2196f3; /* Puedes cambiar el color a tu gusto */
        }
	
	    /* Estilos para el overlay */
	    .overlay {
	        position: fixed;
	        top: 0;
	        left: 0;
	        width: 100%;
	        height: 100%;
	        background-color: rgba(0, 0, 0, 0.5);
	        display: none;
	        z-index: 1000; /* Asegurarse de que esté por encima de otros elementos */
	    }
	
	    /* Estilos para el mensaje emergente de éxito */
	    .success-popup {
	        position: fixed;
	        top: 50%;
	        left: 50%;
	        transform: translate(-50%, -50%);
	        background-color: #fff;
	        padding: 20px;
	        border-radius: 10px;
	        display: none;
	        z-index: 1001; /* Asegurarse de que esté por encima del overlay */
	        text-align: center;
	    }
	</style>
</head>
  <jsp:include page="menu.jsp" />
<body>
    <div class="container">
        <h1 class="title">Registrar Detalle de Reserva</h1>
        <form action="guardarDetalleReserva.jsp" method="POST">
			<input type="hidden" name="reservation_id" value="<%= request.getParameter("id") %>">
            <div class="form-group">
                <label for="book_id">ID de Libro:</label>
                <select id="book_id" name="book_id" required>
                    <option value="" disabled selected>Seleccionar Libro</option>
                    <% 
                        // Obtener los datos (títulos) de la tabla "book" excluyendo aquellos con estado "I"
                        Connection conBook = null;
                        PreparedStatement stmtBook = null;
                        ResultSet rsBook = null;

                        try {
                            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                            String urlBook = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
                            conBook = DriverManager.getConnection(urlBook);

                            String queryBook = "SELECT id, title FROM book WHERE active = ?";
                            stmtBook = conBook.prepareStatement(queryBook);
                            stmtBook.setString(1, "A");
                            rsBook = stmtBook.executeQuery();

                            while (rsBook.next()) {
                                int bookId = rsBook.getInt("id");
                                String bookTitle = rsBook.getString("title");
                                // Mostrar el título del libro como opción en el dropdown
                                out.println("<option value=\"" + bookId + "\">" + bookTitle + "</option>");
                            }
                        } catch (Exception e) {
                            // Manejar el error (puedes mostrar un mensaje de error o registrar el error en un archivo de log)
                            e.printStackTrace();
                        } finally {
                            // Cerrar la conexión y la declaración
                            if (rsBook != null) {
                                rsBook.close();
                            }
                            if (stmtBook != null) {
                                stmtBook.close();
                            }
                            if (conBook != null) {
                                conBook.close();
                            }
                        }
                    %>
                </select>
            </div>
            <div class="form-group">
                <label for="quantity">Cantidad:</label>
                <select id="quantity" name="quantity" required>
                    <option value="1">1</option>
                    <option value="2">2</option>
                </select>
            </div>
            <div class="form-group">
                <button type="submit" class="save-button">Guardar Detalle de Reserva</button>
                <button type="button" class="back-button" onclick="window.history.back()">Volver</button>
            </div>
        </form>
		<div class="overlay" id="overlay"></div>
		
		<div id="successPopup" class="success-popup">
		    <img src="https://img.freepik.com/vector-premium/gato-enojado-trabajando-ilustracion-ordenador-portatil_138676-305.jpg?w=360" alt="Success Icon">
		    <h4>Registro exitoso!</h4>
		    <p>La reserva del libro ha sido creada correctamente.</p>
		</div>
		<script>
		    document.addEventListener("DOMContentLoaded", function() {
		        const saveButton = document.querySelector(".save-button");
		        const overlay = document.getElementById("overlay");
		        const successPopup = document.getElementById("successPopup");
		
		        saveButton.addEventListener("click", function(event) {
		            event.preventDefault(); // Evitar que el formulario se envíe
		
		            // Mostrar el overlay y el mensaje emergente de éxito
		            overlay.style.display = "block";
		            successPopup.style.display = "block";
		
		            // Ocultar el mensaje emergente después de 3 segundos (3000 milisegundos)
		            setTimeout(function() {
		                overlay.style.display = "none";
		                successPopup.style.display = "none";
		                
		                // Redirigir a guardardetalles.jsp
		                window.location.href = "guardarDetalleReserva.jsp";
		            }, 3000); // Cambia el valor si deseas ajustar la duración
		        });
		    });
		</script>

    </div>
</body>
</html>