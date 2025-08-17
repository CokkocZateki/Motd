$(document).ready(function() {
    const modalDeleteApprove = $('#deleteModal');

    // Approve Request Modal
    modalDeleteApprove.on('show.bs.modal', (event) => {
        const button = $(event.relatedTarget);
        const url = button.data('action');

        $('#modal-button-delete').on('click', () => {
            const form = modalDeleteApprove.find('form');
            const csrfMiddlewareToken = form.find('input[name="csrfmiddlewaretoken"]').val();

            const posting = $.post(
                url,
                {
                    csrfmiddlewaretoken: csrfMiddlewareToken
                }
            );

            posting.done((data) => {
                if (data.success === true) {
                    modalDeleteApprove.modal('hide');
                    window.location.reload();
                }
            }).fail((xhr, _, __) => {
                const response = JSON.parse(xhr.responseText);
                const errorMessage = $('<div class="alert alert-danger"></div>').text(response.message);
                form.append(errorMessage);
            });
        });
    }).on('hide.bs.modal', () => {
        modalDeleteApprove.find('.alert-danger').remove();
        $('#modal-button-delete').unbind('click');
    });
});
