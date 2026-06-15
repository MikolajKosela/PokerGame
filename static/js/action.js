import { processGameData } from "./common.js";

socket.on("checkState", (data) => {
    const target = data.state;
    if(window.location.pathname != target) {
        window.location.href = target;
    } else {
        socket.emit("gameDataRequest");
    }
});

socket.on("gameData", (data) => {
  processGameData(data);
})

function changeValue(where, howMuch) {
  const target = document.getElementById(where);
  let value = parseInt(target.value) || 1;
  value += howMuch;
  if (value < parseInt(target.min)) {
    value = parseInt(target.min);
  }
  target.value = value;
}

socket.on("actionMade", () => {
  window.location.href = "/wait";
})

function check() {
  console.log("check");
  socket.emit("check");
}

function bet() {
  const amount = document.getElementById("betValue");
  console.log("bet: ", amount.value);
  socket.emit("bet", {amount: amount.value});
}

function call() {
  console.log("call");
  socket.emit("call");
}

function raise() {
  const amount = document.getElementById("raiseValue");
  console.log("raise: ", amount.value);
  socket.emit("raise", {amount: amount.value});
}

function fold() {
  console.log("fold");
  socket.emit("fold");
}

function allin() {
  console.log("allin");
  socket.emit("allin");
}