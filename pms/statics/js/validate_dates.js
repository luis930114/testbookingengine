document.addEventListener('DOMContentLoaded', function () {
    const checkinInput = document.getElementById('id_checkin');
    const checkoutInput = document.getElementById('id_checkout');

    // Escuchar cuando el usuario cambia la fecha de salida
    checkoutInput.addEventListener('change', function () {
        const checkinDate = new Date(checkinInput.value);
        const checkoutDate = new Date(checkoutInput.value);

        // Si alguno está vacío, no hacer nada
        if (!checkinInput.value || !checkoutInput.value) return;

        // Validar que la fecha de entrada sea menor a la salida
        if (checkinDate >= checkoutDate) {
            Swal.fire({
                icon: 'error',
                title: 'Fechas inválidas',
                text: 'La fecha de salida debe ser posterior a la fecha de entrada.',
                confirmButtonColor: '#0d6efd',
                confirmButtonText: 'Entendido',
                customClass: {
                    popup: 'rounded-4 shadow-lg'
                }
            });

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
});
