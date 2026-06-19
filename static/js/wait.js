import { processGameData } from "./common.js";

socket.on("gameData", (data) => {
  processGameData(data, window.location.pathname);
});