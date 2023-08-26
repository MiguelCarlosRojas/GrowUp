package pe.edu.vallegrande.app.reservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class CreateReservationRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para insertar un registro
            String sql = "INSERT INTO reservation (person_id, date_available, date_return, observations) " +
                    "VALUES (?, ?, ?, ?)";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setInt(1, 5);  // ID de la persona que realiza la reserva
            statement.setString(2, "2023-08-23");  // Fecha en que el libro reservado está disponible
            statement.setString(3, "2023-10-14");  // Fecha en la que se debe devolver el libro reservado
            statement.setString(4, "Reserva para vacaciones");  // Observaciones adicionales o notas para la reserva

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