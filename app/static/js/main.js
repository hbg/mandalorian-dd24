
(function() {
    "use strict";
    let active = true;

    function init() {
        const glyphSymbols = qsa('.glyph-wrapper > img');
        glyphSymbols.forEach((symbol) => {
            symbol.addEventListener("click", addGlyph);
        });

        const glyphToggles = qsa('#glyph-toggle > div');
        glyphToggles.forEach((toggle) => {
            let toggleValue = toggle.getAttribute('value');
            console.log("hello");
            toggle.addEventListener("click", () => {
                toggleGlyph(toggleValue);
            })
        });
    }

    function toggleGlyph(value) {
        qsa('.glyph-wrapper').forEach((wrapper) => {
            wrapper.classList.add("hidden");
        });
        id('glyph-'+value).classList.toggle("hidden");
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

    function verifyCode() {
        const glyphBoxImgs = qsa('.glyph-box > img');
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