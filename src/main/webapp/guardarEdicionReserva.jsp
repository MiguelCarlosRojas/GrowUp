<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.text.SimpleDateFormat" %>
<%@ page import="java.util.Date" %>

<%
    request.setCharacterEncoding("UTF-8"); // Configurar la codificación de la solicitud

    Connection con = null;
    PreparedStatement pstmt = null;

    try {
        // Establecer la conexión con SQL Server
        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
        con = DriverManager.getConnection(url);

        // Obtener los datos enviados desde el formulario de edición
        int id = Integer.parseInt(request.getParameter("id"));
        String dateAvailableStr = request.getParameter("dateAvailable");
        String dateReturnStr = request.getParameter("dateReturn");
        String observations = request.getParameter("observations");
        int personId = Integer.parseInt(request.getParameter("person")); // Obtener el ID de Persona seleccionado

        // Convertir las fechas enviadas desde el formulario al formato de Date
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dateAvailable = dateFormat.parse(dateAvailableStr);
        Date dateReturn = dateFormat.parse(dateReturnStr);

        // Consulta para actualizar los datos de la reserva
        String query = "UPDATE reservation SET date_available = ?, date_return = ?, observations = ?, person_id = ? WHERE id = ?";
        pstmt = con.prepareStatement(query);
        pstmt.setDate(1, new java.sql.Date(dateAvailable.getTime()));
        pstmt.setDate(2, new java.sql.Date(dateReturn.getTime()));
        pstmt.setString(3, observations);
        pstmt.setInt(4, personId);
        pstmt.setInt(5, id);

        // Ejecutar la actualización
        pstmt.executeUpdate();

        // Redireccionar a la página de listado de reservas después de guardar los cambios
        response.sendRedirect("listadoReservas.jsp");
    } catch (Exception e) {
        out.println("<p>Error al guardar los cambios: " + e.getMessage() + "</p>");
    } finally {
        // Cerrar la conexión y la declaración
        if (pstmt != null) {
            pstmt.close();
        }
        if (con != null) {
            con.close();
        }
    }
%>