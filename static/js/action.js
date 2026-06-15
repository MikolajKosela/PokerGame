socket.on("checkState", (data) => {
    const target = data.state;
    if(window.location.pathname != target) {
        window.location.href = target;
    } else {
        socket.emit("gameDataRequest");
    }
});

socket.on("gameData", (data) => {
    const roundData = data.roundData;
    const buttons = data.buttons;
    const commonCards = data.commonCards;
    const playerCards = data.playerCards;
    const players = data.players;
    console.log(players);

    const commonCardsList = document.getElementById("commonCards");

    for(const card of commonCards.cards) {
        const li = document.createElement("li");

        if (card.visible) {
            let symbol = "?";
            let color = "?";
            switch (card.color) {
                case "Pik":
                    symbol = "♠";
                    color = "black";
                    break;
                case "Kier":
                    symbol = "♥";
                    color = "red";
                    break;
                case "Karo":
                    symbol = "♦";
                    color = "red";
                    break;

                case "Trefl":
                    symbol = "♣";
                    color = "black";
                    break;
                default:
                    symbol = "undefinded";
                    color = "undefinded";
            }

            li.innerHTML = `<span style="color: ${color};">${symbol}</span> ${card.number}`;
        } else {
            li.innerHTML = "???";
        }
        commonCardsList.appendChild(li);
    }
    
    const playerCardsList = document.getElementById("yourCards");

    for(const card of playerCards.cards) {
        const li = document.createElement("li");

        if (card.visible) {
            let symbol = "?";
            let color = "?";
            switch (card.color) {
                case "Pik":
                    symbol = "♠";
                    color = "black";
                    break;
                case "Kier":
                    symbol = "♥";
                    color = "red";
                    break;
                case "Karo":
                    symbol = "♦";
                    color = "red";
                    break;

                case "Trefl":
                    symbol = "♣";
                    color = "black";
                    break;
                default:
                    symbol = "undefinded";
                    color = "undefinded";
            }

            li.innerHTML = `<span style="color: ${color};">${symbol}</span> ${card.number}`;
        } else {
            li.innerHTML = "???";
        }
        playerCardsList.appendChild(li);
    }

    const pot = document.getElementById("pot");
    pot.innerHTML = "Całkowita pula wynosi: " + roundData.pot;
    const credits = document.getElementById("credits");
    credits.innerHTML =
        "Twoje żetony " + roundData.curCredit + " Do wyrównania: " + roundData.bet;

    const callBut = document.getElementById("call");
    callBut.innerHTML = "Sprawdź ( " + roundData.bet + " )";
    

    const playersList = document.getElementById("players");
    for(const player of players) {
        console.log(player.id, roundData.curID);
        if (player.id != roundData.curID) {
            const li = document.createElement("li");
            console.log(player);
            li.textContent =
                player.nickname + " - " + player.credits;
            playersList.appendChild(li);
        }
    }
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
/*
      async function whatRoundIs() {
        const res = await fetch("/whoseRound");
        const data = await res.json();
        if (data.round == -2) window.location.href = "/end";
        if (data.round == -1) window.location.href = "/";
      }

      whatRoundIs();
    </script>
    <form method="POST" id="actionForm"></form>

    <h3>Inni gracze:</h3>
    <ul id="players"></ul>

    <script>
      async function copyData() {
        const res = await fetch("/whoseRound");
        const data = await res.json();
        const pot = document.getElementById("pot");
        pot.innerHTML = "Całkowita pula wynosi: " + data.pot;
        const credits = document.getElementById("credits");
        credits.innerHTML =
          "Twoje żetony " + data.playerCredit + " Do wyrównania: " + data.bet;

        function changeValue(delta) {
          input = document.getElementById("");
          if (data.raiseButton) input = document.getElementById("raiseValue");
          else if (data.betButton) input = document.getElementById("betValue");
          let value = parseInt(input.value) || 1;
          value += delta;
          if (value < parseInt(input.min)) value = parseInt(input.min);
          input.value = value;
        }

        if (data.checkButton) {
          const form = document.getElementById("actionForm");
          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "check";
          button.value = "check";
          button.textContent = "Czekaj";
          button.className = "btn";
          form.appendChild(button);
        }

        if (data.betButton) {
          const form = document.getElementById("actionForm");
          const div = document.createElement("div");
          div.className = "cont";

          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "bet";
          button.value = "bet";
          button.textContent = "Postaw zakład";
          button.className = "btnl";
          div.appendChild(button);

          input = document.createElement("input");
          input.type = "number";
          input.id = "betValue";
          input.name = "betValue";
          input.className = "numInput";
          input.min = "1";
          input.step = "1";
          input.value = "1";
          div.appendChild(input);

          minus = document.createElement("button");
          minus.className = "btn";
          minus.textContent = "-";
          minus.type = "button";
          minus.addEventListener("click", function () {
            changeValue(-1);
          });

          plus = document.createElement("button");
          plus.className = "btnr";
          plus.textContent = "+";
          plus.type = "button";
          plus.addEventListener("click", function () {
            changeValue(1);
          });

          div.appendChild(minus);
          div.appendChild(plus);

          form.appendChild(div);
        }

        if (data.callButton) {
          const form = document.getElementById("actionForm");
          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "call";
          button.value = "call";
          button.textContent = "Sprawdź (" + data.bet + ")";
          button.className = "btn";
          form.appendChild(button);
        }

        if (data.raiseButton) {
          const form = document.getElementById("actionForm");
          const div = document.createElement("div");
          div.className = "cont";

          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "raise";
          button.value = "raise";
          button.textContent = "Podbij";
          button.className = "btnl";
          div.appendChild(button);

          input = document.createElement("input");
          input.type = "number";
          input.id = "raiseValue";
          input.name = "raiseValue";
          input.className = "numInput";
          input.min = "1";
          input.step = "1";
          input.value = "1";
          div.appendChild(input);

          minus = document.createElement("button");
          minus.className = "btn";
          minus.textContent = "-";
          minus.type = "button";
          minus.addEventListener("click", function () {
            changeValue(-1);
          });

          plus = document.createElement("button");
          plus.className = "btnr";
          plus.textContent = "+";
          plus.type = "button";
          plus.addEventListener("click", function () {
            changeValue(1);
          });

          div.appendChild(minus);
          div.appendChild(plus);

          form.appendChild(div);
        }

        if (data.foldButton) {
          const form = document.getElementById("actionForm");
          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "fold";
          button.value = "fold";
          button.textContent = "Pasuj";
          button.className = "btn";
          form.appendChild(button);
        }

        if (data.allinButton) {
          const form = document.getElementById("actionForm");
          button = document.createElement("button");
          button.type = "submit";
          button.name = "action";
          button.id = "allin";
          button.value = "allin";
          button.textContent = "ALL IN 🔥🔥🔥";
          button.className = "btn";
          form.appendChild(button);
        }

        const r = await fetch("/players");
        const d = await r.json();
        const list = document.getElementById("players");
        list.innerHTML = "";
        var cnt = 0;
        d.forEach(function (player) {
          if (data.yourId != cnt) {
            const li = document.createElement("li");
            if (cnt == 0)
              li.textContent =
                player.nickname + " - " + player.credits + " (admin)";
            else li.textContent = player.nickname + " - " + player.credits;
            list.appendChild(li);
          }
          cnt += 1;
        });
      }

      copyData();
      setInterval(whatRoundIs, 1000);
    </script>

*/