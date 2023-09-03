package pe.edu.vallegrande.app.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.model.detailreservation;
import pe.edu.vallegrande.app.service.spec.CrudServiceSpec;
import pe.edu.vallegrande.app.service.spec.RowMapper;

public class CrudDetailReservationService implements CrudServiceSpec<detailreservation>, RowMapper<detailreservation> {

    // Definiendo consultas SQL
    private final String SQL_SELECT_BASE = "SELECT id, reservation_id, book_id, quantity, reason FROM detail_reservation";
    private final String SQL_INSERT = "INSERT INTO detail_reservation(reservation_id, book_id, quantity, reason) VALUES(?,?,?,?)";
    private final String SQL_UPDATE = "UPDATE detail_reservation SET reservation_id=?, book_id=?, quantity=?, reason=? WHERE id=?";
    private final String SQL_DELETE = "DELETE FROM detail_reservation WHERE id=?";

    @Override
    public List<detailreservation> getAll() {
        // Variables
        Connection cn = null;
        List<detailreservation> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        detailreservation bean;
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
    public detailreservation getForId(String id) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        ResultSet rs = null;
        detailreservation bean = null;
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
    public List<detailreservation> get(detailreservation bean) {
        // Variables
        Connection cn = null;
        List<detailreservation> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        detailreservation item;
        String sql;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            sql = SQL_SELECT_BASE + " WHERE reservation_id=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, bean.getReservationId());
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
    public void insert(detailreservation bean) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            // Insertar nuevo detalle de reserva
            pstm = cn.prepareStatement(SQL_INSERT);
            pstm.setInt(1, bean.getReservationId());
            pstm.setInt(2, bean.getBookId());
            pstm.setInt(3, bean.getQuantity());
            pstm.setString(4, bean.getReason());
            pstm.executeUpdate();
            pstm.close();
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
    public void update(detailreservation bean) {
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
            pstm.setInt(1, bean.getReservationId());
            pstm.setInt(2, bean.getBookId());
            pstm.setInt(3, bean.getQuantity());
            pstm.setString(4, bean.getReason());
            pstm.setInt(5, bean.getId());
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo actualizar el detalle de reserva.");
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
        int rows = 0;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            // Proceso
            pstm = cn.prepareStatement(SQL_DELETE);
            pstm.setInt(1, Integer.parseInt(id));
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo eliminar el detalle de reserva.");
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
    public detailreservation mapRow(ResultSet rs) throws SQLException {
    	detailreservation bean = new detailreservation();
        bean.setId(rs.getInt("id"));
        bean.setReservationId(rs.getInt("reservation_id"));
        bean.setBookId(rs.getInt("book_id"));
        bean.setQuantity(rs.getInt("quantity"));
        bean.setReason(rs.getString("reason"));
        return bean;
    }

}
