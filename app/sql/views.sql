CREATE OR REPLACE VIEW vw_precio_actual AS
SELECT DISTINCT ON (ideess, id_producto)
  ideess, id_producto, precio, fecha
FROM precios
ORDER BY ideess, id_producto, fecha DESC;
