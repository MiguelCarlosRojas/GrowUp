package pe.edu.vallegrande.app.detailreservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ConsultTotalDetailReservationRecords {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar todos los registros
            String sql = "SELECT * FROM detail_reservation";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Mostrar los resultados en columnas divididas
            System.out.println("=========================================");
            String header = String.format("%-4s | %-10s | %-2s | %-8s |",
                    "ID", "Reserva ID", "Libro ID", "Cantidad");
            System.out.println(header);
            System.out.println("=========================================");
            while (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                int reservationId = resultSet.getInt("reservation_id");
                int bookId = resultSet.getInt("book_id");
                int quantity = resultSet.getInt("quantity");

                // Mostrar los datos del registro en columnas divididas
                String row = String.format("%-4s | %-10s | %-8s | %-8s |",
                        id, reservationId, bookId, quantity);
                System.out.println(row);
            }
            System.out.println("=========================================");

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
