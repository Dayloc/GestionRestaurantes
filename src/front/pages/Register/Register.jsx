import "./styleRegister.css";

export default function Register() {
  return (
    <div className="register-overlay">
      <div className="register-container">
        <h2>Crear cuenta</h2>

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

          <input type="text" placeholder="Nombre completo" />
          <input type="email" placeholder="Correo electrónico" />
          <input type="password" placeholder="Contraseña" />

          <button type="submit">Registrarme</button>
        </form>
      </div>
    </div>
  );
}
