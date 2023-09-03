package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class ModifyDetailReservationRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para modificar un registro
            String sql = "UPDATE detail_reservation SET reservation_id = ?, book_id = ?, quantity = ? WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setInt(1, 1);  // ID de la reserva
            statement.setInt(2, 2);  // ID del libro
            statement.setInt(3, 5);  // Cantidad
            statement.setInt(4, 1); // ID del registro a modificar

            // Ejecutar la consulta
            int rowsModified = statement.executeUpdate();

            // Verificar si se modificó el registro exitosamente
            if (rowsModified > 0) {
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
