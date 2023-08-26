package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class CreateDetailReservationRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para insertar un registro
            String sql = "INSERT INTO detail_reservation (reservation_id, book_id, quantity) " +
                    "VALUES (?, ?, ?)";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setInt(1, 2);  //ID de la reserva
            statement.setInt(2, 2);  // ID del libro que se reserva
            statement.setInt(3, 6);  // Cantidad de libros que se reservan

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
