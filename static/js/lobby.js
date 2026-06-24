import { processGameData } from "./common.js";

const welcome=document.getElementById("welcome");
let nickname=localStorage.getItem("nickname");
welcome.innerHTML="Witaj "+nickname;

socket.on("gameData", (data) => {
  console.log(data);
  processGameData(data, window.location.pathname);
  if (localStorage.getItem("admin") == "true") {
    const button = document.getElementById("start");
    button.addEventListener("click", () => start());
    button.className = "btn";
    }
});

function start() {
    socket.emit("startGame");
}