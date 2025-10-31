document.addEventListener('DOMContentLoaded', function () {
    const checkinInput = document.getElementById('id_checkin');
    const checkoutInput = document.getElementById('id_checkout');
    const roomId = document.getElementById('id_room');

    const checkAvailabilityBtn = document.getElementById('check-availability');

    // Función para mostrar alertas bonitas
        function showAlert(icon, title, text) {
            Swal.fire({
                icon: icon,
                title: title,
                text: text,
                confirmButtonColor: '#0d6efd',
                confirmButtonText: 'Entendido',
                customClass: {
                    popup: 'rounded-4 shadow-lg'
                }
            });
        }

    if (checkAvailabilityBtn) {
        checkAvailabilityBtn.addEventListener('click', function (event) {
            event.preventDefault(); // Evita que el enlace recargue la página
            checkAvailability();
        });
    }

    // Escuchar cuando el usuario cambia la fecha de salida
    checkoutInput.addEventListener('change', function () {        

        const checkinDate = new Date(checkinInput.value);
        const checkoutDate = new Date(checkoutInput.value);

        // Si alguno está vacío, no hacer nada
        if (!checkinInput.value || !checkoutInput.value) return;

        // Validar que la fecha de entrada sea menor a la salida
        if (checkinDate >= checkoutDate) {
            showAlert('error', 'Fechas inválidas', 'La fecha de salida debe ser posterior a la fecha de entrada.');

            // Limpiar la fecha de salida
            checkoutInput.value = '';
            // Resaltar los campos en rojo
            checkinInput.classList.add('is-invalid');
            checkoutInput.classList.add('is-invalid');
        } else {
            // Si es válido, limpiar estado de error
            checkinInput.classList.remove('is-invalid');
            checkoutInput.classList.remove('is-invalid');
        }
    });

    // Validar disponibilidad
    async function checkAvailability() {
        const checkin = checkinInput.value;
        const checkout = checkoutInput.value;
        const roomIdValue = roomId.value;
        const submitBtn = document.getElementById('btnguardar');

        if (!checkin || !checkout) return;

        // Llamada a la API
        const url = `/api/check-availability/?room_id=${roomIdValue}&checkin=${checkin}&checkout=${checkout}`;
        try {
            const response = await fetch(url);
            const data = await response.json();

            if (!data.available) {
                showAlert('error', 'No disponible', data.message);
                submitBtn.disabled = true;
                checkoutInput.classList.add('is-invalid');
            } else {
                Swal.close(); // cerrar cualquier alerta previa si la hay
                showAlert('success', 'Disponible', data.message);
                checkoutInput.classList.remove('is-invalid');
                submitBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error al verificar disponibilidad:', error);
            showAlert('error', 'Error del servidor', 'No se pudo validar la disponibilidad.');
        }
    }

});
