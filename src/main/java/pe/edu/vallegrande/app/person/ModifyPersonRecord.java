package pe.edu.vallegrande.app.person;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class ModifyPersonRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para modificar un registro
            String sql = "UPDATE person SET names = ?, last_name = ?, type_document = ?, number_document = ?, " +
                    "email = ?, cell_phone = ?, rol = ?, active = ? WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setString(1, "Chessi");  // Nombre de la persona
            statement.setString(2, "Vt");  // Apellido de la persona
            statement.setString(3, "CNT");  // Tipo de identificación (por ejemplo, 'DNI' DNI, 'CNT' Carnet 'PPE' Pasaporte, etc.)
            statement.setString(4, "9876543282");  // Número de identificación 'DNI' 8, 'CNT' 10, 'PPE' 15
            statement.setString(5, "chessi.vt@universidad.edu");  // Dirección de correo electrónico de la persona
            statement.setString(6, "987654321");  // Número de teléfono de la persona
            statement.setString(7, "PR");  // Rol de la persona (por ejemplo, 'ES' Estudiante, 'AP' Apoderado, 'PR' Profesor, 'PA' Personal Administrativo)
            statement.setString(8, "A");  // Estado de la persona (por ejemplo, A para activo o I para inactivo)
            statement.setInt(9, 1); // ID del registro a modificar

            // Ejecutar la consulta
            int filasModificadas = statement.executeUpdate();

            // Verificar si se modificó el registro exitosamente
            if (filasModificadas > 0) {
                System.out.println("Registro modificado correctamente.");
            } else {
                System.out.println("No se pudo modificar el registro.");
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