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
  updateButtons(data.buttons)
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
    const buttton = document.getElementById(target);
    const minus = document.getElementById(target + "Minus");
    const plus = document.getElementById(target + "Plus");

    contener.className = "cont";
    buttton.addEventListener("click", actions[target]);
    minus.addEventListener("click", () => changeValue(target + "Value", -1));
    plus.addEventListener("click", () => changeValue(target + "Value", 1));
  } else {
    const buttton = document.getElementById(target);

    buttton.className = "btn";
    buttton.addEventListener("click", actions[target]);
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


  /*
  const checkBut = document.getElementById("check");

  const betCont = document.getElementById("betCont");
  const betBut = document.getElementById("bet");
  const betMinus = document.getElementById("betMinus");
  const betPlus = document.getElementById("betPlus");

  const callBut = document.getElementById("call");

  const raiseCont = document.getElementById("raiseCont");
  const raiseBut = document.getElementById("raise");
  const raiseMinus = document.getElementById("raiseMinus");
  const raisePlus = document.getElementById("raisePlus");

  const foldBut = document.getElementById("fold");
  const allinBut = document.getElementById("allin");

  if (data.check == true) {
    checkBut.className = "btn";
    checkBut.addEventListener("click", check);
  }

  if (data.bet == true) {
  betCont.className = "cont";
  betBut.addEventListener("click", bet);
  betMinus.addEventListener("click", () => changeValue('betValue', -1));
  betPlus.addEventListener("click", () => changeValue('betValue', 1));
  }

  if (data.call == true) {
  callBut.className = "btn";
  callBut.addEventListener("click", call);
  }

  if (data.raise == true) {
  raiseCont.className = "cont";
  raiseBut.addEventListener("click", raise);
  raiseMinus.addEventListener("click", () => changeValue('raiseValue', -1));
  raisePlus.addEventListener("click", () => changeValue('raiseValue', 1));
  }

  if (data.fold == true) {
  foldBut.className = "btn";
  foldBut.addEventListener("click", fold);
  }

  if (data.allin == true) {
  allinBut.className = "btn";
  allinBut.addEventListener("click", allin);
  }
  */
}