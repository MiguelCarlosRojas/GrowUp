package pe.edu.vallegrande.app.reservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class ModifyReservationRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para modificar un registro
            String sql = "UPDATE reservation SET person_id = ?, date_available = ?, date_return = ?, observations = ? WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setInt(1, 3);  // ID de la persona que realiza la reserva
            statement.setString(2, "2023-08-25");  // Fecha en que el libro reservado está disponible
            statement.setString(3, "2023-10-30");  // Fecha en la que se debe devolver el libro reservado
            statement.setString(4, "Reserva para lectura");  // Observaciones adicionales o notas para la reserva
            statement.setInt(5, 3); // ID del registro a modificar

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