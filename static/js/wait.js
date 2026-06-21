import { processGameData } from "./common.js";

socket.on("gameData", (data) => {
  const roundInfo = document.getElementById("roundInfo");
  if (roundInfo != null) {
    roundInfo.innerHTML = "Poczekaj (trwa runda nr. " + data.roundData.roundNum + ")";
  }

  const curNick = document.getElementById("curNick");
  if (curNick != null) {
    curNick.innerHTML = "Akcję wykonuje gracz: " + data.roundData.curNick;
  }

  processGameData(data, window.location.pathname);
});