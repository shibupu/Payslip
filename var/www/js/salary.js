function validate_form() {
    var elements = ['basic'];
    for (var i = 0; i < elements.length; i++) {
        if (validate_element(elements[i]) == false) return;
    }

    document.salary.submit();
}