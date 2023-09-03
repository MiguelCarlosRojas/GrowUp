<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Registrar Detalle de Reserva</title>
    <!-- Agrega los enlaces a los estilos CSS y las bibliotecas de iconos Font Awesome -->
  	<link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">

    <!-- Estilos adicionales aquí si los necesitas -->

    <style>
        /* Estilos para los mensajes de éxito y error */
        .message-container {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 15px;
            border-radius: 5px;
            z-index: 9999;
            text-align: center;
        }

        .success {
            background-color: #4CAF50;
            color: white;
        }

        .error {
            background-color: #f44336;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">Registrar Detalle de Reserva</h1>
        <form action="guardarDetalleReserva.jsp" method="POST" accept-charset="UTF-8">
            <% 
                // Obtener los valores del formulario
                int reservationId = Integer.parseInt(request.getParameter("reservation_id"));
                int bookId = Integer.parseInt(request.getParameter("book_id"));
                int quantity = Integer.parseInt(request.getParameter("quantity"));

                // Realizar la conexión a la base de datos y guardar los valores en la tabla detail_reservation
                Connection con = null;
                PreparedStatement stmt = null;

                try {
                    // Establecer la conexión con SQL Server
                    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
                    con = DriverManager.getConnection(url);

                    // Insertar el nuevo detalle de reserva en la tabla detail_reservation
                    String insertQuery = "INSERT INTO detail_reservation (reservation_id, book_id, quantity) VALUES (?, ?, ?)";
                    stmt = con.prepareStatement(insertQuery);
                    stmt.setInt(1, reservationId);
                    stmt.setInt(2, bookId);
                    stmt.setInt(3, quantity);
                    stmt.executeUpdate();

                    // Mostrar mensaje de éxito
                    out.println("<p class=\"success\">Detalle de reserva registrado exitosamente.</p>");
                } catch (Exception e) {
                    // Mostrar mensaje de error
                    out.println("<p class=\"error\">Error al registrar el detalle de reserva.</p>");
                    e.printStackTrace();
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
        </form>
    </div>
    
	<!-- Script para mostrar mensajes y redireccionar después de 3 segundos -->
	<script>
	    const showMessage = (messageType, message) => {
	        const messageContainer = document.createElement('div');
	        messageContainer.classList.add('message-container', messageType);
	        messageContainer.innerText = message;
	        document.body.appendChild(messageContainer);
	        
	        setTimeout(() => {
	            messageContainer.style.display = 'none';
	            
	            // Redireccionar según el tipo de mensaje
	            if (messageType === 'success') {
	                window.location.href = 'listadoReservas.jsp';
	            } else if (messageType === 'error') {
	                window.history.back();
	            }
	        }, 3000); // 3 segundos
	    };
	    
	    // Mostrar el mensaje de éxito o error según lo que se haya impreso en el JSP
	    const messageElement = document.querySelector('.success, .error');
	    if (messageElement) {
	        showMessage(messageElement.classList.contains('success') ? 'success' : 'error', messageElement.innerText);
	    }
	</script>

</body>
</html>