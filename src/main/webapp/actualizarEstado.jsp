<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

<%
  String personId = request.getParameter("id");
  String estado = request.getParameter("estado");

  // Actualizar el estado en la base de datos
  Connection con = null;
  try {
    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel"; // Reemplaza los valores de acuerdo a tu configuración
    con = DriverManager.getConnection(url);

    String updateQuery = "UPDATE dbo.person SET active = ? WHERE id = ?";
    PreparedStatement updateStmt = con.prepareStatement(updateQuery);
    updateStmt.setString(1, estado);
    updateStmt.setString(2, personId);
    updateStmt.executeUpdate();

    response.getWriter().write("Actualización exitosa");
  } catch (Exception e) {
    e.printStackTrace();
    response.getWriter().write("Error al actualizar");
  } finally {
    if (con != null) {
      try {
        con.close();
      } catch (SQLException e) {
        e.printStackTrace();
      }
    }
  }
%>
