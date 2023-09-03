package pe.edu.vallegrande.app.model;

public class person {

	private Integer id;
	private String names;
	private String last_name;
	private String type_document;
	private String number_document;
	private String email;
	private String cell_phone;
	private String rol;
	private String active;
	
	
	public person() {
	}

	public person(Integer id, String names, String last_name, String type_document, String number_document, String email, String cell_phone, String rol, String active) {
		super();
		this.id = id;
		this.names = names;
		this.last_name = last_name;
		this.type_document = type_document;
		this.number_document = number_document;
		this.email = email;
		this.cell_phone = cell_phone;
		this.rol = rol;
		this.active = active;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getNames() {
		return names;
	}

	public void setNames(String names) {
		this.names = names;
	}

	public String getLast_Name() {
		return last_name;
	}

	public void setLast_Name(String last_name) {
		this.last_name = last_name;
	}

	public String getType_Document() {
		return type_document;
	}

	public void setType_Document(String type_document) {
		this.type_document = type_document;
	}

	public String getNumber_Document() {
		return number_document;
	}
	
	public void setNumber_Document(String number_document) {
		this.number_document = number_document;
	}
	
	public String getEmail() {
		return email;
	}
	
	public void setEmail(String email) {
		this.email = email;
	}

	public String getCell_Phone() {
		return cell_phone;
	}
	
	public void setCell_Phone(String cell_phone) {
		this.cell_phone = cell_phone;
	}
	
	public String getRol() {
		return rol;
	}
	
	public void setRol(String rol) {
		this.rol = rol;
	}

	public String getActive() {
		return active;
	}
	
	public void setActive(String active) {
		this.active = active;
	}
	
	@Override
	public String toString() {
		String data = "[id: " + this.id;
		data += ", names: " + this.names;
		data += ", last_name: " + this.last_name;
		data += ", type_document: " + this.type_document;
		data += ", number_document:" + this.number_document;
		data += ", email: " + this.email;
		data += ", cell_phone:" + this.cell_phone;
		data += ", rol:" + this.rol;
		data += ", active:" + this.active + "]";
		return data;
	}
}