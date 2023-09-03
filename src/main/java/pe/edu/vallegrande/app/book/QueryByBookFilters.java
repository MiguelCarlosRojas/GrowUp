package pe.edu.vallegrande.app.book;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;


public class QueryByBookFilters {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL con los filtros deseados
            String sql = "SELECT * FROM book WHERE catalogs = ? AND active = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros para la consulta
            statement.setString(1, "Arte"); // Valor del filtro de catálogos
            statement.setString(2, "A"); // Valor del filtro de estado "Inactivo" (I) o "Activo" (A)

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Crear una tabla para mostrar los resultados
            System.out.println("+----+----------------------+--------------+---------------+----------------+------------------+--------+");
            System.out.println("| ID |        Título        |   Catálogos  |      ISBN     |    Ubicación   | Número de copias | Estado |");
            System.out.println("+----+----------------------+--------------+---------------+----------------+------------------+--------+");

            while (resultSet.next()) {
                // Obtener los valores de las columnas del registro
                int id = resultSet.getInt("id");
                String title = resultSet.getString("title");
                String catalogs = resultSet.getString("catalogs");
                String isbn = resultSet.getString("isbn");
                String location = resultSet.getString("location");
                int numberCopies = resultSet.getInt("number_copies");
                String active = resultSet.getString("active");

                // Mostrar los valores del registro en la tabla
                System.out.printf("| %2d | %20s | %12s | %12s | %14s | %16d | %6s |%n", id, title, catalogs, isbn, location, numberCopies, active);
            }

            System.out.println("+----+----------------------+--------------+---------------+----------------+------------------+--------+");

            // Cerrar el ResultSet y el PreparedStatement
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