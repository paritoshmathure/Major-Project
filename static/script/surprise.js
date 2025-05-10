console.log("Welcome to Spotify");

// Initialize the Variables
let songIndex = 0;
let audioElement = new Audio("static/songs/surprise/1.mp3");
let masterPlay = document.getElementById('masterPlay');
let myProgressBar = document.getElementById('myProgressBar');
let gif = document.getElementById('gif');
let masterSongName = document.getElementById('masterSongName');
let songItems = Array.from(document.getElementsByClassName('songItem'));

let songs = [
    {songName: "24kGoldn-Mood", filePath: 'static/songs/surprise/1.mp3' , coverPath: "static/covers/surprise/1.jpg"},
    {songName: "Bruno-Mars-Leave-The-Door-Open-Ft-Anderson-Paak-And-Silk-Sonic-(TrendyBeatz.com)", filePath: 'static/songs/surprise/2.mp3' , coverPath: "static/covers/surprise/2.jpg"},
    {songName: "BTS - Dynamite- [MyMp3Bhojpuri.In]", filePath: "static/songs/surprise/3.mp3" , coverPath: "static/covers/surprise/3.jpg"},
    {songName: "Favourite Crime ! Olivia Rodrigo ! English ! Song", filePath: "static/songs/surprise/4.mp3", coverPath: "static/covers/surprise/4.jpg"},
    {songName: "Justin-Bieber-Peaches-Ft-Daniel-Caesar-Giveon-(TrendyBeatz.com)", filePath: "static/songs/surprise/5.mp3", coverPath: "static/covers/surprise/5.jpg"},
    {songName: "Maroon_5_Ft_Megan_Thee_Stallion_-_Beautiful_Mistakes_Soloplay.ng", filePath: "static/songs/surprise/6.mp3", coverPath: "static/covers/surprise/6.jpg"},
    {songName: "Masked_Wolf_-_Astronaut_In_The_Ocean_(sound-library.net)", filePath: "static/songs/surprise/7.mp3", coverPath: "static/covers/surprise/7.jpg"},
    {songName: "The_Weeknd_Ft_Ariana_Grande_-_Save_Your_Tears_Remix_", filePath: "static/songs/surprise/8.mp3", coverPath: "static/covers/surprise/8.jpg"},
    {songName: "Watermelon Sugar - Seaside SEB(PagalWorld)", filePath: "static/songs/surprise/9.mp3", coverPath: "static/covers/surprise/9.jpg"},
    {songName: "Your Love (9PM) &#8211; ATB, Topic, A7S-ringtones247.info", filePath: "static/songs/surprise/10.mp3", coverPath: "static/covers/surprise/10.jpg"}
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
        audioElement.src = `static/songs/surprise/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/surprise/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/surprise/${songIndex+1}.mp3`;
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