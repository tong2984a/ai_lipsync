/* Audio enable & disable switch */
$("#audioUploadSwitch").change((e)=>{
  var value = e.target.checked;
  var sampleUrl = "https://upload.wikimedia.org/wikipedia/commons/f/f3/Anthem_of_Europe_%28US_Navy_instrumental_short_version%29.ogg";
  if(value == true){
    $("#track").attr("src", sampleUrl);
    document.getElementById("track").load();
    $("div.player").toggleClass('d-none');
    $(".file-upload-wrapper").toggleClass('d-none');
  }else{
    $("div.player").toggleClass('d-none');
    $(".file-upload-wrapper").toggleClass('d-none');
  }
});

/* upload audio file */
function handleFiles(event) {
    var files = event.target.files;
    $("#track").attr("src", URL.createObjectURL(files[0]));
    document.getElementById("track").load();
    console.log(event);
    $("div.player").toggleClass('d-none');
    $(".file-upload-wrapper").toggleClass('d-none');
}
document.getElementById("audiofile").addEventListener("change", handleFiles, false);

$('#track').each(function(index, audio) {
    $(audio).on('canplay', function() {
        console.log(audio.duration);
        $("#duration")[0].innerHTML = sec2time(audio.duration);
        $("#timeslieder")[0].max = audio.duration * 1000;
    });
});

/* start button */
$("#start").click(function() {
    $("#track")[0].play();
    $(this).toggleClass('d-none');
    $("#pause").toggleClass('d-none');
});
/* pause button */
$("#pause").click(function() {
    $("#track")[0].pause();
    $(this).toggleClass('d-none');
    $("#start").toggleClass('d-none');
});
/* reset button */
$("#reset").click(function() {
    $("#track")[0].load();
    $("#start").toggleClass('d-none');
    $("#pause").toggleClass('d-none');
});
/* timeupdate log */
$("#track")[0].addEventListener('timeupdate', function() {
    var currentTimeSec = this.currentTime;
    var currentTimeMs = this.currentTime * 1000;
    $("#currentTime")[0].innerHTML = sec2time(currentTimeSec);
    $("#timeslieder")[0].value = currentTimeMs;
    initRangeEl();
    var arrayTime = [sec2time(currentTimeSec), currentTimeMs];
    console.log(currentTimeMs);
}, false);

function sec2time(timeInSeconds) {
    var pad = function(num, size) {
            return ('000' + num).slice(size * -1);
        },
        time = parseFloat(timeInSeconds).toFixed(3),
        hours = Math.floor(time / 60 / 60),
        minutes = Math.floor(time / 60) % 60,
        seconds = Math.floor(time - minutes * 60),
        milliseconds = time.slice(-3);
    return pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2);
}


/* timeline slieder */
function valueTotalRatio(value, min, max) {
    return ((value - min) / (max - min)).toFixed(2);
}

function getLinearGradientCSS(ratio, leftColor, rightColor) {
    return [
        '-webkit-gradient(',
        'linear, ',
        'left top, ',
        'right top, ',
        'color-stop(' + ratio + ', ' + leftColor + '), ',
        'color-stop(' + ratio + ', ' + rightColor + ')',
        ')'
    ].join('');
}

function updateRangeEl(rangeEl) {
    var ratio = valueTotalRatio(rangeEl.value, rangeEl.min, rangeEl.max);
    rangeEl.style.backgroundImage = getLinearGradientCSS(ratio, '#3b87fd', '#fffcfc');
}

function initRangeEl() {
    var rangeEl = document.getElementById("timeslieder");
    updateRangeEl(rangeEl);
    rangeEl.addEventListener("input", function(e) {
        updateRangeEl(e.target);
    });
}

$("#timeslieder")[0].addEventListener("input", function(e) {
    updateRangeEl(e.target);
    this.value = e.target.value;
    $("#track")[0].currentTime = e.target.value / 1000;
});