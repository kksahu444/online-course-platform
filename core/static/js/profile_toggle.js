// core/static/js/profile_toggle.js

document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.querySelector('#id_role');
    const studentIdInput = document.querySelector('#id_student_id');
    const instructorIdInput = document.querySelector('#id_instructor_id');

    function updateFields() {
        const role = roleSelect.value;

        if (role === 'Student') {
            // Logic for Student: Lock Instructor ID, Unlock Student ID
            instructorIdInput.value = '';           // Clear value
            instructorIdInput.readOnly = true;      // Make read-only
            instructorIdInput.style.backgroundColor = '#e0e0e0'; // Grey out

            studentIdInput.readOnly = false;        // Unlock
            studentIdInput.style.backgroundColor = '#ffffff'; // White
        } 
        else if (role === 'Instructor') {
            // Logic for Instructor: Lock Student ID, Unlock Instructor ID
            studentIdInput.value = '';
            studentIdInput.readOnly = true;
            studentIdInput.style.backgroundColor = '#e0e0e0';

            instructorIdInput.readOnly = false;
            instructorIdInput.style.backgroundColor = '#ffffff';
        }
        else {
            // Logic for Admin/Analyst: Lock BOTH (they don't need IDs)
            studentIdInput.value = '';
            studentIdInput.readOnly = true;
            studentIdInput.style.backgroundColor = '#e0e0e0';

            instructorIdInput.value = '';
            instructorIdInput.readOnly = true;
            instructorIdInput.style.backgroundColor = '#e0e0e0';
        }
    }

    // Run on page load (in case editing an existing profile)
    if (roleSelect) {
        updateFields();
        // Run every time the user changes the dropdown
        roleSelect.addEventListener('change', updateFields);
    }
});