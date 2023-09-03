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

        // Obtener los datos enviados desde el formulario de creación de reserva
        int personId = Integer.parseInt(request.getParameter("person"));
        String dateAvailableStr = request.getParameter("dateAvailable");
        String dateReturnStr = request.getParameter("dateReturn");
        String observations = request.getParameter("observations");

        // Convertir las fechas enviadas desde el formulario al formato de Date
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date dateAvailable = dateFormat.parse(dateAvailableStr);
        Date dateReturn = dateFormat.parse(dateReturnStr);

        // Consulta para insertar la nueva reserva en la base de datos
        String query = "INSERT INTO reservation (person_id, date_available, date_return, status, observations) VALUES (?, ?, ?, 'P', ?)";
        pstmt = con.prepareStatement(query);
        pstmt.setInt(1, personId);
        pstmt.setDate(2, new java.sql.Date(dateAvailable.getTime()));
        pstmt.setDate(3, new java.sql.Date(dateReturn.getTime()));
        pstmt.setString(4, observations);

        // Ejecutar la inserción
        pstmt.executeUpdate();

        // Redireccionar a la página de listado de reservas después de guardar la reserva
        response.sendRedirect("listadoReservas.jsp");
    } catch (Exception e) {
        out.println("<p>Error al guardar la reserva: " + e.getMessage() + "</p>");
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