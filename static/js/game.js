import { processGameData } from "./common.js";

initActions();

function initActions() {
  document.getElementById("check").addEventListener("click", check);
  document.getElementById("bet").addEventListener("click", bet);
  document.getElementById("call").addEventListener("click", call);
  document.getElementById("fold").addEventListener("click", fold);
  document.getElementById("raise").addEventListener("click", raise);
  document.getElementById("allin").addEventListener("click", allin);

  document.getElementById("betMinus").addEventListener("click", () => changeValue("betValue", -1));
  document.getElementById("betPlus").addEventListener("click", () => changeValue("betValue", 1));

  document.getElementById("raiseMinus").addEventListener("click", () => changeValue("raiseValue", -1));
  document.getElementById("raisePlus").addEventListener("click", () => changeValue("raiseValue", 1));
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
    console.log("MAM dane");
    if (processGameData(data, window.location.pathname) == 1) {  
        if (data.roundData.yourRound == true) {
            console.log("AKCJA");
            action(data);
        } else {
            console.log("CZEKAJ");
            wait(data);
        }
    }
})

function changeValue(where, howMuch) {
  console.log(where, howMuch);

  const target = document.getElementById(where);
  let value = parseInt(target.value) || 1;
  value += howMuch;
  if (value < parseInt(target.min)) {
    value = parseInt(target.min);
  }
  target.value = value;
}

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

function updateBut(target) {
  const actions = {
    check: check,
    bet: bet,
    call: call,
    fold: fold,
    raise: raise,
    allin: allin
  };

  if (target == "bet" || target == "raise") {
    const contener = document.getElementById(target + "Cont");
    contener.className = "cont";
  } else {
    const buttton = document.getElementById(target);
    buttton.className = "btn";
  }
}

function updateButtons(data) {
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