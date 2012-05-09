function post(endURL, postData) {
    var frm = document.createElement('form');
    frm.method = 'post';
    frm.action = endURL;
    
    for (var elem in postData) {
        var inputBox = document.createElement('input');
        inputBox.setAttribute('name', elem);
        inputBox.setAttribute('value', postData[elem]);
        frm.appendChild(inputBox);
    }
    
    document.body.appendChild(frm);
    frm.submit();
    document.body.removeChild(frm);
}