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
        /* Estilos anteriores */

        .form-group {
            /* Estilos anteriores */
            display: flex;
            align-items: center;
        }

        .form-group label {
            /* Estilos anteriores */
            margin-right: 10px;
        }

        .form-group input[type="date"] {
            /* Estilos anteriores */
            margin-right: 10px;
        }
    </style>
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
            appearance: none; /* Eliminar la apariencia predeterminada del select */
            -webkit-appearance: none;
            -moz-appearance: none;
            padding-right: 25px; /* Agregar espacio para la flecha personalizada */
            background-image: url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/svgs/solid/chevron-down.svg");
            background-repeat: no-repeat;
            background-position: right 8px center;
            background-size: 14px;
        }
    </style>
        <style>
        /* Estilos anteriores */

        .form-group {
            /* Estilos anteriores */
            display: flex;
            align-items: center;
        }

        .form-group label {
            /* Estilos anteriores */
            margin-right: 10px;
        }

        .form-group input[type="date"] {
            /* Estilos anteriores */
            margin-right: 10px;
        }
        
        .observations-group {
            /* Estilos para el contenedor de Observaciones */
            display: flex;
            align-items: center;
            flex-wrap: wrap; /* Para que los elementos se muestren en líneas si no caben en el ancho */
        }

        .observations-group label {
            /* Estilos para el label de Observaciones */
            margin-right: 10px;
        }

        .observations-group textarea {
            /* Estilos para el campo de texto de Observaciones */
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            flex: 1; /* Ocupar todo el espacio disponible en el contenedor */
            min-width: 200px; /* Ancho mínimo para que no se colapse completamente */
        }
    </style>
    <style>
	    .title {
	        font-size: 24px;
	        margin-right: 20px; /* Puedes ajustar este valor para cambiar la distancia a la derecha */
	        color: #2196f3; /* Puedes cambiar el color a tu gusto */
	    }
	</style> 
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

        .form-group input[type="number"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .form-group button {
            background-color: #2196f3;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 20px;
            cursor: pointer;
        }
    </style>
    <style>
        /* Estilos anteriores */

        .form-group {
            /* Estilos anteriores */
            display: flex;
            align-items: center;
        }

        .form-group label {
            /* Estilos anteriores */
            margin-right: 10px;
        }

        .form-group input[type="date"] {
            /* Estilos anteriores */
            margin-right: 10px;
        }
        
        /* Agregar estilos adicionales si es necesario */
    </style>
    <style>
	    .title {
	        font-size: 24px;
	        margin-right: 20px; /* Puedes ajustar este valor para cambiar la distancia a la derecha */
	        color: #2196f3; /* Puedes cambiar el color a tu gusto */
	    }
	</style>
</head>
  <jsp:include page="menu.jsp" />
<body>
    <div class="container">
        <h1 class="title">Registrar Detalle de Reserva</h1>
        <form action="guardarDetalleReserva.jsp" method="POST">
            <div class="form-group">
                <label for="reservation_id">ID de Reserva:</label>
                <input type="number" id="reservation_id" name="reservation_id" value="<%= request.getParameter("id") %>" required readonly>
            </div>
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
                <input type="number" id="quantity" name="quantity" required min="1" max="10">
            </div>
            <div class="form-group">
                <button type="submit">Guardar Detalle de Reserva</button>
            </div>
        </form>
    </div>
</body>
</html>
