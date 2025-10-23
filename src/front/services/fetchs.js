const URL_BASE = import.meta.env.VITE_BACKEND_URL;

// ------------------ REGISTROS ------------------

// Registrar Cliente
export const registerClient = async (nombre, primer_apellido, email, password) => {
  try {
    const response = await fetch(`${URL_BASE}/clien/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, primer_apellido, email, password }),
    });
    if (!response.ok) throw new Error("Error al registrar cliente");
    return await response.json();
  } catch (error) {
    console.error("❌ Error registrando cliente:", error);
    throw error;
  }
};

// Registrar Restaurante
export const registerRestaurant = async (nombre, cantidad_trabajadores, localizacion, email, password) => {
  try {
    const response = await fetch(`${URL_BASE}/rest/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, cantidad_trabajadores, localizacion, email, password }),
    });
    if (!response.ok) throw new Error("Error al registrar restaurante");
    return await response.json();
  } catch (error) {
    console.error("❌ Error registrando restaurante:", error);
    throw error;
  }
};

// Registrar Trabajador
export const registerTrabajador = async (nombre, primer_apellido, email, password, restaurant_id) => {
  try {
    const response = await fetch(`${URL_BASE}/trab/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, primer_apellido, email, password, restaurant_id }),
    });
    if (!response.ok) throw new Error("Error al registrar trabajador");
    return await response.json();
  } catch (error) {
    console.error("❌ Error registrando trabajador:", error);
    throw error;
  }
};

// ------------------ LOGINS ------------------

// Login Cliente
export const loginClient = async (email, password) => {
  try {
    const response = await fetch(`${URL_BASE}/clien/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error("Error en login cliente");
    return await response.json();
  } catch (error) {
    console.error("❌ Error en login cliente:", error);
    throw error;
  }
};

// Login Restaurante
export const loginRestaurant = async (email, password) => {
  try {
    const response = await fetch(`${URL_BASE}/rest/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error("Error en login restaurante");
    return await response.json();
  } catch (error) {
    console.error("❌ Error en login restaurante:", error);
    throw error;
  }
};

// Login Trabajador
export const loginTrabajador = async (email, password) => {
  try {
    const response = await fetch(`${URL_BASE}/trab/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) throw new Error("Error en login trabajador");
    return await response.json();
  } catch (error) {
    console.error("❌ Error en login trabajador:", error);
    throw error;
  }
};
