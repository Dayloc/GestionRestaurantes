import { Link } from "react-router-dom";
import "./Navbar.css";

export const Navbar = () => {
  return (
    <nav className="navbar-custom">
      <div className="navbar-container">
        {/* Nombre o logo */}
        <Link to="/" className="navbar-brand">
          🍴 App Restaurante
        </Link>

        {/* Botones */}
        <div className="navbar-buttons">
          <Link to="/login">
            <button className="btn-login">Iniciar sesión</button>
          </Link>
          <Link to="/register">
            <button className="btn-register">Registrarse</button>
          </Link>
        </div>
      </div>
    </nav>
  );
};
