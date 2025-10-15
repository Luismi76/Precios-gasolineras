import React from "react";

export default function Filters({
  productos,
  provincias,
  producto,
  setProducto,
  provincia,
  setProvincia,
  count,
}: {
  productos: any[];
  provincias: any[];
  producto?: string;
  setProducto: (v: string | undefined) => void;
  provincia?: string;
  setProvincia: (v: string | undefined) => void;
  count: number;
}) {
  return (
    <div className="filters">
      <select
        value={producto || ""}
        onChange={(e) => setProducto(e.target.value || undefined)}
      >
        <option value="">Producto</option>
        {productos.map((p: any) => (
          <option key={p.id_producto} value={p.id_producto}>
            {p.nombre}
          </option>
        ))}
      </select>

      <select
        value={provincia || ""}
        onChange={(e) => setProvincia(e.target.value || undefined)}
        style={{ marginLeft: 8 }}
      >
        <option value="">Provincia</option>
        {provincias.map((p: any) => (
          <option key={p.id_prov} value={p.id_prov}>
            {p.nombre}
          </option>
        ))}
      </select>

      <div style={{ marginTop: 8 }}>
        <strong>Resultados:</strong> {count}
      </div>
    </div>
  );
}
