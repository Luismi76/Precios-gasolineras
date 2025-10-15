import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'

export default function StationDetail(){
  const { ideess } = useParams()
  const { data } = useQuery({ queryKey:['estacion', ideess], queryFn: ()=> api(`/api/estacion/${ideess}`) })
  if(!data) return <div>Cargando…</div>
  return (
    <div>
      <h2>{data.estacion.rotulo}</h2>
      <div>{data.estacion.direccion} – {data.estacion.localidad} ({data.estacion.provincia})</div>
      <h3>Precios</h3>
      <ul>
        {data.precios.map((p:any)=> <li key={p.id_producto}>{p.id_producto}: {p.precio ?? '—'}</li>)}
      </ul>
    </div>
  )
}
