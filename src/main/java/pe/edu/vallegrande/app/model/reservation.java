package pe.edu.vallegrande.app.model;

import java.sql.Date;
import java.sql.Timestamp;

public class reservation {
    private Integer id;
    private Integer personId;
    private Timestamp dateReservation;
    private Date dateAvailable;
    private Date dateReturn;
    private String status;
    private String observations;
    private String active;

    public reservation() {
    }

    public reservation(Integer id, Integer personId, Timestamp dateReservation, Date dateAvailable,
                       Date dateReturn, String status, String observations, String active) {
        this.id = id;
        this.personId = personId;
        this.dateReservation = dateReservation;
        this.dateAvailable = dateAvailable;
        this.dateReturn = dateReturn;
        this.status = status;
        this.observations = observations;
        this.active = active;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getPersonId() {
        return personId;
    }

    public void setPersonId(Integer personId) {
        this.personId = personId;
    }

    public Timestamp getDateReservation() {
        return dateReservation;
    }

    public void setDateReservation(Timestamp timestamp) {
        this.dateReservation = timestamp;
    }

    public Date getDateAvailable() {
        return dateAvailable;
    }

    public void setDateAvailable(Date date) {
        this.dateAvailable = date;
    }

    public Date getDateReturn() {
        return dateReturn;
    }

    public void setDateReturn(Date date) {
        this.dateReturn = date;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getObservations() {
        return observations;
    }

    public void setObservations(String observations) {
        this.observations = observations;
    }

    public String getActive() {
        return active;
    }

    public void setActive(String active) {
        this.active = active;
    }

    @Override
    public String toString() {
        return "Reservation{" +
                "id=" + id +
                ", personId=" + personId +
                ", dateReservation=" + dateReservation +
                ", dateAvailable=" + dateAvailable +
                ", dateReturn=" + dateReturn +
                ", status='" + status + '\'' +
                ", observations='" + observations + '\'' +
                ", active='" + active + '\'' +
                '}';
    }
}
