import { processGameData } from "./common.js";

initActions();
const gameState = {
  gameBet: 0,
  callCost: 0,
  betCost: 0,
  raiseCost: 0,
}

function initActions() {
  document.getElementById("check").addEventListener("click", check);
  document.getElementById("bet").addEventListener("click", bet);
  document.getElementById("call").addEventListener("click", call);
  document.getElementById("fold").addEventListener("click", fold);
  document.getElementById("raise").addEventListener("click", raise);
  document.getElementById("allin").addEventListener("click", allin);

  document.getElementById("betMinus").addEventListener("click", () => changeValue("bet", -1));
  document.getElementById("betPlus").addEventListener("click", () => changeValue("bet", 1));

  document.getElementById("raiseMinus").addEventListener("click", () => changeValue("raise", -1));
  document.getElementById("raisePlus").addEventListener("click", () => changeValue("raise", 1));

  document.getElementById("betValue").addEventListener("input", () => updateBut("bet"));
  document.getElementById("raiseValue").addEventListener("input", () => updateBut("raise"));
}

function action(data) {
    const div = document.getElementById("action");
    div.className = "";

    const prevDiv = document.getElementById("wait");
    prevDiv.className = "hidden";

    const roundInfo = document.getElementById("roundInfo");

    if (roundInfo != null) {
        roundInfo.innerHTML = "Twoja kolej (trwa runda nr. " + data.roundData.roundNum + ")";
    }

    updateButtons(data.buttons);
}

function wait(data) {
    const div = document.getElementById("wait");
    div.className = "";

    const prevDiv = document.getElementById("action");
    prevDiv.className = "hidden";

    const roundInfo = document.getElementById("roundInfo");

    if (roundInfo != null) {
        roundInfo.innerHTML = "Poczekaj (trwa runda nr. " + data.roundData.roundNum + ")";
    }
        
    const curNick = document.getElementById("curNick");
    if (curNick != null) {
        curNick.innerHTML = "Akcję wykonuje gracz: " + data.roundData.curNick;
    }

}

socket.on("gameData", (data) => {
    console.log("MAM dane", data);
    if (data.roundData != null) {
      gameState.gameBet = data.roundData.bet;
    }

    if (processGameData(data, window.location.pathname) == 1) {  
        if (data.roundData.yourRound == true) {
            console.log("AKCJA");
            gameState.callCost = gameState.gameBet;
            gameState.betCost = 1;
            gameState.raiseCost = gameState.gameBet + 1;

            action(data);
        } else {
            console.log("CZEKAJ");
            wait(data);
        }
    }
})

function changeValue(target, howMuch) {
  console.log(target, howMuch);

  const input = document.getElementById(target + "Value");
  let value = parseInt(input.value) || 1;
  value += howMuch;

  if (value < parseInt(input.min)) {
    value = parseInt(input.min);
  }
  input.value = value;

  gameState[target + "Cost"] = gameState.gameBet + value;
  const amount = document.getElementById(target + "Amount");
  if (amount != null) {
    amount.innerHTML = gameState[target + "Cost"];
  }

  console.log("asdklajfkjdfklajd");
  console.log(gameState);
}

function check() {
  console.log("check");
  socket.emit("check");
}

function bet() {
  const amount = gameState.betCost;
  console.log("bet: ", amount);
  socket.emit("bet", {amount: amount});
}

function call() {
  console.log("call");
  socket.emit("call");
}

function raise() {
  const amount = gameState.raiseCost;
  document.getElementById("raiseValue");
  console.log("raise: ", amount);
  socket.emit("raise", {amount: amount});
}

function fold() {
  console.log("fold");
  socket.emit("fold");
}

function allin() {
  console.log("allin");
  socket.emit("allin");
}

function updateBut(target) {
  console.log("dafkjakldfjafl", target);
  if (target == "bet" || target == "raise") {
    const contener = document.getElementById(target + "Cont");
    contener.className = "cont";
  } else {
    const buttton = document.getElementById(target);
    buttton.className = "btn";
  }

  const input = document.getElementById(target + "Value");
  const amount = document.getElementById(target + "Amount");

  if (input != null && amount != null) {
    let value = parseInt(input.value) || 1;
    console.log(value);

    gameState[target + "Cost"] = gameState.gameBet + value;
    if (amount != null) {
      amount.innerHTML = gameState[target + "Cost"];
    }

  }
}

function updateButtons(data) {
  if (data == null) {
    return;
  }

  console.log(data);

  if (data.check == true) {
    updateBut("check");
  } else {
    document.getElementById("check").className = "hidden";
  }

  if (data.bet == true) {
    updateBut("bet");
  } else {
    document.getElementById("betCont").className = "hidden";
  }

  if (data.call == true) {
    updateBut("call");
  } else {
    document.getElementById("call").className = "hidden";
  }

  if (data.raise == true) {
    updateBut("raise");
  } else {
    document.getElementById("raiseCont").className = "hidden";
  }

  if (data.fold == true) {
    updateBut("fold");
  } else {
    document.getElementById("fold").className = "hidden";
  }

  if (data.allin == true) {
    updateBut("allin");
  } else {
    document.getElementById("allin").className = "hidden";
  }
}