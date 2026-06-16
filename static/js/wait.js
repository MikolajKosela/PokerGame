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
});

socket.on("actionMade", () => {
  socket.emit("checkStateRequest");
})