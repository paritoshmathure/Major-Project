console.log("Welcome to Spotify");

// Initialize the Variables
let songIndex = 0;
let audioElement = new Audio("static/songs/happy/1.mp3");
let masterPlay = document.getElementById('masterPlay');
let myProgressBar = document.getElementById('myProgressBar');
let gif = document.getElementById('gif');
let masterSongName = document.getElementById('masterSongName');
let songItems = Array.from(document.getElementsByClassName('songItem'));

let songs = [
    {songName: "Dancing-On-Dangerous-feat.-Sofia-Reyes", filePath: 'static/songs/happy/1.mp3' , coverPath: "static/covers/happy/1.jpg"},
    {songName: "Follow-You", filePath: 'static/songs/happy/2.mp3' , coverPath: "static/covers/happy/2.jpg"},
    {songName: "Bruno_Mars_-_Just_the_Way_You_Are", filePath: "static/songs/happy/3.mp3" , coverPath: "static/covers/happy/3.jpg"},
    {songName: "Cheap-Thrills-Sia-SOUNDOFNAJIA", filePath: "static/songs/happy/4.mp3", coverPath: "static/covers/happy/4.jpg"},
    {songName: "Clean_Bandit_feat_Iann_Dior_-_Higher", filePath: "static/songs/happy/5.mp3", coverPath: "static/covers/happy/5.jpg"},
    {songName: "Coldplay-Adventure-Of-A-Lifetime", filePath: "static/songs/happy/6.mp3", coverPath: "static/covers/happy/6.jpg"},
    {songName: "Electric Katy Perry 128 Kbps", filePath: "static/songs/happy/7.mp3", coverPath: "static/covers/happy/7.jpg"},
    {songName: "Floating Through Space Sia 128 Kbps", filePath: "static/songs/happy/8.mp3", coverPath: "static/covers/happy/8.jpg"},
    {songName: "Majid_Jordan_-_Waves_of_Blue_SkinnyGistcom_", filePath: "static/songs/happy/9.mp3", coverPath: "static/covers/happy/9.jpg"},
    {songName: "Stereo-Hearts", filePath: "static/songs/happy/10.mp3", coverPath: "static/covers/happy/10.jpg"}
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
        audioElement.src = `static/songs/happy/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/happy/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/happy/${songIndex+1}.mp3`;
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