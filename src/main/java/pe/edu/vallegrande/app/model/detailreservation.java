package pe.edu.vallegrande.app.model;

public class detailreservation {
    private Integer id;
    private Integer reservationId;
    private Integer bookId;
    private Integer quantity;
    private String reason;

    public detailreservation() {
    }

    public detailreservation(Integer id, Integer reservationId, Integer bookId, Integer quantity, String reason) {
        this.id = id;
        this.reservationId = reservationId;
        this.bookId = bookId;
        this.quantity = quantity;
        this.reason = reason;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getReservationId() {
        return reservationId;
    }

    public void setReservationId(Integer reservationId) {
        this.reservationId = reservationId;
    }

    public Integer getBookId() {
        return bookId;
    }

    public void setBookId(Integer bookId) {
        this.bookId = bookId;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    public String getReason() {
        return reason;
    }

    public void setReason(String reason) {
        this.reason = reason;
    }

    @Override
    public String toString() {
        return "DetailReservation{" +
                "id=" + id +
                ", reservationId=" + reservationId +
                ", bookId=" + bookId +
                ", quantity=" + quantity +
                ", reason='" + reason + '\'' +
                '}';
    }
}
