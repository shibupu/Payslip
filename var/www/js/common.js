function validate_element(id) {
    var obj = document.getElementById(id);
    var val = obj.value;
    var tit = obj.title;
    if (val == null || val == '' || val.match(/^\s+$/)) {
        alert('Please enter ' + tit);
        obj.focus();
        return false;
    }

    return true;
}

function validate_number(e) {
    var charCode = e.which || event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    return true;
}

function validate_amount(e) {
    var charCode = e.which || event.keyCode;
    if (charCode > 31 && charCode != 46 && (charCode < 48 || charCode > 57))
        return false;

    return true;
}

function validate_email(id) {
    if (validate_element(id) == false) return false;

    var obj = document.getElementById(id);
    var val = obj.value;
    var tit = obj.title;
    var atpos  = val.indexOf("@");
    var dotpos = val.lastIndexOf(".");
    if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= val.length) {
        alert('Please enter valid ' + tit);
        obj.focus();
        return false;
    }

    return true;
}