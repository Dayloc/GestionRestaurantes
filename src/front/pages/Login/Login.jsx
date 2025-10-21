import "./styleLogin.css";
import {Link} from "react-router-dom";

export default function Login() {
  return (
    <div className="login-overlay">
      <div className="login-container">
        <h2>Iniciar sesión</h2>

        <form>
          <div className="user-type">
            <label>
              <input type="radio" name="tipo" value="cliente" defaultChecked /> Cliente
            </label>
            <label>
              <input type="radio" name="tipo" value="trabajador" /> Trabajador
            </label>
            <label>
              <input type="radio" name="tipo" value="restaurante" /> Restaurante
            </label>
          </div>

          <input type="email" placeholder="Correo electrónico" />
          <input type="password" placeholder="Contraseña" />

          <button type="submit">Ingresar</button>
        </form>
    <p className="mt-3">Si aún no te has registrado,<Link className="text-warning" to="/register"> haz click aquí</Link>  </p>
    
      </div>
    </div>
  );
}
