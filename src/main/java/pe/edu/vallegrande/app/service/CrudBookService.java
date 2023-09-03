package pe.edu.vallegrande.app.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import pe.edu.vallegrande.app.db.AccesoDBLocal;
import pe.edu.vallegrande.app.model.book;
import pe.edu.vallegrande.app.service.spec.CrudServiceSpec;
import pe.edu.vallegrande.app.service.spec.RowMapper;

public class CrudBookService implements CrudServiceSpec<book>, RowMapper<book> {

    // Definiendo consultas SQL
    private final String SQL_SELECT_BASE = "SELECT id, title, catalogs, isbn, location, number_copies, status FROM book";
    private final String SQL_INSERT = "INSERT INTO book(title, catalogs, isbn, location, number_copies, status) VALUES(?,?,?,?,?,?)";
    private final String SQL_UPDATE = "UPDATE book SET title=?, catalogs=?, isbn=?, location=?, number_copies=?, status=? WHERE id=?";
    private final String SQL_DELETE = "DELETE FROM book WHERE id=?";

    @Override
    public List<book> getAll() {
        // Variables
        Connection cn = null;
        List<book> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        book bean;
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
    public book getForId(String id) {
        // Variables
        Connection cn = null;
        PreparedStatement pstm = null;
        ResultSet rs = null;
        book bean = null;
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
    public List<book> get(book bean) {
        // Variables
        Connection cn = null;
        List<book> lista = new ArrayList<>();
        PreparedStatement pstm = null;
        ResultSet rs = null;
        book item;
        String sql;
        String title;
        String catalogs;
        // Preparar los datos
        title = "%" + UtilService.setStringVacio(bean.getTitle()) + "%";
        catalogs = "%" + UtilService.setStringVacio(bean.getCatalogs()) + "%";
        // Proceso
        try {
            cn = AccesoDBLocal.getConnection();
            sql = SQL_SELECT_BASE + " WHERE title LIKE ? AND catalogs LIKE ?";
            pstm = cn.prepareStatement(sql);
            pstm.setString(1, title);
            pstm.setString(2, catalogs);
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
    public void insert(book bean) {
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
            sql = "SELECT valor FROM control WHERE parametro='Book'";
            pstm = cn.prepareStatement(sql);
            rs = pstm.executeQuery();
            if (!rs.next()) {
                rs.close();
                pstm.close();
                throw new SQLException("Contador de libros no existe.");
            }
            id = Integer.parseInt(rs.getString("valor"));
            rs.close();
            pstm.close();
            // Actualizar contador
            id++;
            sql = "UPDATE control SET valor = ? WHERE parametro='Book'";
            pstm = cn.prepareStatement(sql);
            pstm.setString(1, id + "");
            pstm.executeUpdate();
            pstm.close();
            // Insertar nuevo libro
            pstm = cn.prepareStatement(SQL_INSERT);
            pstm.setString(1, bean.getTitle());
            pstm.setString(2, bean.getCatalogs());
            pstm.setString(3, bean.getIsbn());
            pstm.setString(4, bean.getLocation());
            pstm.setInt(5, bean.getNumber_Copies());
            pstm.setString(6, bean.getStatus());
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
    public void update(book bean) {
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
            pstm.setString(1, bean.getTitle());
            pstm.setString(2, bean.getCatalogs());
            pstm.setString(3, bean.getIsbn());
            pstm.setString(4, bean.getLocation());
            pstm.setInt(5, bean.getNumber_Copies());
            pstm.setString(6, bean.getStatus());
            pstm.setInt(7, bean.getId());
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo actualizar el libro.");
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
            sql = "SELECT COUNT(1) filas FROM loan WHERE book_id=?";
            pstm = cn.prepareStatement(sql);
            pstm.setInt(1, Integer.parseInt(id));
            rs = pstm.executeQuery();
            rs.next();
            rows = rs.getInt("filas");
            rs.close();
            pstm.close();
            if (rows > 0) {
                throw new SQLException("ERROR: No se puede eliminar el libro, tiene préstamos relacionados.");
            }
            // Proceso
            pstm = cn.prepareStatement(SQL_DELETE);
            pstm.setInt(1, Integer.parseInt(id));
            rows = pstm.executeUpdate();
            pstm.close();
            if (rows != 1) {
                throw new SQLException("No se pudo eliminar el libro.");
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
    public book mapRow(ResultSet rs) throws SQLException {
    	book bean = new book();
        bean.setId(rs.getInt("id"));
        bean.setTitle(rs.getString("title"));
        bean.setCatalogs(rs.getString("catalogs"));
        bean.setIsbn(rs.getString("isbn"));
        bean.setLocation(rs.getString("location"));
        bean.setNumber_Copies(rs.getInt("number_copies"));
        bean.setStatus(rs.getString("status"));
        return bean;
    }
}