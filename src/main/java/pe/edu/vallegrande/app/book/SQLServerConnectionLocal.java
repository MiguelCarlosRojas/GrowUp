package pe.edu.vallegrande.app.book;

import java.sql.Connection;

import pe.edu.vallegrande.app.db.AccesoDBLocal;

public class SQLServerConnectionLocal {
	
	public static void main(String[] args) {
		try {
			Connection cn = AccesoDBLocal.getConnection();
			System.out.println("Conexión ok.");
			cn.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
