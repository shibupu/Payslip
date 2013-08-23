function validate_form() {
    var elements = ['name', 'emp_no', 'designation', 'address', 'phone', 'mobile', 'email', 'date_of_birth', 'date_of_joining'];
    for (var i = 0; i < elements.length; i++) {
        if (validate_element(elements[i]) == false) return;
    }

    if (validate_email('email') == false) return;

    document.employees.submit();
}