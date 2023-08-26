package pe.edu.vallegrande.app.controller;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.http.HttpServletResponse;

public class ControllerUtil {
	
	private ControllerUtil() {
	}
	
	public static void responseJson(HttpServletResponse response, String data) throws IOException {
		PrintWriter out = response.getWriter();
		response.setContentType("application/json");
		response.setCharacterEncoding("UTF-8");
		out.print(data);
		out.flush();
	}

}