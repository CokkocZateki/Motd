$(document).ready(function() {
    // Initialize Select2 for groups dropdown
    $('.select2').select2({
        theme: 'bootstrap-5',
        placeholder: 'Select groups...',
        allowClear: true,
        width: '100%'
    });

    // Toggle groups section based on show_to_all checkbox
    function toggleGroups() {
        if ($('#id_show_to_all').is(':checked')) {
            $('#groups-section').hide();
        } else {
            $('#groups-section').show();
        }
    }

    toggleGroups();
    $('#id_show_to_all').change(toggleGroups);
});
