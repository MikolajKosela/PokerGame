import { processGameData } from "./common.js";

const welcome=document.getElementById("welcome");
let nickname=localStorage.getItem("nickname");
welcome.innerHTML="Witaj "+nickname;

socket.on("checkState", (data) => {
    const target = data.state;
    if(window.location.pathname != target) {
        window.location.href = target;
    } else {
        if (localStorage.getItem("admin") == "true") {
            const button = document.getElementById("start");
            button.addEventListener("click", () => start());
            button.className = "btn";
        }
        socket.emit("gameDataRequest");
    }
});

socket.on("gameData", (data) => {
  console.log(data);
  processGameData(data);
});

function start() {
    if (localStorage.getItem("admin") == "true") {
        socket.emit("startGame");
    }
}

socket.on("started", () => {
    socket.emit("checkStateRequest");
})