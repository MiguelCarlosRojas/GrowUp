package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DeleteDetailReservationRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para eliminar un registro
            String sql = "DELETE FROM detail_reservation WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer el valor del parámetro
            statement.setInt(1, 1); // ID del registro a eliminar

            // Ejecutar la consulta
            int filasEliminadas = statement.executeUpdate();

            // Verificar si se eliminó el registro exitosamente
            if (filasEliminadas > 0) {
                System.out.println("Registro eliminado correctamente.");
            } else {
                System.out.println("No se pudo eliminar el registro.");
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
