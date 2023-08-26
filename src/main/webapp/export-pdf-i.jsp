<%@ page language="java" contentType="application/pdf" pageEncoding="UTF-8"%>
<%@ page import="com.itextpdf.text.Document"%>
<%@ page import="com.itextpdf.text.Element"%>
<%@ page import="com.itextpdf.text.PageSize"%>
<%@ page import="com.itextpdf.text.Paragraph"%>
<%@ page import="com.itextpdf.text.pdf.PdfPCell"%>
<%@ page import="com.itextpdf.text.pdf.PdfPTable"%>
<%@ page import="com.itextpdf.text.pdf.PdfWriter"%>
<%@ page import="java.sql.*" %>
<%@ page import="java.io.*" %>

<%
  // Establecer la conexión a la base de datos
  Connection con = null;
  try {
    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel";
    con = DriverManager.getConnection(url);

    // Obtener los datos de la tabla "person" con estado "I"
    String selectQuery = "SELECT * FROM dbo.person WHERE active = 'I'";
    Statement selectStmt = con.createStatement();
    ResultSet rs = selectStmt.executeQuery(selectQuery);

    // Crear un nuevo documento PDF
    Document document = new Document(PageSize.A4);
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    PdfWriter.getInstance(document, baos);

    // Abrir el documento
    document.open();

    // Crear la tabla para los datos de la tabla "person"
    PdfPTable table = new PdfPTable(9); // Número de columnas
    table.setWidthPercentage(100);

    // Agregar encabezados de columna
    table.addCell("ID");
    table.addCell("Nombres");
    table.addCell("Apellidos");
    table.addCell("Tipo Documento");
    table.addCell("Número Documento");
    table.addCell("Email");
    table.addCell("Teléfono");
    table.addCell("Rol");
    table.addCell("Estado");

    // Agregar los datos de la tabla "person" a la tabla del PDF
    while (rs.next()) {
      String personId = rs.getString("id");
      String names = rs.getString("names");
      String lastName = rs.getString("last_name");
      String documentType = rs.getString("type_document");
      String documentNumber = rs.getString("number_document");
      String email = rs.getString("email");
      String phone = rs.getString("cell_phone");
      String role = rs.getString("rol");
      String active = rs.getString("active");

      // Agregar una fila a la tabla con los datos de la persona
      table.addCell(personId);
      table.addCell(names);
      table.addCell(lastName);
      table.addCell(documentType);
      table.addCell(documentNumber);
      table.addCell(email);
      table.addCell(phone);
      table.addCell(role);
      table.addCell(active);
    }

    // Agregar la tabla al documento
    document.add(table);

    // Cerrar el documento
    document.close();

    // Establecer la respuesta HTTP para descargar el archivo PDF
    response.setContentType("application/pdf");
    response.setHeader("Content-Disposition", "attachment;filename=inactive_persons.pdf");
    response.setContentLength(baos.size());

    OutputStream os = response.getOutputStream();
    baos.writeTo(os);
    os.flush();
    os.close();
  } catch (Exception e) {
    out.println("Error: " + e.getMessage());
  } finally {
    if (con != null) {
      try {
        con.close();
      } catch (Exception e) {
        // Ignorar error al cerrar la conexión
      }
    }
  }
%>