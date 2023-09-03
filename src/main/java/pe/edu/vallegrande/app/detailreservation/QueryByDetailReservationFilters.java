package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class QueryByDetailReservationFilters {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar registros por filtros
            String sql = "SELECT * FROM detail_reservation WHERE reservation_id = ? AND book_id = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setInt(1, 1); // ID de la reserva
            statement.setInt(2, 2); // ID del libro

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Imprimir los resultados en columnas divididas
            System.out.println("============================================");
            System.out.printf("%-4s | %-12s | %-9s | %-8s%n",
                    "ID", "Reserva ID", "Libro ID", "Cantidad");
            System.out.println("============================================");
            while (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                int reservationId = resultSet.getInt("reservation_id");
                int bookId = resultSet.getInt("book_id");
                int quantity = resultSet.getInt("quantity");

                // Mostrar los datos del registro en columnas divididas
                System.out.printf("%-4d | %-12d | %-9d | %-8s%n",
                        id, reservationId, bookId, quantity);
            }
            System.out.println("============================================");

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
