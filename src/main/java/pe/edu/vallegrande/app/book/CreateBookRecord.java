package pe.edu.vallegrande.app.book;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class CreateBookRecord {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para insertar un nuevo registro
            String sql = "INSERT INTO book (title, catalogs, location, number_copies) VALUES (?, ?, ?, ?)";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros para el nuevo registro
            statement.setString(1, "Astronomía Básica"); // Valor del title
            statement.setString(2, "Ciencias"); // Valor del catalogs
            statement.setString(3, "Estantería D1"); // Valor del location
            statement.setInt(4, 4); // Valor del number_copies

            // Ejecutar la consulta para insertar el nuevo registro
            int rowsInserted = statement.executeUpdate();

            if (rowsInserted > 0) {
                System.out.println("Registro creado exitosamente.");
            } else {
                System.out.println("No se pudo crear el registro.");
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