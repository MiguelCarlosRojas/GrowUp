package pe.edu.vallegrande.app.book;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class ModifyBookRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para modificar un registro existente por ID
            String sql = "UPDATE book SET title = ?, catalogs = ?, isbn = ?, location = ?, number_copies = ? WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros para la modificación del registro
            statement.setString(1, "Análisis Financiero"); // Valor del title
            statement.setString(2, "Economía"); // Valor del catalogs
            statement.setString(3, "9780123456789"); // Valor del isbn
            statement.setString(4, "Estantería I5"); // Valor del location
            statement.setInt(5, 3); // Valor del number_copies
            statement.setInt(6, 7); // Valor del ID del registro a modificar

            // Ejecutar la consulta para modificar el registro
            int rowsUpdated = statement.executeUpdate();

            if (rowsUpdated > 0) {
                System.out.println("Registro modificado exitosamente.");
            } else {
                System.out.println("No se pudo modificar el registro. Verifica el ID.");
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