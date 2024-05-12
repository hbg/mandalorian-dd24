
(function() {
    "use strict";
    let active = true;

    function init() {
        const glyphSymbols = qsa('#glyph-wrapper > img');
        glyphSymbols.forEach((symbol) => {
            symbol.addEventListener("click", addGlyph);
        });
    }

    function addGlyph() {
        const glyphBoxes = qsa('.glyph-box');
        let completedGlyphs = 0;
        for (let i = 0; i < glyphBoxes.length; i++) {
            completedGlyphs++;
            let box = glyphBoxes[i];
            if (box.innerHTML == '') {
                box.appendChild(this.cloneNode(true));
                break;
            }
        }
        if (completedGlyphs == glyphBoxes.length) {
            verifyCode();
        }
    }

    function arraysEqual(a, b) {
        if (a === b) return true;
        if (a == null || b == null) return false;
        if (a.length !== b.length) return false;
        for (var i = 0; i < a.length; ++i) {
          if (a[i] !== b[i]) return false;
        }
        return true;
      }

    function verifyCode() {
        const glyphBoxImgs = qsa('.glyph-box > img');
        let solution = ['1', '3', '5', '5', '7'];
        let code = [];
        glyphBoxImgs.forEach((img) => {
            code = code.concat(img.alt);
        });

        let codeId = qs("main").getAttribute('value');
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/submit", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        console.log(codeId);
        xhr.send(JSON.stringify({
            codeId: codeId,
            code: code
        }));
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    var json_data = JSON.parse(xhr.responseText);
                    if (json_data['solved'] == true) {
                        console.log("Solved!");
                    } else {
                        active = false;
                        glyphBoxImgs.forEach((img) => {
                            img.classList.add("wrong");
                        });
                        setTimeout(resetCode, 1000);
                    }
                }
            }
        }
    }

    function resetCode() {
        const glyphBoxImgs = qsa('.glyph-box > img');
        active = true;
        glyphBoxImgs.forEach((img) => {
            img.remove();
        });
    }

    init()
})()