document.addEventListener('DOMContentLoaded', function() {
    // Confirmação para ações de cancelamento
    const cancelButtons = document.querySelectorAll('.btn-cancelar');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Você tem certeza que deseja cancelar este agendamento?')) {
                event.preventDefault();
            }
        });
    });

    // Confirmação para ações de aceitar
    const acceptButtons = document.querySelectorAll('.btn-aceitar');
    acceptButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Você tem certeza que deseja aceitar este agendamento?')) {
                event.preventDefault();
            }
        });
    });

    // Confirmação para ações de recusar
    const refuseButtons = document.querySelectorAll('.btn-recusar');
    refuseButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Você tem certeza que deseja recusar este agendamento?')) {
                event.preventDefault();
            }
        });
    });

    // Confirmação para ações de remarcação
    const rescheduleButtons = document.querySelectorAll('.btn-remarcar');
    rescheduleButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Você tem certeza que deseja remarcar este agendamento?')) {
                event.preventDefault();
            }
        });
    });
});
