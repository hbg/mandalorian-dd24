
(function() {
    "use strict";

    function init() {
        const killswitch = id("killswitch");
        if (killswitch) {
            killswitch.addEventListener("click", () => {
                window.location.href = '/activate';
            })
        } else {
            setInterval(updateTime, 1000);
        }
    }

    function updateTime() {
        const timeRemaining = id('time-remaining');
        let secondsLeft = parseInt(timeRemaining.textContent);
        if (secondsLeft == 0) {
            window.location.href = '/'
        }
        timeRemaining.textContent = secondsLeft - 1;
    }

    init()
})()