<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>

	<%
	  String searchName = request.getParameter("name");
	  String searchLastName = request.getParameter("lastname");
	  String searchDocumentType = request.getParameter("documenttype");
	  String searchRole = request.getParameter("role");
	  String searchStatus = request.getParameter("status");
	
	  // Obtener los registros de la base de datos
	  Connection con = null;
	  try {
	    Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
	    String url = "jdbc:sqlserver://localhost:1433;databaseName=dbGrowUp;encrypt=true;TrustServerCertificate=True;user=sa;password=miguelangel"; // Reemplaza los valores de acuerdo a tu configuración
	    con = DriverManager.getConnection(url);
	
	    String selectQuery = "SELECT id, names, last_name, type_document, number_document, email, cell_phone, rol, active FROM dbo.person";
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
	    if (searchStatus != null && !searchStatus.isEmpty()) {
	      if (searchStatus.equals("A")) {
	        whereClause += " AND active = 'A'";
	      } else if (searchStatus.equals("I")) {
	        whereClause += " AND active = 'I'";
	      }
	    }
	
	    selectQuery += whereClause + " ORDER BY id ASC";
	
	    PreparedStatement selectStmt = con.prepareStatement(selectQuery);
	    ResultSet rs = selectStmt.executeQuery();
	
	%>
	<!DOCTYPE html>
	<html>
	<head>
	  <meta charset="UTF-8">
	  <title>CRUD de Personas</title>
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
	 <!-- Agrega este código en el sección <style> o en un archivo CSS -->
	<style>
	  .confirmation-dialog {
	    position: fixed;
	    top: 0;
	    left: 0;
	    width: 100%;
	    height: 100%;
	    background-color: rgba(0, 0, 0, 0.5);
	    display: flex;
	    align-items: center;
	    justify-content: center;
	    z-index: 999;
	  }
	
	  .confirmation-dialog-content {
	    background-color: white;
	    padding: 20px;
	    border-radius: 4px;
	    text-align: center;
	  }
	
	  .confirmation-dialog-buttons {
	    margin-top: 20px;
	  }
	
	  .confirmation-dialog-buttons button {
	    margin: 0 10px;
	    margin-top: 10px;
	    padding: 6px 12px;
	    font-size: 14px;
	    border-radius: 4px;
	    border: none;
	    color: white;
	    cursor: pointer;
	  }
	  
	  .accept-btn {
	    background-color: #5cb85c;
	    color: #fff;
	  }
	
	  .cancel-btn {
	    background-color: #dc3545;
	    color: #fff;
	  }
	  
	.emergency-box {
	  position: fixed;
	  top: 50%;
	  left: 50%;
	  transform: translate(-50%, -50%);
	  width: 430px;
	  padding: 20px;
	  background-color: white;
	  color: black;
	  text-align: center;
	  font-size: 14px;
	  border-radius: 5px;
	  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
	}
	
	.emergency-box input[type="text"],
	.emergency-box input[type="email"],
	.emergency-box select {
	  padding: 5px;
	  margin-bottom: 10px;
	  box-sizing: border-box;
	}
	
	.emergency-box label {
	  display: block;
	  text-align: left;
	  margin-bottom: 5px;
	}
	
	.emergency-box .row {
	  display: flex;
	  justify-content: space-between;
	  align-items: center;
	}
	
	.emergency-box .row .column {
	  flex-basis: 49%;
	}
	
	.emergency-box .row.justify-center {
	  justify-content: center;
	}
	
	.emergency-box button[type="submit"],
	.emergency-box button.cancel-button {
	  margin-top: 10px;
	  padding: 8px 10px;
	  font-size: 14px;
	}
	
	.emergency-box .cancel-button {
	  background-color: #ccc;
	  color: black;
	  border: none;
	}
	
	.emergency-box .cancel-button:hover {
	  background-color: #999;
	}
	
	  /* Estilo para el fondo semitransparente */
	  #overlay {
	    position: fixed;
	    top: 0;
	    left: 0;
	    width: 100%;
	    height: 100%;
	    background-color: rgba(0, 0, 0, 0.5); /* Color de fondo semitransparente (negro con opacidad 0.5) */
	    z-index: 999; /* Z-index alto para que esté por encima del contenido */
	    display: none; /* Ocultar inicialmente */
	  }
	
	  /* Estilo para el cuadro de edición */
	  .edit-box {
	    position: fixed;
	    top: 50%;
	    left: 50%;
	    transform: translate(-50%, -50%);
	    background-color: white;
	    padding: 40px;
	    border-radius: 5px;
	    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
	    z-index: 1000;
	  }

	    .export-buttonss {
	        margin-top: 20px; /* Agregar espacio en la parte superior */
	    }
	</style>    
	</head>
	  <jsp:include page="menu.jsp" />
	<body>
	  <h1>CRUD de Personas</h1>          
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
		<input type="button" class="btn-csv btn-icon" value="CSV" onclick="location.href='export-csv-a.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-pdf btn-icon" value="PDF" onclick="location.href='export-pdf-a.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-xlsx btn-icon" value="XLSX" onclick="location.href='export-xlsx-a.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
	    <input type="button" class="btn-new" value="Nuevo" onclick="location.href='register.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; cursor: pointer; color: white; float: right;">
		<input type="button" class="btn-reactivate" value="Reactivar" onclick="location.href='delete.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; cursor: pointer; color: white; background-color: #1a73e8; float: right; margin-right: 8px;">
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
	      <th>Acciones</th>
	    </tr>
	    <% while (rs.next()) {
	        String personId = rs.getString("id");
	        String names = rs.getString("names");
	        String lastName = rs.getString("last_name");
	        String typeDocument = rs.getString("type_document");
	        String numberDocument = rs.getString("number_document");
	        String email = rs.getString("email");
	        String cellPhone = rs.getString("cell_phone");
	        String rol = rs.getString("rol");
	        String active = rs.getString("active");
	        String rolText;
	        if (rol.equals("ES")) {
	          rolText = "Estudiante";
	        } else if (rol.equals("AP")) {
	          rolText = "Apoderado";
	        } else if (rol.equals("PR")) {
	          rolText = "Profesor";
	        } else if (rol.equals("PA")) {
	            rolText = "Personal";
	        } else {
	          rolText = "Desconocido";
	        }
	        String typeDocumentText;
	        if (typeDocument.equals("DNI")) {
	          typeDocumentText = "DNI";
	        } else if (typeDocument.equals("CNT")) {
	          typeDocumentText = "Carnet";
	        } else if (typeDocument.equals("PPE")) {
	          typeDocumentText = "Pasaporte";
	        } else {
	          typeDocumentText = "Desconocido";
	        }
	        // Omitir las filas inactivas
	        if (active.equals("I")) {
	            continue;
	        }
	    %>
		<tr>
		  <td><%= personId %></td>
		  <td><%= names %></td>
		  <td><%= lastName %></td>
		  <td><%= typeDocumentText %></td>
		  <td><%= numberDocument %></td>
		  <td><%= email %></td>
		  <td><%= cellPhone %></td>
		  <td><%= rolText %></td>
		  <td>
	<button class="edit-btn" id="edit-button" onclick="showEditOverlay('<%= rs.getInt("id") %>', '<%= names %>', '<%= lastName %>', '<%= typeDocument %>', '<%= numberDocument %>', '<%= email %>', '<%= cellPhone %>', '<%= rol %>')">Editar</button>
		    <button class="delete-btn" onclick="deletePerson('<%= personId %>')">Eliminar</button>
	      </td>
	    </tr>
	    <% } %>
	  </table>
	<div id="overlay" onclick="event.stopPropagation()"></div>

	<form id="edit-form" class="edit-box emergency-box" style="display: none;" action="actualizar.jsp" method="POST">
		  <input type="hidden" id="edit-id" name="id">
		<h2>Modificar Persona</h2>
	  <h3>Ingresa los nuevos datos:</h3>
	  <div class="row">
	    <div class="column">
	      <label>Nombres:</label>
	      <input type="text" id="edit-names" name="names" style="width: 100%;" pattern="[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+" required title="Ingrese un nombre válido (solo letras y espacios)">
	    </div>
	    <div class="column">
	      <label>Apellido:</label>
	      <input type="text" id="edit-lastname" name="lastname" style="width: 100%;" pattern="[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+" required title="Ingrese apellidos válidos (solo letras y espacios)">
	    </div>
	  </div>
	<div class="row">
	  <div class="column">
	    <label>Tipo de Documento:</label>
	    <select id="edit-typedocument" name="typedocument" style="width: 100%;" onchange="updateDocumentPattern()">
	      <option value="DNI">DNI</option>
	      <option value="PPE">Pasaporte</option>
	      <option value="CNT">Carnet</option>
	    </select>
	  </div>
	  <div class="column">
	    <label>Número de Documento:</label>
	    <input type="text" id="edit-numberdocument" name="numberdocument" style="width: 100%;" required>
	  </div>
	</div>
	
	<script>
	function updateDocumentPattern() {
	  const selectedType = document.getElementById("edit-typedocument").value;
	  const numberDocumentInput = document.getElementById("edit-numberdocument");
	
	  if (selectedType === "DNI") {
	    numberDocumentInput.pattern = "\\d{8}";
	    numberDocumentInput.title = "Ingrese un número de DNI válido (8 dígitos)";
	  } else if (selectedType === "CNT") {
	    numberDocumentInput.pattern = "\\d{10}";
	    numberDocumentInput.title = "Ingrese un número de Carnet válido (10 dígitos)";
	  } else if (selectedType === "PPE") {
	    numberDocumentInput.pattern = "\\d{15}";
	    numberDocumentInput.title = "Ingrese un número de Pasaporte válido (15 dígitos)";
	  }
	}
	</script>

	  <div class="row">
	    <div class="column">
	      <label>Email:</label>
	      <input type="email" id="edit-email" name="email" style="width: 100%; border: 1px solid #ccc; border-radius: 4px;">
	    </div>
	    <div class="column">
	      <label>Teléfono Celular:</label>
			<input type="text" id="edit-cellphone" name="cellphone" style="width: 100%;" pattern="\d{9}" required title="Ingrese un número de teléfono celular válido (mínimo 9 dígitos)">
			
			<script>
			document.getElementById("edit-cellphone").addEventListener("input", function() {
			  const input = this.value;
			  const startsWith9 = input.startsWith("9");
			
			  if (input.length === 0) {
			    this.setCustomValidity(""); // Clear any previous validation message
			  } else if (!startsWith9) {
			    this.setCustomValidity("El número de celular debe comenzar con 9.");
			  } else if (input.length < 9) {
			    this.setCustomValidity("Ingrese un número de teléfono celular válido (mínimo 9 dígitos)");
			  } else {
			    this.setCustomValidity(""); // Clear any previous validation message
			  }
			});
			</script>
	    </div>
	  </div>
	  <div class="row justify-center">
	    <div class="column">
	      <label>Rol:</label>
	      <select id="edit-rol" name="rol">
	        <option value="ES">Estudiante</option>
	        <option value="AP">Apoderado</option>
	        <option value="PR">Profesor</option>
	        <option value="PA">Personal</option>
	      </select>
	    </div>
	    <div class="column">
	      <button type="submit"  style="background-color: #1a73e8; border: none; color: white; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin-right: 5px; cursor: pointer; border-radius: 4px;">Actualizar</button>
	      <button type="button" class="cancel-button" onclick="window.location.href='edit.jsp'" style="background-color: #FF4136; border: none; color: white; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin-right: -16px; cursor: pointer; border-radius: 4px;">Cancelar</button>
	    </div>
	  </div>
	</form>
	
	    <!-- Agregar los botones CSV, PDF y XLSX aquí -->
	  <div class="export-buttonss">
		<input type="button" class="btn-csv btn-icon" value="CSV" onclick="location.href='export-csv.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-pdf btn-icon" value="PDF" onclick="location.href='export-pdf.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
		<input type="button" class="btn-xlsx btn-icon" value="XLSX" onclick="location.href='export-xlsx.jsp';" style="padding: 5px 10px; font-size: 14px; border-radius: 4px; border: none; color: white; cursor: pointer;">
	  </div>
	
	<script>
	  function showEditOverlay(id, names, lastName, typeDocument, numberDocument, email, cellPhone, rol) {
	    // Mostrar el cuadro de edición
	    document.getElementById('edit-form').style.display = 'block';
	
	    // Rellenar los campos del formulario con los datos actuales
	    document.getElementById('edit-id').value = id;
	    document.getElementById('edit-names').value = names;
	    document.getElementById('edit-lastname').value = lastName;
	    document.getElementById('edit-typedocument').value = typeDocument;
	    document.getElementById('edit-numberdocument').value = numberDocument;
	    document.getElementById('edit-email').value = email;
	    document.getElementById('edit-cellphone').value = cellPhone;
	    document.getElementById('edit-rol').value = rol;
	
	    // Mostrar el fondo semitransparente
	    document.getElementById('overlay').style.display = 'block';
	  }
	
	  function hideEditOverlay() {
	    // Ocultar el cuadro de edición
	    document.getElementById('edit-form').style.display = 'none';
	
	    // Ocultar el fondo semitransparente
	    document.getElementById('overlay').style.display = 'none';
	  }
	</script>
	<script>
	  // Obtener referencias a los elementos del formulario
	  const form = document.getElementById('edit-form');
	  const updateButton = document.querySelector('#edit-form button[type="submit"]');
	  const inputs = form.querySelectorAll('input, select');
	
	  // Guardar los valores iniciales de los campos del formulario
	  const initialFieldValues = Array.from(inputs).reduce((values, input) => {
	    values[input.name] = input.value;
	    return values;
	  }, {});
	
	  // Verificar si se han realizado modificaciones en los campos del formulario
	  const hasModifications = () => {
	    for (let input of inputs) {
	      if (input.value !== initialFieldValues[input.name]) {
	        return true;
	      }
	    }
	    return false;
	  };
	
	  // Actualizar estado del botón "Actualizar"
	  const updateButtonState = () => {
	    if (hasModifications()) {
	      updateButton.disabled = false;
	      updateButton.style.backgroundColor = '#1a73e8';  // Color activo (celeste)
	      updateButton.style.color = '#ffffff';  // Color del texto activo (blanco)
	      updateButton.style.cursor = 'pointer';  // Cursor apuntador
	    } else {
	      updateButton.disabled = true;
	      updateButton.style.backgroundColor = '#e0e0e0';  // Color inactivo (gris claro)
	      updateButton.style.color = '#555555';  // Color del texto inactivo (#555555)
	      updateButton.style.cursor = 'default';  // Cursor predeterminado
	    }
	  };
	
	  // Escuchar el evento 'input' en los campos del formulario
	  inputs.forEach((input) => {
	    input.addEventListener('input', updateButtonState);
	  });
	
	  // Actualizar estado del botón al cargar la página
	  updateButtonState();
	</script>
	
	  	<script>
	  	function editPerson(id, names, lastName, typeDocument, numberDocument, email, cellPhone, rol) {
	  	  // Asignar los valores a los campos del formulario
	  	  document.getElementById("edit-id").value = id;
	  	  document.getElementById("edit-names").value = names;
	  	  document.getElementById("edit-lastname").value = lastName;
	  	  document.getElementById("edit-typedocument").value = typeDocument;
	  	  document.getElementById("edit-numberdocument").value = numberDocument;
	  	  document.getElementById("edit-email").value = email;
	  	  document.getElementById("edit-cellphone").value = cellPhone;
	  	  document.getElementById("edit-rol").value = rol;
	  	  
	  	  // Mostrar el formulario de edición
	  	  document.getElementById("edit-form").style.display = "block";
	  	}
	
		</script>
	  <!-- Agrega este código en la sección <script> del archivo JSP -->
		<script>
		  function deletePerson(personId) {
		    var confirmationDialog = document.createElement('div');
		    confirmationDialog.className = 'confirmation-dialog';
		
		    var confirmationDialogContent = document.createElement('div');
		    confirmationDialogContent.className = 'confirmation-dialog-content';
		
		    var confirmationDialogTitle = document.createElement('h3');
		    confirmationDialogTitle.innerHTML = 'Confirmación';
		
		    var confirmationDialogText = document.createElement('p');
		    confirmationDialogText.innerHTML = '¿Estás seguro de realizar esta acción?';
		
		    var confirmationDialogButtons = document.createElement('div');
		    confirmationDialogButtons.className = 'confirmation-dialog-buttons';
		
		    var confirmButton = document.createElement('button');
		    confirmButton.className = 'accept-btn';
		    confirmButton.innerHTML = 'Aceptar';
		    confirmButton.addEventListener('click', function() {
		      updateStatus(personId);
		      document.body.removeChild(confirmationDialog);
		    });
		
		    var cancelButton = document.createElement('button');
		    cancelButton.className = 'cancel-btn';
		    cancelButton.innerHTML = 'Cancelar';
		    cancelButton.addEventListener('click', function() {
		      document.body.removeChild(confirmationDialog);
		    });
		
		    confirmationDialogButtons.appendChild(confirmButton);
		    confirmationDialogButtons.appendChild(cancelButton);
		
		    confirmationDialogContent.appendChild(confirmationDialogTitle);
		    confirmationDialogContent.appendChild(confirmationDialogText);
		    confirmationDialogContent.appendChild(confirmationDialogButtons);
		
		    confirmationDialog.appendChild(confirmationDialogContent);
		
		    document.body.appendChild(confirmationDialog);
		  }
		
		  function updateStatus(personId) {
		    // Realizar la solicitud AJAX para actualizar el estado a "Inactivo"
		    var xhr = new XMLHttpRequest();
		    xhr.onreadystatechange = function() {
		      if (xhr.readyState === 4 && xhr.status === 200) {
		        // Recargar la página después de la actualización
		        location.reload();
		      }
		    };
		    xhr.open('POST', 'actualizarEstado.jsp', true);
		    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		    xhr.send('id=' + personId + '&estado=I');
		  }
		</script>
	</body>
	</html>
	
	<%
	  } catch (Exception e) {
	    e.printStackTrace();
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
