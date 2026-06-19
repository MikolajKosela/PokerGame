import { checkState } from "./common.js";

const button = document.getElementById("join");
button.addEventListener("click", () => join());

socket.on("gameData", (data) => {
  console.log(data);
  if (checkState(data, window.location.pathname) == 0) {
    window.location.href = data.state;
  }
  socket.emit("lobbyUpdateRequest");
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

socket.on("lobbyUpdate", (data) => {
  const playersNum = document.getElementById("playersNum");
  if (playersNum != null) {
      if (data.playersNum == 0) {
          playersNum.innerHTML = "Dołącz do lobby jako pierwszy";
      } else if (data.playersNum == 1) {
          playersNum.innerHTML = "W lobby czeka: " + data.playersNum + " gracz";
      } else {
          playersNum.innerHTML = "W lobby czeka: " + data.playersNum + " graczy";
      }
  }
}) 