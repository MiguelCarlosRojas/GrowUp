<%@ page language="java" contentType="text/csv; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%@ page import="java.io.IOException" %>
<%@ page import="java.sql.Connection" %>
<%@ page import="java.sql.DriverManager" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.sql.Statement" %>
<%@ page import="com.opencsv.CSVWriter" %>

<%
    // Establecer la conexión con la base de datos
    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;";
    String username = "sa";
    String password = "miguelangel";
    Connection con = null;

    try {
        // Establecer la conexión
        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        con = DriverManager.getConnection(url, username, password);

        // Consulta SQL para obtener los registros con estado "A" y "I" ordenados
        String query = "SELECT names, last_name, type_document, number_document, email, cell_phone, rol, active FROM dbo.person WHERE active IN ('A', 'I') ORDER BY names";

        // Crear el statement y ejecutar la consulta
        Statement statement = con.createStatement();
        ResultSet resultSet = statement.executeQuery(query);

        // Configurar la respuesta HTTP para la descarga del archivo CSV
        response.setContentType("text/csv");
        response.setHeader("Content-Disposition", "attachment; filename=report.csv");

        // Obtener el flujo de salida de la respuesta
        CSVWriter csvWriter = new CSVWriter(response.getWriter());

        // Escribir el encabezado del archivo CSV
        csvWriter.writeNext(new String[]{"Nombres", "Apellidos", "Tipo de Documento", "Numero de Documento", "Email", "Telefono Celular", "Rol", "Estado"});

        // Escribir los datos en el archivo CSV
        while (resultSet.next()) {
            String names = resultSet.getString("names");
            String last_name = resultSet.getString("last_name");
            String type_document = resultSet.getString("type_document");
            String number_document = resultSet.getString("number_document");
            String email = resultSet.getString("email");
            String cell_phone = resultSet.getString("cell_phone");
            String rol = resultSet.getString("rol");
            String active = resultSet.getString("active");

            csvWriter.writeNext(new String[]{names, last_name, type_document, number_document, email, cell_phone, rol, active});
        }

        // Cerrar el CSVWriter
        csvWriter.close();
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        // Cerrar la conexión
        if (con != null) {
            try {
                con.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
%>