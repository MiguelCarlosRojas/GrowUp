package pe.edu.vallegrande.app.person;

import java.sql.Connection;

import pe.edu.vallegrande.app.db.AccesoDBCloud;

public class SQLServerConnectionCloud {
	
	public static void main(String[] args) {
		try {
			Connection cn = AccesoDBCloud.getConnection();
			System.out.println("Conexión ok.");
			cn.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
