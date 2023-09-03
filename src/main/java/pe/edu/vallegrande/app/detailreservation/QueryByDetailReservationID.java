package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class QueryByDetailReservationID {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar un registro por ID
            String sql = "SELECT * FROM detail_reservation WHERE id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer el valor del parámetro
            statement.setInt(1, 2); // ID del registro a consultar

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Verificar si se encontró el registro
            if (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                int reservationId = resultSet.getInt("reservation_id");
                int bookId = resultSet.getInt("book_id");
                int quantity = resultSet.getInt("quantity");

                // Mostrar los datos del registro
                System.out.println("ID: " + id);
                System.out.println("Reserva ID: " + reservationId);
                System.out.println("Libro ID: " + bookId);
                System.out.println("Cantidad: " + quantity);
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
