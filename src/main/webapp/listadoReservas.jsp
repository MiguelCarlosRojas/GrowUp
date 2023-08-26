<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Listado de Reservas</title>
  	<link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
	<link rel="stylesheet" href="css/style.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ccc;
        }

	    th {
	        background-color: #00CED1; /* Color de fondo deseado */
	        color: white; /* Color de texto blanco */
	        padding: 10px;
	        border: 1px solid #ccc;
	    }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        .button-container {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }

        .create-btn {
            color: #ffffff;
            border: none;
            border-radius: 3px;
            padding: 3px 10px;
        }

	    .edit-btn,
	    .delete-btn {
	        font-size: 16px;
	        border-radius: 3px;
	        border: none;
	        padding: 8px;
	        width: 30px; /* Tamaño fijo para crear botones cuadrados */
	        height: 30px; /* Tamaño fijo para crear botones cuadrados */
	        text-align: center;
	        line-height: 1;
	    }
	
	    .edit-btn {
	        background-color: #4CAF50; /* Verde */
	        color: white;
	    }
	
	    .delete-btn {
	        background-color: #f44336; /* Rojo */
	        color: white;
	    }
		
		.confirmation-overlay {
		    display: flex;
		    align-items: center;
		    justify-content: center;
		    position: fixed;
		    top: 0;
		    left: 0;
		    width: 100%;
		    height: 100%;
		    background-color: rgba(0, 0, 0, 0.5);
		}
		
		.confirmation-dialog {
		    background-color: #fff;
		    padding: 20px;
		    border-radius: 7px;
		    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		}
		
		.confirmation-dialog h3 {
		    margin-top: 0;
		    margin-bottom: 10px;
		    text-align: center;
		    font-size: 18px;
		}
		
		.confirmation-dialog p {
		    text-align: center;
		    font-size: 16px;
		    margin-bottom: 20px;
		}
		
		.button-container {
		    display: flex;
		    justify-content: center;
		}
		
		.confirm-btn,
		.cancel-btn {
		    padding: 6px 15px;
		    border: none;
		    border-radius: 4px;
		    cursor: pointer;
		}
		
		.confirm-btn {
		    background-color: #4caf50;
		    color: #fff;
		    margin-right: 10px;
		}
		
		.cancel-btn {
		    background-color: #f44336;
		    color: #fff;
		}

        .good-btn {
            font-size: 16px;
            border-radius: 3px;
            border: none;
            padding: 8px;
            width: 30px; /* Tamaño fijo para crear botones cuadrados */
            height: 30px; /* Tamaño fijo para crear botones cuadrados */
            text-align: center;
            line-height: 1;
            background-color: #ffeb3b; /* Amarillo */
            color: #000;
        }
    </style>
</head>
  <jsp:include page="menu.jsp" />
<body>
    <h1>Listado de Reservas</h1>
	<div class="button-container" style="display: flex; justify-content: flex-end;">
	    <button class="create-btn" style="background-color: #00CED1;" onclick="window.location.href = 'crearReserva.jsp'">Nuevo</button>
	</div>
    <table>
	    <tr>
	        <th>Apellidos y Nombres</th>
	        <th>Fecha de Inicio</th>
	        <th>Fecha de Devolución</th>
	        <th>Libro</th>
	        <th>Cantidad</th>
	        <th>Estado</th>
	        <th>Observaciones</th>
	        <th>Acciones</th>
	    </tr>

        <% 
            Connection con = null;
            Statement stmt = null;

            try {
                // Establecer la conexión con SQL Server
                Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
                con = DriverManager.getConnection(url);

                // Ejecutar la consulta para obtener los datos de la tabla "reservation" y los títulos de los libros
                String query = "SELECT r.id, CONCAT(p.last_name, ', ', p.names) AS person_name, r.date_reservation, r.date_available, r.date_return, r.status, r.observations, r.active, " +
                               "b.title, d.quantity " +
                               "FROM reservation r " +
                               "INNER JOIN person p ON r.person_id = p.id " +
                               "LEFT JOIN detail_reservation d ON r.id = d.reservation_id " +
                               "LEFT JOIN book b ON d.book_id = b.id"; // Agregado
                stmt = con.createStatement();
                ResultSet rs = stmt.executeQuery(query);

                SimpleDateFormat dateFormat = new SimpleDateFormat("dd MMM yyyy, HH:mm");
                SimpleDateFormat spanishDateFormat = new SimpleDateFormat("d MMM yyyy");

                // Iterar sobre los resultados y mostrarlos en la tabla
                while (rs.next()) {
                    int id = rs.getInt("id");
                    String personName = rs.getString("person_name");
                    Timestamp dateReservation = rs.getTimestamp("date_reservation");
                    Date dateAvailable = rs.getDate("date_available");
                    Date dateReturn = rs.getDate("date_return");
                    String status = rs.getString("status");
                    String observations = rs.getString("observations");
                    if (observations != null && observations.length() > 25) {
                        observations = observations.substring(0, 25) + "...";
                    }
                    String active = rs.getString("active");
                    String bookTitle = rs.getString("title"); // Cambiado de book_id a title
                    int quantity = rs.getInt("quantity");

                    // Traducir el estado a su representación completa
                    String statusText = "";
                    if (status.equals("P")) {
                        statusText = "Pendiente";
                    } else if (status.equals("C")) {
                        statusText = "Confirmada";
                    }

                    // Si el registro está activo (active = "A"), mostrar los botones "Editar" y "Eliminar"
                    // Si el registro está inactivo (active = "I"), ocultar la fila
	                if (active.equals("A")) {
	                    out.println("<tr>");
	                    out.println("<td>" + personName + "</td>");
	                    out.println("<td>" + spanishDateFormat.format(dateAvailable) + "</td>");
	                    out.println("<td>" + spanishDateFormat.format(dateReturn) + "</td>");
	                    out.println("<td>" + (bookTitle != null ? bookTitle : "Pendiente") + "</td>"); // Cambiado con condición
	                    out.println("<td>" + quantity + "</td>");
	                    out.println("<td>" + statusText + "</td>");
	                    out.println("<td>" + observations + "</td>");
	                    out.println("<td>");
	                    out.println("<button class=\"edit-btn\" onclick=\"editReservation(" + id + ")\"><i class=\"fas fa-edit\"></i></button>");
	                    out.println("<button class=\"delete-btn\" onclick=\"deleteReservation(" + id + ")\"><i class=\"fas fa-trash-alt\"></i></button>");
	                    // Si el registro está activo (active = "A") y el estado no es "Confirmado" (status != "C"), mostrar el botón "good-btn"
	                    if (active.equals("A") && !status.equals("C")) {
	                        out.println("<button class=\"good-btn\" onclick=\"doSomethingGood(" + id + ")\"><i class=\"fas fa-check\"></i></button>");
	                    }
	                    out.println("</td>");
	                    out.println("</tr>");
	                }
                }
            } catch (Exception e) {
                out.println("<p>Error al obtener los datos de la tabla: " + e.getMessage() + "</p>");
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
    </table>

    <div id="confirmation-overlay" class="confirmation-overlay" style="display: none;">
        <div class="confirmation-dialog">
            <h3>Confirmar Eliminación</h3>
            <p>¿Estás seguro de eliminar esta reserva?</p>
            <div class="button-container">
                <!-- Iconos Font Awesome para los botones -->
                <button class="confirm-btn" onclick="confirmDelete()"><i class="fas fa-check"></i> Confirmar</button>
                <button class="cancel-btn" onclick="cancelDelete()"><i class="fas fa-times"></i> Cancelar</button>
            </div>
        </div>
    </div>

	<script>
	    // Variables para almacenar el ID de la reserva a eliminar y el cuadro de diálogo de confirmación
	    let reservationIdToDelete = null;
	    const confirmationOverlay = document.getElementById("confirmation-overlay");
	
	    function deleteReservation(id) {
	        // Guardar el ID de la reserva a eliminar
	        reservationIdToDelete = id;
	
	        // Mostrar el cuadro de diálogo de confirmación
	        confirmationOverlay.style.display = "flex";
	    }
	
	    function confirmDelete() {
	        // Enviar una solicitud al servidor para eliminar la reserva con el ID almacenado
	        fetch('eliminarReserva.jsp?id=' + reservationIdToDelete, {
	            method: 'POST',
	            headers: {
	                'Content-Type': 'application/x-www-form-urlencoded'
	            }
	        })
	        .then(response => response.text())
	        .then(data => {
	            // Ocultar el cuadro de diálogo de confirmación
	            confirmationOverlay.style.display = "none";
	            // Actualizar la página después de eliminar la reserva
	            location.reload();
	        })
	        .catch(error => console.error('Error:', error));
	    }
	
	    function cancelDelete() {
	        // Ocultar el cuadro de diálogo de confirmación y restablecer el ID de la reserva a eliminar
	        confirmationOverlay.style.display = "none";
	        reservationIdToDelete = null;
	    }
	</script>
	
	<script>
	    // Resto de funciones existentes
	
	    function editReservation(id) {
	        // Redireccionar a la página de edición con el ID de la reserva
	        window.location.href = "editarReserva.jsp?id=" + id;
	    }
	</script>
    <script>
        // Resto de funciones existentes
        
        function doSomethingGood(id) {
	        // Redireccionar a la página de edición con el ID de la detalle reserva
	        window.location.href = "registrarDetalleReserva.jsp?id=" + id;
        }
    </script>
</body>
</html>