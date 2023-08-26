<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Actualizar datos</title>
    <style>
        #message {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-size: 24px;
            font-weight: bold;
        }

        .loader {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
<%
// Obtener los parámetros enviados desde el formulario de edición
String id = request.getParameter("id");
String names = request.getParameter("names");
String lastName = request.getParameter("lastname");
String typeDocument = request.getParameter("typedocument");
String numberDocument = request.getParameter("numberdocument");
String email = request.getParameter("email");
String cellPhone = request.getParameter("cellphone");
String rol = request.getParameter("rol");

// Establecer la conexión con la base de datos
String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;";
String username = "sa";
String password = "miguelangel";

Connection connection = null;
PreparedStatement statement = null;

try {
    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
    connection = DriverManager.getConnection(url, username, password);

    // Preparar la consulta de actualización
    String query = "UPDATE dbo.person SET names=?, last_name=?, type_document=?, number_document=?, email=?, cell_phone=?, rol=? WHERE id=?";
    statement = connection.prepareStatement(query);

    // Establecer los valores en la consulta de actualización
    statement.setString(1, names);
    statement.setString(2, lastName);
    statement.setString(3, typeDocument);
    statement.setString(4, numberDocument);
    statement.setString(5, email);
    statement.setString(6, cellPhone);
    statement.setString(7, rol);
    statement.setString(8, id);

    // Ejecutar la consulta de actualización
    int rowsAffected = statement.executeUpdate();

    // Verificar si la actualización se realizó correctamente
    if (rowsAffected > 0) {
        // Mostrar el mensaje de actualización exitosa y animación de espera
        out.println("<div id=\"message\">");
        out.println("<div class=\"loader\"></div>");
        out.println("<span>Los datos se actualizaron correctamente. Redireccionando...</span>");
        out.println("</div>");

        // Redirigir a edit.jsp después de 2 segundos
        out.println("<script>");
        out.println("setTimeout(function() { window.location.href = 'edit.jsp'; }, 2000);");
        out.println("</script>");
    } else {
        // Mostrar el mensaje de error y animación de espera
        out.println("<div id=\"message\">");
        out.println("<div class=\"loader\"></div>");
        out.println("<span>Error al actualizar los datos. Redireccionando...</span>");
        out.println("</div>");

        // Redirigir a edit.jsp después de 2 segundos
        out.println("<script>");
        out.println("setTimeout(function() { window.location.href = 'edit.jsp'; }, 2000);");
        out.println("</script>");
    }
} catch (Exception e) {
    e.printStackTrace();
} finally {
    if (statement != null) {
        statement.close();
    }
    if (connection != null) {
        connection.close();
    }
}
%>
</body>
</html>
    