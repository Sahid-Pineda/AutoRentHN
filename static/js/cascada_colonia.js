document.addEventListener("DOMContentLoaded", function () {
  const seleccionPais = document.getElementById("pais_id");
  const seleccionDepartamento = document.getElementById("departamento_id");
  const seleccionCiudad = document.getElementById("ciudad_id");
  const seleccionColonia = document.getElementById("colonia_id");

  // Limpia y asigna opción al vuelo
  function limpiar_select(select, placeholder) {
    select.innerHTML = `<option value="">--${placeholder}--</option>`;
  }

  function llenar_select(select, data) {
    limpiar_select(select, select.name.replace("_id", ""));
    data.forEach((item) => {
      const opcion = document.createElement("option");
      opcion.value = item.id;
      opcion.textContent = item.nombre;
      select.appendChild(opcion);
    });
  }

  seleccionPais.addEventListener("change", function () {
    const paisId = this.value;
    limpiar_select(seleccionDepartamento, "Selecciona un departamento");
    limpiar_select(seleccionCiudad, "Selecciona una ciudad");
    limpiar_select(seleccionColonia, "Selecciona una colonia");

    if (paisId) {
      fetch(`/api/obtener-departamento/?pais_id=${paisId}`)
        .then((response) => response.json())
        .then((data) => {
          llenar_select(seleccionDepartamento, data.departamentos);
        });
    }
  });

  seleccionDepartamento.addEventListener("change", function () {
    const departamentoId = this.value;
    limpiar_select(seleccionCiudad, "Selecciona una ciudad");
    limpiar_select(seleccionColonia, "Selecciona una colonia");

    if (departamentoId) {
      fetch(`/api/obtener-ciudad/?departamento_id=${departamentoId}`)
        .then((response) => response.json())
        .then((data) => llenar_select(seleccionCiudad, data.ciudades));
    }
  });

  seleccionCiudad.addEventListener("change", function () {
    const ciudadId = this.value;
    limpiar_select(seleccionColonia, "Selecciona una colonia");

    if (ciudadId) {
      fetch(`/api/obtener-colonia/?ciudad_id=${ciudadId}`)
        .then((response) => response.json())
        .then((data) => llenar_select(seleccionColonia, data.colonias));
    }
  });
});

// Espera 5 segundos y luego esconde el mensaje de error
setTimeout(() => {
  const mensaje = document.getElementById("mensaje-error");
  if (mensaje) {
    mensaje.style.display = "none";
  }
}, 5000); // 5000ms = 5 segundos
