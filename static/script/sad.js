console.log("Welcome to Spotify");

// Initialize the Variables
let songIndex = 0;
let audioElement = new Audio("static/songs/sad/1.mp3");
let masterPlay = document.getElementById('masterPlay');
let myProgressBar = document.getElementById('myProgressBar');
let gif = document.getElementById('gif');
let masterSongName = document.getElementById('masterSongName');
let songItems = Array.from(document.getElementsByClassName('songItem'));

let songs = [
    {songName: "Adele-Someone-Like-You-(TrendyBeatz.com)", filePath: 'static/songs/sad/1.mp3' , coverPath: "static/covers/sad/1.jpg"},
    {songName: "Ashe - Till Forever Falls Apart Ft. Finneas (Pendona.com)", filePath: 'static/songs/sad/2.mp3' , coverPath: "static/covers/sad/2.jpg"},
    {songName: "Gnash-I-Hate-You-I-Love-You-ft.-Olivia-Obrien-Mybestfeelings.com_", filePath: "static/songs/sad/3.mp3" , coverPath: "static/covers/sad/3.jpg"},
    {songName: "James_Arthur_-_Say_You_Wont_Let_Go_[NaijaGreen.Com]_", filePath: "static/songs/sad/4.mp3", coverPath: "static/covers/sad/4.jpg"},
    {songName: "Kina-get-you-the-moon-ft.-Snow", filePath: "static/songs/sad/5.mp3", coverPath: "static/covers/sad/5.jpg"},
    {songName: "Lewis Capaldi Someone You Loved Lyrics(RemixZilla.Com)", filePath: "static/songs/sad/6.mp3", coverPath: "static/covers/sad/6.jpg"},
    {songName: "Lil-Nas-X-That's-What-I-Want-(TrendyBeatz.com)", filePath: "static/songs/sad/7.mp3", coverPath: "static/covers/sad/7.jpg"},
    {songName: "Post_Malone_-_Circles_talkglitz.tv", filePath: "static/songs/sad/8.mp3", coverPath: "static/covers/sad/8.jpg"},
    {songName: "Sam_Smith_-_Dancing_With_a_Stranger_ft_Normani", filePath: "static/songs/sad/9.mp3", coverPath: "static/covers/sad/9.jpg"},
    {songName: "Xxxtentacion_-_Everybody_Dies_In_Their_Nightmares", filePath: "static/songs/sad/10.mp3", coverPath: "static/covers/sad/10.jpg"}
]

songItems.forEach((element, i)=>{ 
    element.getElementsByTagName("img")[0].src = songs[i].coverPath; 
    element.getElementsByClassName("songName")[0].innerText = songs[i].songName; 
})
 

// Handle play/pause click
masterPlay.addEventListener('click', ()=>{
    if(audioElement.paused || audioElement.currentTime<=0){
        audioElement.play();
        masterPlay.classList.remove('fa-play-circle');
        masterPlay.classList.add('fa-pause-circle');
        gif.style.opacity = 1;
    }
    else{
        audioElement.pause();
        masterPlay.classList.remove('fa-pause-circle');
        masterPlay.classList.add('fa-play-circle');
        gif.style.opacity = 0;
    }
})
// Listen to Events
audioElement.addEventListener('timeupdate', ()=>{ 
    // Update Seekbar
    progress = parseInt((audioElement.currentTime/audioElement.duration)* 100); 
    myProgressBar.value = progress;
})

myProgressBar.addEventListener('change', ()=>{
    audioElement.currentTime = myProgressBar.value * audioElement.duration/100;
})

const makeAllPlays = ()=>{
    Array.from(document.getElementsByClassName('songItemPlay')).forEach((element)=>{
        element.classList.remove('fa-pause-circle');
        element.classList.add('fa-play-circle');
    })
}
ext = ".mp3";
Array.from(document.getElementsByClassName('songItemPlay')).forEach((element)=>{
    element.addEventListener('click', (e)=>{ 
        makeAllPlays();
        songIndex = parseInt(e.target.id);
        e.target.classList.remove('fa-play-circle');
        e.target.classList.add('fa-pause-circle');
        audioElement.src = `static/songs/sad/${songIndex+1}.mp3`;
        masterSongName.innerText = songs[songIndex].songName;
        audioElement.currentTime = 0;
        audioElement.play();
        gif.style.opacity = 1;
        masterPlay.classList.remove('fa-play-circle');
        masterPlay.classList.add('fa-pause-circle');
    })
})

document.getElementById('next').addEventListener('click', ()=>{
    if(songIndex>=9){
        songIndex = 0;
    }
    else{
        songIndex += 1;
    }
    audioElement.src = `static/songs/sad/${songIndex+1}.mp3`;
    masterSongName.innerText = songs[songIndex].songName;
    audioElement.currentTime = 0;
    audioElement.play();
    masterPlay.classList.remove('fa-play-circle');
    masterPlay.classList.add('fa-pause-circle');

})

document.getElementById('previous').addEventListener('click', ()=>{
    if(songIndex<=0){
        songIndex = 0;
    }
    else{
        songIndex -= 1;
    }
    audioElement.src = `static/songs/sad/${songIndex+1}.mp3`;
    masterSongName.innerText = songs[songIndex].songName;
    audioElement.currentTime = 0;
    audioElement.play();
    masterPlay.classList.remove('fa-play-circle');
    masterPlay.classList.add('fa-pause-circle');
})

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }