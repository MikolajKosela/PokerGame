import { checkState } from "./common.js";

const button = document.getElementById("join");
button.addEventListener("click", () => join());

socket.on("gameData", (data) => {
  console.log(data);
  if (checkState(data, window.location.pathname) == 0) {
    window.location.href = data.state;
  }
  socket.emit("startDataRequest");
});

socket.on("joined", (data) => {
  localStorage.setItem("token", data.token);
  console.log(localStorage.getItem("token"));
  window.location.href = "/lobby";
});

function join() {
  let nickname = document.getElementById("nickname").value;
  localStorage.setItem("nickname", nickname);

  console.log("Wywołuje joina");
  socket.emit("join", {
    nickname : nickname
  });
}

socket.on("startData", (data) => {
  console.log(data);
  const info = document.getElementById("playersInfo");
  if (info != null) {
    if (data.started == true) {
      info.innerHTML = "Nie możesz dołączyć w trakcie trwającej rozgrywki"; 
    } else {
      if (data.playersNum == 0) {
          info.innerHTML = "Dołącz do lobby jako pierwszy";
      } else if (data.playersNum == 1) {
          info.innerHTML = "W lobby czeka: " + data.playersNum + " gracz";
      } else {
          info.innerHTML = "W lobby czeka: " + data.playersNum + " graczy";
      }
    } 
  }
}) 