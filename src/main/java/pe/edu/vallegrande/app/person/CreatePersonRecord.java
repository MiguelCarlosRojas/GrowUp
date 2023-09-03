package pe.edu.vallegrande.app.person;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class CreatePersonRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para insertar un registro
            String sql = "INSERT INTO person (names, last_name, type_document, number_document, email, cell_phone, rol, active) " +
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setString(1, "John");  // Nombre de la persona
            statement.setString(2, "Doe");  // Apellido de la persona
            statement.setString(3, "DNI");  // Tipo de identificación (por ejemplo, 'DNI' DNI, 'CNT' Carnet 'PPE' Pasaporte, etc.)
            statement.setString(4, "12345678");  // Número de identificación 'DNI' 8, 'CNT' 10, 'PPE' 15
            statement.setString(5, "johndoe@example.com");  // Dirección de correo electrónico de la persona
            statement.setString(6, "923456789");  // Número de teléfono de la persona
            statement.setString(7, "ES");  // Rol de la persona (por ejemplo, 'ES' Estudiante, 'AP' Apoderado, 'PR' Profesor, 'PA' Personal Administrativo)
            statement.setString(8, "A");  // Estado de la persona (por ejemplo, A para activo o I para inactivo)

            // Ejecutar la consulta
            int filasInsertadas = statement.executeUpdate();

            // Verificar si se insertó el registro exitosamente
            if (filasInsertadas > 0) {
                System.out.println("Registro insertado correctamente.");
            } else {
                System.out.println("No se pudo insertar el registro.");
            }

            // Cerrar el PreparedStatement
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