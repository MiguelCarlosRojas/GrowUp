package pe.edu.vallegrande.app.book;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class ConsultTotalBookRecords {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Consultar todos los registros en la tabla "book"
            String selectAllQuery = "SELECT id, title, catalogs, isbn, location, number_copies, active FROM book";

            // Crear un PreparedStatement con la consulta para seleccionar todos los registros
            PreparedStatement selectAllStatement = connection.prepareStatement(selectAllQuery);

            // Ejecutar la consulta para seleccionar todos los registros
            ResultSet selectAllResultSet = selectAllStatement.executeQuery();

            // Mostrar los resultados en una tabla
            System.out.println("=== Registros en la tabla book ===");
            System.out.println("|  ID |          Título	  		|  Catálogos  |      ISBN     |    Ubicación   | Número de Copias | Estado |");
            while (selectAllResultSet.next()) {
                int id = selectAllResultSet.getInt("id");
                String title = selectAllResultSet.getString("title");
                String catalogs = selectAllResultSet.getString("catalogs");
                String isbn = selectAllResultSet.getString("isbn");
                String location = selectAllResultSet.getString("location");
                int numberCopies = selectAllResultSet.getInt("number_copies");
                String active = selectAllResultSet.getString("active");

                System.out.printf("| %3d | %-31s | %-11s | %-13s | %-14s | %16d | %6s |\n",
                        id, title, catalogs, isbn, location, numberCopies, active);
            }
            System.out.println("--------------------------------------------------------------------------------------------------------------------");

            // Cerrar el ResultSet y el PreparedStatement
            selectAllResultSet.close();
            selectAllStatement.close();

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