export default function ResultsTable({ items = [] as any[] }) {
  return (
    <table className="results">
      <thead>
        <tr>
          <th>Estación</th>
          <th>Localidad</th>
          <th>Provincia</th>
          <th>€</th>
        </tr>
      </thead>
      <tbody>
        {items.map((r: any, i: number) => (
          <tr key={`${r.ideess}-${i}`}>
            <td>{r.rotulo}</td>
            <td>{r.localidad}</td>
            <td>{r.provincia}</td>
            <td>{r.precio ?? "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
