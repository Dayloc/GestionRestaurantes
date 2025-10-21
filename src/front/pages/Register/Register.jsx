import "./styleRegister.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { 
  registerRestaurant, 
  registerClient, 
  registerWorker 
} from "./../../services/fetchs";

export default function Register() {
  const navigate = useNavigate();

  const [userType, setUserType] = useState("cliente"); 
  const [registerData, setRegisterData] = useState({
    nombre: "",
    primer_apellido: "",
    cantidad_trabajadores: "",
    localizacion: "",
    restaurant_id: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setRegisterData({ ...registerData, [e.target.name]: e.target.value });
  };

  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (userType === "restaurante") {
        const data = await registerRestaurant(
          registerData.nombre,
          registerData.cantidad_trabajadores,
          registerData.localizacion,
          registerData.email,
          registerData.password
        );
        alert("✅ Restaurante registrado con éxito");
        navigate("/login");
      }

      if (userType === "cliente") {
        const data = await registerClient(
          registerData.nombre,
          registerData.primer_apellido,
          registerData.email,
          registerData.password
        );
        alert("✅ Cliente registrado con éxito");
        navigate("/login");
      }

      if (userType === "trabajador") {
        const data = await registerWorker(
          registerData.nombre,
          registerData.primer_apellido,
          registerData.email,
          registerData.password,
          registerData.restaurant_id
        );
        alert("✅ Trabajador registrado con éxito");
        navigate("/login");
      }

    } catch (err) {
      console.error(err);
      alert("❌ Error al registrar: " + err.message);
    }
  };

  return (
    <div className="register-overlay">
      <div className="register-container">
        <h2>Crear cuenta</h2>

        <form onSubmit={handleSubmit}>
          <div className="user-type">
            <label>
              <input
                type="radio"
                name="tipo"
                value="cliente"
                checked={userType === "cliente"}
                onChange={handleUserTypeChange}
              />{" "}
              Cliente
            </label>

            <label>
              <input
                type="radio"
                name="tipo"
                value="trabajador"
                checked={userType === "trabajador"}
                onChange={handleUserTypeChange}
              />{" "}
              Trabajador
            </label>

            <label>
              <input
                type="radio"
                name="tipo"
                value="restaurante"
                checked={userType === "restaurante"}
                onChange={handleUserTypeChange}
              />{" "}
              Restaurante
            </label>
          </div>

          {/* Nombre */}
          <input
            type="text"
            name="nombre"
            placeholder={userType === "restaurante" ? "Nombre del restaurante" : "Nombre"}
            value={registerData.nombre}
            onChange={handleChange}
          />

          {/* Apellido solo para cliente y trabajador */}
          {(userType === "cliente" || userType === "trabajador") && (
            <input
              type="text"
              name="primer_apellido"
              placeholder="Primer apellido"
              value={registerData.primer_apellido}
              onChange={handleChange}
            />
          )}

          {/* Restaurante: Número de trabajadores */}
          {userType === "restaurante" && (
            <>
              <label>Número de trabajadores:</label>
              <input
                type="number"
                name="cantidad_trabajadores"
                placeholder="Cantidad de trabajadores"
                value={registerData.cantidad_trabajadores}
                onChange={handleChange}
              />
              <input
                type="text"
                name="localizacion"
                placeholder="Localización"
                value={registerData.localizacion}
                onChange={handleChange}
              />
            </>
          )}

          {/* Trabajador: Restaurante ID */}
          {userType === "trabajador" && (
            <input
              type="number"
              name="restaurant_id"
              placeholder="ID del restaurante"
              value={registerData.restaurant_id}
              onChange={handleChange}
            />
          )}

          {/* Email y contraseña */}
          <input
            type="email"
            name="email"
            placeholder="Correo electrónico"
            value={registerData.email}
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={registerData.password}
            onChange={handleChange}
          />

          <button type="submit">Registrarme</button>
        </form>
      </div>
    </div>
  );
}
