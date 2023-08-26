package pe.edu.vallegrande.app.model;

public class book {

	private Integer id;
	private String title;
	private String catalogs;
	private String isbn;
	private String location;
	private int number_copies;
	private String status;
	
	
	public book() {
	}

	public book(Integer id, String title, String catalogs, String isbn, String location, int number_copies, String status) {
		super();
		this.id = id;
		this.title = title;
		this.catalogs = catalogs;
		this.isbn = isbn;
		this.location = location;
		this.number_copies = number_copies;
		this.status = status;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getCatalogs() {
		return catalogs;
	}

	public void setCatalogs(String catalogs) {
		this.catalogs = catalogs;
	}

	public String getIsbn() {
		return isbn;
	}

	public void setIsbn(String isbn) {
		this.isbn = isbn;
	}

	public String getLocation() {
		return location;
	}
	
	public void setLocation(String location) {
		this.location = location;
	}
	
	public int getNumber_Copies() {
		return number_copies;
	}
	
	public void setNumber_Copies(int number_copies) {
		this.number_copies = number_copies;
	}

	public String getStatus() {
		return status;
	}
	
	public void setStatus(String status) {
		this.status = status;
	}
	
	@Override
	public String toString() {
		String data = "[id: " + this.id;
		data += ", title: " + this.title;
		data += ", catalogs: " + this.catalogs;
		data += ", isbn: " + this.isbn;
		data += ", location:" + this.location;
		data += ", number_copies: " + this.number_copies;
		data += ", status:" + this.status + "]";
		return data;
	}
}