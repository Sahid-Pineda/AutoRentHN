document.addEventListener("DOMContentLoaded", function () {
  const seleccionColonia = document.getElementById("colonia_id");
  const seleccionCiudad = document.getElementById("ciudad_id");
  const seleccionDepartamento = document.getElementById("departamento_id");
  const seleccionPais = document.getElementById("pais_id");

  // Limpia y asigna opción al vuelo
  function setSelectValue(select, id, nombre) {
    select.innerHTML = ""; // limpia opciones
    if (id && nombre) {
      const opt = document.createElement("option");
      opt.value = id;
      opt.textContent = nombre;
      select.appendChild(opt);
      select.value = id;
    }
  }

  seleccionColonia.addEventListener("change", function () {
    const coloniaId = this.value;

    if (coloniaId) {
      fetch(`/api/get_ubicacion/?colonia_id=${coloniaId}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            console.error("Error:", data.error);
            return;
          }

          setSelectValue(seleccionCiudad, data.ciudad.id, data.ciudad.nombre);
          setSelectValue(
            seleccionDepartamento,
            data.departamento.id,
            data.departamento.nombre
          );
          setSelectValue(seleccionPais, data.pais.id, data.pais.nombre);
        })
        .catch((error) => {
          console.error("Error al obtener los datos de la colonia:", error);
        });
    } else {
      // Si se limpia la colonia, limpia también los demás
      seleccionCiudad.innerHTML =
        "<option value=''>--Selecciona una ciudad--</option>";
      seleccionDepartamento.innerHTML =
        "<option value=''>--Selecciona un departamento--</option>";
      seleccionPais.innerHTML =
        "<option value=''>--Selecciona un país--</option>";
    }
  });
});
