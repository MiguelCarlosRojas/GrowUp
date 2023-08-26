package pe.edu.vallegrande.app.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class AccesoDBCloud {
	private static final String URL = "jdbc:sqlserver://serverdatabase19.database.windows.net:1433;database=dbGrowUp;user=dbGrowUp;password=MiguelAngel12";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL);
    }
}