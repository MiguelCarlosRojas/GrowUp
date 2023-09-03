package pe.edu.vallegrande.app.reservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ConsultTotalReservationRecords {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar todos los registros
            String sql = "SELECT * FROM reservation";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Mostrar los resultados en columnas divididas
            System.out.println("====================================================================================================================================");
            String header = String.format("%-4s | %-10s | %-23s | %-12s | %-12s | %-1s | %-26s | %-20s",
                    "ID", "Person ID", "Fecha Y Hora de la Reserva", "Fecha Disponible", "Fecha Regreso", "Estado", "Observaciones", "Activo");
            System.out.println(header);
            System.out.println("====================================================================================================================================");
            while (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                int personId = resultSet.getInt("person_id");
                String dateReservation = resultSet.getString("date_reservation");
                String dateAvailable = resultSet.getString("date_available");
                String dateReturn = resultSet.getString("date_return");
                String status = resultSet.getString("status");
                String observations = resultSet.getString("observations");
                String active = resultSet.getString("active");

                // Mostrar los datos del registro en columnas divididas
                String row = String.format("%-4d | %-10d | %-26s | %-16s | %-13s | %-6s | %-26s | %-20s",
                        id, personId, dateReservation, dateAvailable, dateReturn, status, observations, active);
                System.out.println(row);
            }
            System.out.println("====================================================================================================================================");

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
