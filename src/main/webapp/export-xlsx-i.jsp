<%@ page language="java" contentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<%@ page import="org.apache.poi.xssf.usermodel.XSSFWorkbook" %>
<%@ page import="org.apache.poi.ss.usermodel.*" %>
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

    // Crear un nuevo libro de Excel
    Workbook workbook = new XSSFWorkbook();

    // Crear una nueva hoja de Excel
    Sheet sheet = workbook.createSheet("Inactive Persons");

    // Crear la fila de encabezados de columna
    Row headerRow = sheet.createRow(0);
    headerRow.createCell(0).setCellValue("ID");
    headerRow.createCell(1).setCellValue("Nombres");
    headerRow.createCell(2).setCellValue("Apellidos");
    headerRow.createCell(3).setCellValue("Tipo Documento");
    headerRow.createCell(4).setCellValue("Número Documento");
    headerRow.createCell(5).setCellValue("Email");
    headerRow.createCell(6).setCellValue("Teléfono");
    headerRow.createCell(7).setCellValue("Rol");
    headerRow.createCell(8).setCellValue("Estado");

    // Agregar los datos de la tabla "person" al libro de Excel
    int rowNum = 1;
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

      // Crear una nueva fila en el libro de Excel solo si el estado es "I"
      if (active.equals("I")) {
        Row row = sheet.createRow(rowNum++);
        row.createCell(0).setCellValue(personId);
        row.createCell(1).setCellValue(names);
        row.createCell(2).setCellValue(lastName);
        row.createCell(3).setCellValue(documentType);
        row.createCell(4).setCellValue(documentNumber);
        row.createCell(5).setCellValue(email);
        row.createCell(6).setCellValue(phone);
        row.createCell(7).setCellValue(role);
        row.createCell(8).setCellValue(active);
      }
    }

    // Ajustar el ancho de las columnas
    for (int i = 0; i < 9; i++) {
      sheet.autoSizeColumn(i);
    }

    // Cerrar el ResultSet, Statement y Connection
    rs.close();
    selectStmt.close();
    con.close();

    // Escribir el libro de Excel en un OutputStream
    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
    workbook.write(outputStream);

    // Establecer las cabeceras de la respuesta HTTP para descargar el archivo
    response.setHeader("Content-Disposition", "attachment; filename=inactive_persons.xlsx");
    response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
    response.setContentLength(outputStream.size());

    // Enviar los datos del archivo al cliente
    OutputStream outStream = response.getOutputStream();
    outStream.write(outputStream.toByteArray());
    outStream.flush();
  } catch (Exception e) {
    e.printStackTrace();
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