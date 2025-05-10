// var for audio content

var audio = document.getElementById('audio');
let wave = document.getElementsByClassName('wave')[0];

// html5 function - toggle play/pause btn and audio

$("#plays_btn").click(function() {

    if (audio.paused == false) {
        audio.pause();
        $("#play_btn").show();
        $("#pause_btn").hide();
        wave.classList.remove('active2');
    } else {
        audio.play();
        $("#play_btn").hide();
        $("#pause_btn").show();
        wave.classList.add('active2');
    }
});


// function for timeline

audio.addEventListener("timeupdate", function() {
    var currentTime = audio.currentTime,
        duration = audio.duration,
        currentTimeMs = audio.currentTime * 1000;
    $('.progressbar_range').stop(true, true).animate({ 'width': (currentTime + .25) / duration * 100 + '%' }, 250, 'linear');
});


// count function for timeleft

audio.addEventListener("timeupdate", function() {
    var timeleft = document.getElementById('timeleft'),
        duration = parseInt(audio.duration),
        currentTime = parseInt(audio.currentTime),
        timeLeft = duration - currentTime,
        s, m;

    s = timeLeft % 60;
    m = Math.floor(timeLeft / 60) % 60;

    s = s < 10 ? "0" + s : s;
    m = m < 10 ? "0" + m : m;

    $('#timeleft').text("-" + m + ":" + s);

});
let currentStart = document.getElementById('currentStart');
let currentEnd = document.getElementById('currentEnd');
let seek = document.getElementById('seek');
let bar2 = document.getElementById('bar2');
let dot = document.getElementsByClassName('dot')[0];

audio.addEventListener('timeupdate', () => {
    let music_curr = audio.currentTime;
    let music_dur = audio.duration;

    let min = Math.floor(music_dur / 60);
    let sec = Math.floor(music_dur % 60);
    if (sec < 10) {
        sec = `0${sec}`
    }
    currentEnd.innerText = `${min}:${sec}`;

    let min1 = Math.floor(music_curr / 60);
    let sec1 = Math.floor(music_curr % 60);
    if (sec1 < 10) {
        sec1 = `0${sec1}`
    }
    currentStart.innerText = `${min1}:${sec1}`;

    let progressbar = parseInt((audio.currentTime / audio.duration) * 100);
    seek.value = progressbar;
    let seekbar = seek.value;
    bar2.style.width = `${seekbar}%`;
    dot.style.left = `${seekbar}%`;
})

seek.addEventListener('change', () => {
    audio.currentTime = seek.value * audio.duration / 100;
})

audio.addEventListener("ended", next);