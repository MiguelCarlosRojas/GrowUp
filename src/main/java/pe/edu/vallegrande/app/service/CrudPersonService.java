package pe.edu.vallegrande.app.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.model.person;
import pe.edu.vallegrande.app.service.spec.CrudServiceSpec;
import pe.edu.vallegrande.app.service.spec.RowMapper;

public class CrudPersonService implements CrudServiceSpec<person>, RowMapper<person> {

    // Definiendo cosas
    private final String SQL_SELECT_BASE = "SELECT id, names, last_name, type_document, number_document, email, cell_phone, rol, active FROM person";
    private final String SQL_INSERT = "INSERT INTO person(id, names, last_name, type_document, number_document, email, cell_phone, rol, active) VALUES(?,?,?,?,?,?,?,?,?)";
    private final String SQL_UPDATE = "UPDATE person SET names=?, last_name=?, type_document=?, number_document=?, email=?, cell_phone=?, rol=?, active=? WHERE id=?";
    private final String SQL_DELETE = "DELETE FROM person WHERE id=?";

    @Override
    public List<person> getAll() {
        // Variables
        Connection cn = null;
        List<person> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        person bean;
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
    public person getForId(String id) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        ResultSet rs = null;
        person bean = null;
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

    /**
     * Realiza la búsqueda por nombres y apellidos.
     */
    @Override
    public List<person> get(person bean) {
        // Variables
        Connection cn = null;
        List<person> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        person item;
        String sql;
        String names;
        String lastName;
        // Preparar los datos
        names = "%" + UtilService.setStringVacio(bean.getNames()) + "%";
        lastName = "%" + UtilService.setStringVacio(bean.getLast_Name()) + "%";
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            sql = SQL_SELECT_BASE + " WHERE names LIKE ? AND last_name LIKE ?";
            pstm = cn.prepareStatement(sql);
            pstm.setString(1, names);
            pstm.setString(2, lastName);
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
    public void insert(person bean) {
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
            sql = "SELECT MAX(id) as max_id FROM person";
            pstm = cn.prepareStatement(sql);
            rs = pstm.executeQuery();
            if (rs.next()) {
                id = rs.getInt("max_id");
            }
            rs.close();
            pstm.close();
            id++;
            pstm = cn.prepareStatement(SQL_INSERT);
            pstm.setInt(1, id);
            pstm.setString(2, bean.getNames());
            pstm.setString(3, bean.getLast_Name());
            pstm.setString(4, bean.getType_Document());
            pstm.setString(5, bean.getNumber_Document());
            pstm.setString(6, bean.getEmail());
            pstm.setString(7, bean.getCell_Phone());
            pstm.setString(8, bean.getRol());
            pstm.setString(9, bean.getActive());
            pstm.executeUpdate();
            pstm.close();
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
    public void update(person bean) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        int rows;
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            cn.setAutoCommit(false);
            pstm = cn.prepareStatement(SQL_UPDATE);
            pstm.setString(1, bean.getNames());
            pstm.setString(2, bean.getLast_Name());
            pstm.setString(3, bean.getType_Document());
            pstm.setString(4, bean.getNumber_Document());
            pstm.setString(5, bean.getEmail());
            pstm.setString(6, bean.getCell_Phone());
            pstm.setString(7, bean.getRol());
            pstm.setString(8, bean.getActive());
            pstm.setInt(9, bean.getId());
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("Error updating person.");
            }
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
            sql = "SELECT count(1) rows FROM usuario WHERE idempleado=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, Integer.parseInt(id));
            rs = pstm.executeQuery();
            rs.next();
            rows = rs.getInt("rows");
            rs.close();
            pstm.close();
            if (rows > 0) {
                throw new SQLException("ERROR: Cannot delete person with associated records.");
            }
            pstm = cn.prepareStatement(SQL_DELETE);
            pstm.setInt(1, Integer.parseInt(id));
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("Could not delete person.");
            }
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
    public person mapRow(ResultSet rs) throws SQLException {
    	person bean = new person();
        bean.setId(rs.getInt("id"));
        bean.setNames(rs.getString("names"));
        bean.setLast_Name(rs.getString("last_name"));
        bean.setType_Document(rs.getString("type_document"));
        bean.setNumber_Document(rs.getString("number_document"));
        bean.setEmail(rs.getString("email"));
        bean.setCell_Phone(rs.getString("cell_phone"));
        bean.setRol(rs.getString("rol"));
        bean.setActive(rs.getString("active"));
        return bean;
    }
}