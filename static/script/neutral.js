console.log("Welcome to Spotify");

// Initialize the Variables
let songIndex = 0;
let audioElement = new Audio("static/songs/neutral/1.mp3");
let masterPlay = document.getElementById('masterPlay');
let myProgressBar = document.getElementById('myProgressBar');
let gif = document.getElementById('gif');
let masterSongName = document.getElementById('masterSongName');
let songItems = Array.from(document.getElementsByClassName('songItem'));

let songs = [
    {songName: "Believer_192(PagalWorld)", filePath: 'static/songs/neutral/1.mp3' , coverPath: "static/covers/neutral/1.jpg"},
    {songName: "Bruno_Mars_-_24K_Magic", filePath: 'static/songs/neutral/2.mp3' , coverPath: "static/covers/neutral/2.jpg"},
    {songName: "Camila_Cabello_ft_Young_Thug_-_Havana", filePath: "static/songs/neutral/3.mp3" , coverPath: "static/covers/neutral/3.jpg"},
    {songName: "Chainsmokers_Coldplay_-_Just_Like_This_CeeNaija.com_", filePath: "static/songs/neutral/4.mp3", coverPath: "static/covers/neutral/4.jpg"},
    {songName: "Ed-Sheeran-Galway-Girl-via-Naijafinix.com_", filePath: "static/songs/neutral/5.mp3", coverPath: "static/covers/neutral/5.jpg"},
    {songName: "Faded_192(PaglaSongs)", filePath: "static/songs/neutral/6.mp3", coverPath: "static/covers/neutral/6.jpg"},
    {songName: "Perfect-Ed-Sheeran_320-MostMags", filePath: "static/songs/neutral/7.mp3", coverPath: "static/covers/neutral/7.jpg"},
    {songName: "Shape of You(PagalWorld.com.se)", filePath: "static/songs/neutral/8.mp3", coverPath: "static/covers/neutral/8.jpg"},
    {songName: "Shawn_Mendes_-_Theres_Nothing_Holding_Me_Back_[NaijaGreen.Com]_", filePath: "static/songs/neutral/9.mp3", coverPath: "static/covers/neutral/9.jpg"},
    {songName: "Twenty-One-Pilots-Heathens-Mybestfeelings.com_", filePath: "static/songs/neutral/10.mp3", coverPath: "static/covers/neutral/10.jpg"}
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
        audioElement.src = `static/songs/neutral/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/neutral/${songIndex+1}.mp3`;
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
    audioElement.src = `static/songs/neutral/${songIndex+1}.mp3`;
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