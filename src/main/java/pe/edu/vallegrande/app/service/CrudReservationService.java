package pe.edu.vallegrande.app.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.model.reservation;
import pe.edu.vallegrande.app.service.spec.CrudServiceSpec;
import pe.edu.vallegrande.app.service.spec.RowMapper;

public class CrudReservationService implements CrudServiceSpec<reservation>, RowMapper<reservation> {

    // Definiendo consultas SQL
    private final String SQL_SELECT_BASE = "SELECT id, person_id, date_reservation, date_available, date_return, status, observations, active FROM reservation";
    private final String SQL_INSERT = "INSERT INTO reservation(person_id, date_reservation, date_available, date_return, status, observations, active) VALUES(?,?,?,?,?,?,?)";
    private final String SQL_UPDATE = "UPDATE reservation SET person_id=?, date_reservation=?, date_available=?, date_return=?, status=?, observations=?, active=? WHERE id=?";
    private final String SQL_DELETE = "DELETE FROM reservation WHERE id=?";

    @Override
    public List<reservation> getAll() {
        // Variables
        Connection cn = null;
        List<reservation> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        reservation bean;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            pstm = cn.prepareStatement(SQL_SELECT_BASE);
            rs = pstm.executeQuery();
            while (rs.next()) {
                bean = mapRow(rs);
                lista.add(bean);
            }
            rs.close();
            pstm.close();
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
        return lista;
    }

    @Override
    public reservation getForId(String id) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        ResultSet rs = null;
        reservation bean = null;
        String sql;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            sql = SQL_SELECT_BASE + " WHERE id=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, Integer.parseInt(id));
            rs = pstm.executeQuery();
            if (rs.next()) {
                bean = mapRow(rs);
            }
            rs.close();
            pstm.close();
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
        return bean;
    }

    @Override
    public List<reservation> get(reservation bean) {
        // Variables
        Connection cn = null;
        List<reservation> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        reservation item;
        String sql;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            sql = SQL_SELECT_BASE + " WHERE person_id=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, bean.getPersonId());
            rs = pstm.executeQuery();
            while (rs.next()) {
                item = mapRow(rs);
                lista.add(item);
            }
            rs.close();
            pstm.close();
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
        return lista;
    }

    @Override
    public void insert(reservation bean) {
        // Variables
        Connection cn = null;
        String sql = null;
        PreparedStatement pstm = null;
        ResultSet rs;
        Integer id = 0;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            // Obtener contador
            sql = "SELECT valor FROM control WHERE parametro='Reservation'";
            pstm = cn.prepareStatement(sql);
            rs = pstm.executeQuery();
            if (!rs.next()) {
                rs.close();
                pstm.close();
                throw new SQLException("Contador de reservas no existe.");
            }
            id = Integer.parseInt(rs.getString("valor"));
            rs.close();
            pstm.close();
            // Actualizar contador
            id++;
            sql = "UPDATE control SET valor = ? WHERE parametro='Reservation'";
            pstm = cn.prepareStatement(sql);
            pstm.setString(1, id + "");
            pstm.executeUpdate();
            pstm.close();
            // Insertar nueva reserva
            pstm = cn.prepareStatement(SQL_INSERT);
            pstm.setInt(1, bean.getPersonId());
            pstm.setTimestamp(2, bean.getDateReservation());
            pstm.setDate(3, bean.getDateAvailable());
            pstm.setDate(4, bean.getDateReturn());
            pstm.setString(5, bean.getStatus());
            pstm.setString(6, bean.getObservations());
            pstm.setString(7, bean.getActive());
            pstm.executeUpdate();
            pstm.close();
            // Confirmar transacción
            bean.setId(id);
            cn.commit();
        } catch (SQLException e) {
            try {
                cn.rollback();
                cn.close();
            } catch (Exception e2) {
            }
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
    }

    @Override
    public void update(reservation bean) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        int rows;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            // Actualizar el registro
            pstm = cn.prepareStatement(SQL_UPDATE);
            pstm.setInt(1, bean.getPersonId());
            pstm.setTimestamp(2, bean.getDateReservation());
            pstm.setDate(3, bean.getDateAvailable());
            pstm.setDate(4, bean.getDateReturn());
            pstm.setString(5, bean.getStatus());
            pstm.setString(6, bean.getObservations());
            pstm.setString(7, bean.getActive());
            pstm.setInt(8, bean.getId());
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo actualizar la reserva.");
            }
            // Confirmar transacción
            cn.commit();
        } catch (SQLException e) {
            try {
                cn.rollback();
                cn.close();
            } catch (Exception e2) {
            }
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
    }

    @Override
    public void delete(String id) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        ResultSet rs = null;
        int rows = 0;
        String sql;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            // Validar
            sql = "SELECT COUNT(1) filas FROM detail_reservation WHERE reservation_id=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, Integer.parseInt(id));
            rs = pstm.executeQuery();
            rs.next();
            rows = rs.getInt("filas");
            rs.close();
            pstm.close();
            if (rows > 0) {
                throw new SQLException("ERROR: No se puede eliminar la reserva, tiene detalles de reserva relacionados.");
            }
            // Proceso
            pstm = cn.prepareStatement(SQL_DELETE);
            pstm.setInt(1, Integer.parseInt(id));
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo eliminar la reserva.");
            }
            // Confirmar transacción
            cn.commit();
        } catch (SQLException e) {
            throw new RuntimeException(e.getMessage());
        } finally {
            try {
                cn.close();
            } catch (Exception e2) {
            }
        }
    }

    @Override
    public reservation mapRow(ResultSet rs) throws SQLException {
    	reservation bean = new reservation();
        bean.setId(rs.getInt("id"));
        bean.setPersonId(rs.getInt("person_id"));
        bean.setDateReservation(rs.getTimestamp("date_reservation"));
        bean.setDateAvailable(rs.getDate("date_available"));
        bean.setDateReturn(rs.getDate("date_return"));
        bean.setStatus(rs.getString("status"));
        bean.setObservations(rs.getString("observations"));
        bean.setActive(rs.getString("active"));
        return bean;
    }
}
