var editor = ace.edit("editor");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/rust");
editor.setShowPrintMargin(false);
editor.session.setUseWrapMode(true);
editor.session.setTabSize(3);
editor.setOptions({
    fontSize: "11pt"
});

var output = ace.edit("output");
output.setTheme("ace/theme/dracula");
output.session.setMode("ace/mode/text");
output.setReadOnly(true);
output.setShowPrintMargin(false);
output.setHighlightActiveLine(false);
output.session.setUseWrapMode(true);
output.session.setTabSize(3);
output.setOptions({
    fontSize: "11pt"
});
output.renderer.setShowGutter(false);

document.getElementById("run-button").addEventListener("click", function () {
    var code = editor.getValue();

    this.disabled = true;
    this.style.backgroundColor = 'grey';
    this.style.cursor = 'wait';

    output.setValue("Compiling...\nNote: your request may be queued if the server has too many compile requests to handle.");
    output.gotoLine(0);

    fetch("/run-code", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        output.setValue(data.output);
        output.gotoLine(0);
        this.disabled = false;
        this.style.backgroundColor = '#0be881';
        this.style.cursor = 'pointer';
    })
    .catch(err => {
        output.setValue("Connection to server failed." + JSON.stringify(err));
        output.gotoLine(0);
        this.disabled = false;
        this.style.backgroundColor = '#0be881';
        this.style.cursor = 'not-allowed';
        this.style.cursor = 'pointer';
    });
});

for (var selector of document.querySelectorAll("button.example")) {
    selector.addEventListener("click", function () {
        let name = this.id.slice(0, -12); // remove the "-example-btn" part (12 characters long)
        fetch("static/" + name + ".va")
        .then((res) => res.text())
        .then((text) => {
            editor.setValue(text);
         })
        .catch((e) => console.error(e));
    });
}