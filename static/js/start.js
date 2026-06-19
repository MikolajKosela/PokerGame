import { processGameData } from "./common.js";

socket.on("checkState", (data) => {
  const target = data.state;
    if (window.location.pathname != target) {
      window.location.href = target;
    } else {
      const button = document.getElementById("join");
      button.addEventListener("click", () => join());
      socket.emit("gameDataRequest");
    }
  });

socket.on("gameData", (data) => {
  console.log(data);
  processGameData(data);
});

socket.on("joined", (data) => {
  localStorage.setItem("token", data.token);
  console.log(localStorage.getItem("token"));
  window.location.href = "/lobby";
});

function join() {
  let nickname = document.getElementById("nickname").value;
  localStorage.setItem("nickname", nickname);

  socket.emit("join", {
    nickname : nickname
  });
}