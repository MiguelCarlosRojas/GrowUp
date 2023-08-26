<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

	<%
	  // Obtener parámetros del formulario
	  String id = request.getParameter("id");
	  String action = request.getParameter("action");
	
	  // Actualizar la base de datos
	  Connection con = null;
	  try {
	    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
	    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel"; // Reemplaza los valores de acuerdo a tu configuración
	    con = DriverManager.getConnection(url);
	
	    // Actualizar el estado de activo/inactivo
	    if (action != null && action.equals("inactive")) {
	      String updateQuery = "UPDATE dbo.person SET active = 'I' WHERE id = ?";
	      PreparedStatement updateStmt = con.prepareStatement(updateQuery);
	      updateStmt.setString(1, id);
	      updateStmt.executeUpdate();
	    } else if (action != null && action.equals("reactivate")) {
	      String updateQuery = "UPDATE dbo.person SET active = 'A' WHERE id = ?";
	      PreparedStatement updateStmt = con.prepareStatement(updateQuery);
	      updateStmt.setString(1, id);
	      updateStmt.executeUpdate();
	    }
	
	    // Obtener los registros actualizados
	    String selectQuery = "SELECT id, names, last_name, type_document, number_document, email, cell_phone, rol, active FROM dbo.person";
	
	    // Obtener los parámetros de búsqueda
	    String searchName = request.getParameter("name");
	    String searchLastName = request.getParameter("lastname");
	    String searchDocumentType = request.getParameter("documenttype");
	    String searchRole = request.getParameter("role");
	
	    // Construir la cláusula WHERE para la consulta
	    String whereClause = " WHERE 1=1";
	    if (searchName != null && !searchName.isEmpty()) {
	      whereClause += " AND UPPER(names) LIKE '%" + searchName.toUpperCase() + "%'";
	    }
	    if (searchLastName != null && !searchLastName.isEmpty()) {
	      whereClause += " AND UPPER(last_name) LIKE '%" + searchLastName.toUpperCase() + "%'";
	    }
	    if (searchDocumentType != null && !searchDocumentType.isEmpty()) {
	      whereClause += " AND type_document = '" + searchDocumentType + "'";
	    }
	    if (searchRole != null && !searchRole.isEmpty()) {
	      whereClause += " AND rol = '" + searchRole + "'";
	    }
	
	    // Agregar la cláusula WHERE a la consulta
	    selectQuery += whereClause + " ORDER BY id ASC";
	
	    Statement selectStmt = con.createStatement();
	    ResultSet rs = selectStmt.executeQuery(selectQuery);
	
	    // Mostrar la tabla actualizada
	%>
	<!DOCTYPE html>
	<html>
	<head>
	  <meta charset="UTF-8">
	  <title>Reactivar Personas</title>
	  <link rel="icon" href="https://images.vexels.com/media/users/3/205195/isolated/preview/1c2ccc57f033c7b2612f1cce2b6eb7f2-ilustraci-n-de-gato-durmiendo-en-estanter-a.png">
	  <link rel="stylesheet" href="css/style.css">
	  <style>
	    /* Estilos CSS */
	    body {
	      font-family: Arial, sans-serif;
	      background-color: #f2f2f2;
	      margin: 0;
	      padding: 20px;
	    }
	
	    h1 {
	      text-align: center;
	      margin-bottom: 26px;
	    }
	
	    form {
	      margin-bottom: 20px;
	    }
	
	    label {
	      font-weight: bold;
	    }
	
	    input[type="text"],
	    select {
	      padding: 2px;
	      border: 1px solid #ccc;
	      border-radius: 4px;
	      width: 190px;
	      margin-right: 10px;
	    }
	
	    input[type="submit"] {
	      padding: 4px 11px;
	      border: none;
	      border-radius: 4px;
	      background-color: #1a73e8;
	      color: white;
	      cursor: pointer;
	    }
	
	    table {
	      width: 100%;
	      border-collapse: collapse;
	    }
	
	    th, td {
	      padding: 8px;
	      text-align: left;
	      border-bottom: 1px solid #ddd;
	    }
	
	    th {
	      background-color: #f2f2f2;
	    }
	
	    .inactive-row {
	      background-color: #e0e0e0;
	    }
	
	    .edit-btn {
	      background-color: #4CAF50;
	      border: none;
	      color: white;
	      padding: 6px 12px;
	      text-align: center;
	      text-decoration: none;
	      display: inline-block;
	      font-size: 14px;
	      margin-right: 6px;
	      cursor: pointer;
	      border-radius: 4px;
	    }
	
	    .delete-btn {
	      background-color: #FF4136;
	      border: none;
	      color: white;
	      padding: 6px 12px;
	      text-align: center;
	      text-decoration: none;
	      display: inline-block;
	      font-size: 14px;
	      cursor: pointer;
	      border-radius: 4px;
	    }
	  </style>
	  <style>
	    /* Estilos CSS */
	    .btn-new {
	      padding: 8px 16px;
	      border: none;
	      border-radius: 4px;
	      background-color: #1a73e8;
	      color: white;
	      cursor: pointer;
	    }
	
	    th, td {
	      border: 1px solid #ddd;
	      padding: 8px;
	      text-align: left;
	    }
	
	    th {
	      background-color: #1a73e8;
	      color: white;
	    }
	  </style>
	  <style>
	    .btn-csv {
	      background-color: #24a148;
	    }
	
	    .btn-pdf {
	      background-color: #e06666;
	    }
	
	    .btn-xlsx {
	      background-color: #f4b400;
	    }
	
	    .btn-icon {
	      display: inline-flex;
	      align-items: center;
	      justify-content: center;
	      margin-right: 10px;
	    }
	  </style>
	 <style>
	  /* Estilos CSS */
	  body {
	    font-family: Arial, sans-serif;
	    background-color: #f2f2f2;
	    margin: 0;
	    padding: 20px;
	  }
	  
	  h1{
	    text-align: center;
	    margin-bottom: 26px;
	  }
	
	  table {
	    width: 100%;
	    border-collapse: collapse;
	  }
	
	  th, td {
	    padding: 8px;
	    text-align: left;
	    border: 1px solid #ddd;
	  }
	
	  th {
	    background-color: #1a73e8;
	    color: white;
	  }
	
	  .inactive-row {
	    background-color: #e0e0e0;
	  }
	</style>
	  <style>
	    /* Estilos CSS */    
	    .delete-link {
	      color: red;
	      cursor: pointer;
	    }
	    
	    /* Estilos para los cuadros de diálogo */
	    .background-overlay {
	      position: fixed;
	      top: 0;
	      left: 0;
	      width: 100%;
	      height: 100%;
	      background-color: rgba(211, 211, 211, 0.7); /* Color plomo medio claro con transparencia */
	      z-index: 9999;
	      display: flex;
	      justify-content: center;
	      align-items: center;
	    }
	    
	    .confirmation-dialog {
	      position: fixed;
	      top: 50%;
	      left: 50%;
	      transform: translate(-50%, -50%);
	      background-color: #fff;
	      padding: 20px;
	      border-radius: 5px;
	      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	      z-index: 99999;
		  display: table;
	      flex-direction: column;
	      align-items: center;
	      text-align: center;
	    }
	    
	    .confirmation-dialog h3 {
	      font-size: 18px;
	      margin-bottom: 15px;
	    }
	    
	    .confirmation-dialog button {
		margin: 0 10px;
		margin-top: 10px;
	    padding: 6px 12px;
	    font-size: 14px;
	    border-radius: 4px;
	    border: none;
	    color: white;
	    cursor: pointer;
	    }
	    
	    .confirmation-dialog button.accept-btn {
	      background-color: #5cb85c;
	      color: #fff;
	    }
	    
	    .confirmation-dialog button.cancel-btn {
	      background-color: #d9534f;
	      color: #fff;
	    }
	  </style>
	  <style>
	  /* Estilos CSS */    
	  .delete-link {
	    color: red;
	    cursor: pointer;
	  }
	  
	  .reactivate-link {
	    background-color: #1a73e8;
	    border: none;
	    color: white;
	    padding: 6px 12px;
	    text-align: center;
	    text-decoration: none;
	    display: inline-block;
	    font-size: 14px;
	    margin-right: 6px;
	    cursor: pointer;
	    border-radius: 4px;
	  }
	  </style>
	</head>
	  <jsp:include page="menu.jsp" />
	<body>
	  <h1>Reactivar Personas</h1>
	  <form action="" method="get">
	    <label for="name">Nombres:</label>
	    <input type="text" id="name" name="name" value="<%= (searchName != null) ? searchName : "" %>">
	    <label for="lastname">Apellidos:</label>
	    <input type="text" id="lastname" name="lastname" value="<%= (searchLastName != null) ? searchLastName : "" %>">
	      <label for="documenttype">Tipo de Documento:</label>
	      <select id="documenttype" name="documenttype">
	        <option value="">Todos</option>
	        <option value="DNI" <%= searchDocumentType != null && searchDocumentType.equals("DNI") ? "selected" : "" %>>DNI</option>
	        <option value="CNT" <%= searchDocumentType != null && searchDocumentType.equals("CNT") ? "selected" : "" %>>Carnet</option>
	        <option value="PPE" <%= searchDocumentType != null && searchDocumentType.equals("PPE") ? "selected" : "" %>>Pasaporte</option>
	      </select>
	    <label for="role">Rol:</label>
	    <select id="role" name="role">
	      <option value="">Todos</option>
	      <option value="ES" <% if (searchRole != null && searchRole.equals("ES")) { %>selected<% } %>>Estudiante</option>
	      <option value="AP" <% if (searchRole != null && searchRole.equals("AP")) { %>selected<% } %>>Apoderado</option>
	      <option value="PR" <% if (searchRole != null && searchRole.equals("PR")) { %>selected<% } %>>Profesor</option>
	      <option value="PA" <% if (searchRole != null && searchRole.equals("PA")) { %>selected<% } %>>Personal</option>
	    </select>
	    <input type="submit" value="Buscar" style="margin-right: 4px;">
	  </form>
	  <div>
		<input type="button" class="btn-csv btn-icon" value="CSV" onclick="location.href='export-csv-i.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-pdf btn-icon" value="PDF" onclick="location.href='export-pdf-i.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-xlsx btn-icon" value="XLSX" onclick="location.href='export-xlsx-i.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
	    <input type="button" class="btn-new" value="Nuevo" onclick="location.href='register.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; cursor: pointer; color: white; float: right;">
		<input type="button" class="btn-reactivate" value="Activar" onclick="location.href='edit.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; cursor: pointer; color: white; background-color: #1a73e8; float: right; margin-right: 14px;">
	  </div>
	  <br>
	  <table>    
	  <tr>
	      <th>ID</th>
	      <th>Nombres</th>
	      <th>Apellidos</th>
	      <th>Tipo de Documento</th>
	      <th>Número de Documento</th>
	      <th>Correo Electrónico</th>
	      <th>Teléfono Celular</th>
	      <th>Rol</th>
	      <th>Estado</th>
	      <th>Acción</th>
	    </tr>
	<%
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
	
	  // Definir el texto del rol, tipo documento y el estado
	  String roleText = "";
	  if (role.equals("ES")) {
	    roleText = "Estudiante";
	  } else if (role.equals("AP")) {
	    roleText = "Apoderado";
	  } else if (role.equals("PR")) {
	      roleText = "Profesor";
	  } else if (role.equals("PA")) {
	      roleText = "Personal";
	  }
	
	  // Definir el texto del tipo de documento
	  String documentTypeText = "";
	  if (documentType.equals("CNT")) {
	    documentTypeText = "Carnet";
	  } else if (documentType.equals("PPE")) {
	    documentTypeText = "Pasaporte";
	  } else if (documentType.equals("DNI")) {
	    documentTypeText = "DNI";
	  } else if (documentType.equals("OTRO")) {
	    documentTypeText = "Otro";
	  }
	  
	  String activeText = "";
	  String actionBtnText = "";
	  String actionBtnClass = "";
	  String actionBtnAction = "";
	  
	  if (active.equals("A")) {
	    activeText = "Activo";
	    actionBtnText = "Inactivar";
	    actionBtnClass = "delete-link";
	    actionBtnAction = "inactive";
	  } else if (active.equals("I")) {
	    activeText = "Inactivo";
	    actionBtnText = "Reactivar";
	    actionBtnClass = "reactivate-link";
	    actionBtnAction = "reactivate";
	  }
	%>
	  <% if (active.equals("A")) { %> <!-- Agregar condición para ocultar filas activas -->
	    <tr<% if (active.equals("I")) { %> class="inactive-row"<% } %> style="display: none;">
	  <% } else { %>
	    <tr<% if (active.equals("I")) { %> class="inactive-row"<% } %>>
	  <% } %>
	    <td><%= personId %></td>
	    <td><%= names %></td>
	    <td><%= lastName %></td>
	    <td><%= documentTypeText %></td>
	    <td><%= documentNumber %></td>
	    <td><%= email %></td>
	    <td><%= phone %></td>
	    <td><%= roleText %></td>
	    <td><%= activeText %></td>
	    <td>
	      <a class="<%= actionBtnClass %>" onclick="showConfirmationDialog('<%= personId %>', '<%= actionBtnAction %>')"><%= actionBtnText %></a>
	    </td>
	  </tr>
	<%
	}
	%>
	  </table>
	  <!-- Cuadro de diálogo de confirmación -->
	  <div id="confirmation-dialog" class="background-overlay" style="display: none;">
	    <div class="confirmation-dialog">
	      <h3>Confirmación</h3>
	      <p>¿Estás seguro de realizar esta acción?</p>
	      <button class="accept-btn" onclick="confirmAction()">Aceptar</button>
	      <button class="cancel-btn" onclick="cancelAction()">Cancelar</button>
	    </div>
	  </div>
	  <script>
	    var selectedId;
	    var selectedAction;
	
	    function showConfirmationDialog(id, action) {
	      selectedId = id;
	      selectedAction = action;
	      document.getElementById('confirmation-dialog').style.display = 'flex';
	    }
	
	    function confirmAction() {
	      var form = document.createElement('form');
	      form.method = 'post';
	      form.action = '<%= request.getRequestURI() %>';
	
	      var inputId = document.createElement('input');
	      inputId.type = 'hidden';
	      inputId.name = 'id';
	      inputId.value = selectedId;
	      form.appendChild(inputId);
	
	      var inputAction = document.createElement('input');
	      inputAction.type = 'hidden';
	      inputAction.name = 'action';
	      inputAction.value = selectedAction;
	      form.appendChild(inputAction);
	
	      document.body.appendChild(form);
	      form.submit();
	    }
	
	    function cancelAction() {
	      document.getElementById('confirmation-dialog').style.display = 'none';
	    }
	  </script>
	</body>
	</html>
	<%
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
