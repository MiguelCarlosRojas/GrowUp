package pe.edu.vallegrande.app.person;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.db.AccesoDBCloud;


import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class QueryByPersonFilters {
    public static void main(String[] args) {
        Connection connection = null;
        try {
            // Establecer la conexión
            connection = AccesoDBLocal.getConnection();
            System.out.println("Conexión exitosa a la base de datos.");

            // Definir la consulta SQL para consultar un registro por filtros
            String sql = "SELECT * FROM person WHERE type_document = ? AND active = ?";

            // Crear un PreparedStatement con la consulta SQL
            PreparedStatement statement = connection.prepareStatement(sql);

            // Establecer los valores de los parámetros
            statement.setString(1, "DNI"); // Tipo de documento
            statement.setString(2, "A"); // Activo

            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            // Imprimir los resultados en columnas divididas
            System.out.println("======================================================================================================================================================================");
            System.out.printf("%-4s | %-20s | %-20s | %-20s | %-10s | %-33s | %-15s | %-5s | %-6s%n",
                    "ID", "Nombres", "Apellido", "Tipo Documento", "Número Documento", "Email", "Celular", "Rol", "Activo");
            System.out.println("======================================================================================================================================================================");
            while (resultSet.next()) {
                // Leer los datos del registro
                int id = resultSet.getInt("id");
                String names = resultSet.getString("names");
                String lastName = resultSet.getString("last_name");
                String typeDocument = resultSet.getString("type_document");
                String numberDocument = resultSet.getString("number_document");
                String email = resultSet.getString("email");
                String cellPhone = resultSet.getString("cell_phone");
                String rol = resultSet.getString("rol");
                String active = resultSet.getString("active");

                // Mostrar los datos del registro en columnas divididas
                System.out.printf("%-4d | %-20s | %-20s | %-20s | %-16s | %-33s | %-15s | %-5s | %-6s%n",
                        id, names, lastName, typeDocument, numberDocument, email, cellPhone, rol, active);
            }
            System.out.println("======================================================================================================================================================================");

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