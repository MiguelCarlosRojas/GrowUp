<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

<%
// Verificar si se recibió el parámetro "id" de la reserva a eliminar
String reservationIdStr = request.getParameter("id");
if (reservationIdStr != null && !reservationIdStr.isEmpty()) {
    int reservationId = Integer.parseInt(reservationIdStr);

    Connection con = null;
    PreparedStatement pstmt = null;

    try {
        // Establecer la conexión con SQL Server
        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
        con = DriverManager.getConnection(url);

        // Actualizar el estado de la reserva a "I" (inactivo) para simular la eliminación
        String query = "UPDATE reservation SET active = 'I' WHERE id = ?";
        pstmt = con.prepareStatement(query);
        pstmt.setInt(1, reservationId);
        pstmt.executeUpdate();

        // Redireccionar al listado de reservas después de la eliminación
        response.sendRedirect("listadoReservas.jsp");
    } catch (Exception e) {
        out.println("<p>Error al eliminar la reserva: " + e.getMessage() + "</p>");
    } finally {
        // Cerrar la conexión y la declaración
        if (pstmt != null) {
            pstmt.close();
        }
        if (con != null) {
            con.close();
        }
    }
} else {
    // Si no se recibió el parámetro "id", mostrar mensaje de error
    out.println("<p>Error: No se proporcionó el ID de la reserva a eliminar.</p>");
}
%>