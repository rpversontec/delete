document.addEventListener("DOMContentLoaded", () => {
  // --- CONFIGURACIÓN ---
  // ¡¡¡IMPORTANTE!!! Cambia esta URL por la de tu API backend desplegada en Coolify.
  // Ejemplo DEV: const apiUrl = 'https://api-dev.tu-dominio.coolify.app';
  // Ejemplo PROD: const apiUrl = 'https://api.tu-dominio.coolify.app';
  const apiUrl = "http://hsswkgos8wwgoc8gw084koso.20.55.28.0.sslip.io:4000"; // <-- CAMBIA ESTO (O usa la URL de tu backend)

  // --- REFERENCIAS DEL DOM ---
  const taskInput = document.getElementById("taskInput");
  const addTaskBtn = document.getElementById("addTaskBtn");
  const taskList = document.getElementById("taskList");

  // --- FUNCIONES ---

  // Obtiene todas las tareas del backend y las muestra
  async function fetchTasks() {
    try {
      const response = await fetch(`${apiUrl}/todos/`);
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      const tasks = await response.json();
      displayTasks(tasks);
    } catch (error) {
      console.error("Error al obtener las tareas:", error);
      taskList.innerHTML =
        "<li>Error al cargar las tareas. Revisa la consola.</li>";
    }
  }

  // Muestra las tareas en la lista UL
  function displayTasks(tasks) {
    taskList.innerHTML = ""; // Limpia la lista actual
    if (tasks.length === 0) {
      taskList.innerHTML = "<li>No hay tareas pendientes. ¡Añade una!</li>";
      return;
    }
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.textContent = task.task; // Asume que el objeto task tiene una propiedad "task"

      // Botón para eliminar
      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Eliminar";
      deleteBtn.classList.add("delete-btn");
      deleteBtn.dataset.id = task.id; // Asume que el objeto task tiene una propiedad "id"
      deleteBtn.addEventListener("click", () => {
        deleteTask(task.id);
      });

      li.appendChild(deleteBtn);
      taskList.appendChild(li);
    });
  }

  // Añade una nueva tarea
  async function addTask() {
    const taskText = taskInput.value.trim();
    if (!taskText) {
      alert("Por favor, escribe una tarea.");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/todos/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ task: taskText }), // El backend espera un objeto con la clave "task"
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      // const newTask = await response.json(); // Podrías usar newTask si necesitas el ID devuelto
      taskInput.value = ""; // Limpia el input
      fetchTasks(); // Recarga la lista para mostrar la nueva tarea
    } catch (error) {
      console.error("Error al añadir la tarea:", error);
      alert("No se pudo añadir la tarea.");
    }
  }

  // Elimina una tarea (¡Asegúrate que tu backend tenga este endpoint!)
  async function deleteTask(taskId) {
    if (!confirm("¿Estás seguro de que quieres eliminar esta tarea?")) {
      return;
    }

    try {
      // Asume que tu endpoint DELETE es /todos/{id}
      // Ajusta si tu API tiene una estructura diferente para eliminar
      const response = await fetch(`${apiUrl}/todos/${taskId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        // Si la API devuelve un cuerpo JSON con error, intenta leerlo
        let errorMsg = `Error HTTP: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMsg += ` - ${errorData.detail || JSON.stringify(errorData)}`;
        } catch (e) {
          /* No hacer nada si no hay cuerpo JSON */
        }
        throw new Error(errorMsg);
      }

      // Si la API devuelve algo en DELETE (algunas no lo hacen), podrías procesarlo aquí
      // await response.json();

      fetchTasks(); // Recarga la lista para quitar la tarea eliminada
    } catch (error) {
      console.error("Error al eliminar la tarea:", error);
      alert(`No se pudo eliminar la tarea: ${error.message}`);
    }
  }

  // --- EVENT LISTENERS ---

  // Añadir tarea al hacer clic en el botón
  addTaskBtn.addEventListener("click", addTask);

  // Añadir tarea al presionar Enter en el input
  taskInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      addTask();
    }
  });

  // --- CARGA INICIAL ---
  fetchTasks();
});
