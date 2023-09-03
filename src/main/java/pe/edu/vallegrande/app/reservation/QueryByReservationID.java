package pe.edu.vallegrande.app.reservation;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class QueryByReservationID {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar un registro por ID
            String sql = "SELECT * FROM reservation WHERE id = ?";

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
                int personId = resultSet.getInt("person_id");
                String dateReservation = resultSet.getString("date_reservation");
                String dateAvailable = resultSet.getString("date_available");
                String dateReturn = resultSet.getString("date_return");
                String status = resultSet.getString("status");
                String observations = resultSet.getString("observations");
                String active = resultSet.getString("active");


                // Mostrar los datos del registro
                System.out.println("ID: " + id);
                System.out.println("Person ID: " + personId);
                System.out.println("Fecha Y Hora de la Reserva: " + dateReservation);
                System.out.println("Fecha Disponible: " + dateAvailable);
                System.out.println("Fecha Regreso: " + dateReturn);
                System.out.println("Estado: " + status);                
                System.out.println("Observaciones: " + observations);
                System.out.println("Activo: " + active);
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
