package pe.edu.vallegrande.app.person;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class QueryByPersonID {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar un registro por ID
            String sql = "SELECT * FROM person WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer el valor del parámetro
            statement.setInt(1, 3); // ID del registro a consultar

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Verificar si se encontró el registro
            if (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                String names = resultSet.getString("names");
                String lastName = resultSet.getString("last_name");
                String typeDocument = resultSet.getString("type_document");
                String numberDocument = resultSet.getString("number_document");
                String email = resultSet.getString("email");
                String cellPhone = resultSet.getString("cell_phone");
                String rol = resultSet.getString("rol");
                String active = resultSet.getString("active");

                // Mostrar los datos del registro
                System.out.println("ID: " + id);
                System.out.println("Nombres: " + names);
                System.out.println("Apellido: " + lastName);
                System.out.println("Tipo de documento: " + typeDocument);
                System.out.println("Número de documento: " + numberDocument);
                System.out.println("Email: " + email);
                System.out.println("Celular: " + cellPhone);
                System.out.println("Rol: " + rol);
                System.out.println("Activo: " + active);
            } else {
                System.out.println("No se encontró el registro.");
            }

            // Cerrar el ResultSet y PreparedStatement
            resultSet.close();
            statement.close();

        } catch (SQLException e) {
            System.out.println("Error al conectar a la base de datos: " + e.getMessage());
        } finally {
            try {
                // Cerrar la conexión
                if (connection != null) {
                    connection.close();
                }
            } catch (SQLException e) {
                System.out.println("Error al cerrar la conexión: " + e.getMessage());
            }
        }
    }
}