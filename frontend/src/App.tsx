import { Outlet, Link } from 'react-router-dom'

export default function App(){
  return (
    <div className="container">
      <header>
        <h1>PrecioGasolineras</h1>
        <nav>
          <Link to="/">Inicio</Link>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}
