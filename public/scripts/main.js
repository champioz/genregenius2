

function copy_text(target){

    textTarget = "copypaste".concat(target);
    buttonTarget = "copy_button".concat(target);

    let copyText = document.getElementById(textTarget);
    navigator.clipboard.writeText(copyText.textContent);

    let button = document.getElementById(buttonTarget);
    button.textContent = "Copied!";
    setTimeout(function () {
        button.textContent = "Copy"
    }, 2000);    
}

function runPyScript(input){
    let jqXHR = $.ajax({
        type: "GET",
        url: `/classify/${input}`,
        async: false,
        data: { mydata: input }
    });

    return jqXHR.responseText;
}