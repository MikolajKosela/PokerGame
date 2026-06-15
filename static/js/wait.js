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
/*
    <script>
      async function printCommonCards() {
        const res = await fetch("/commonCards");
        const data = await res.json();
        const list = document.getElementById("commonCards");
        list.innerHTML = "";
        data.cards.forEach(function (card) {
          const li = document.createElement("li");
          if (card.visible) {
            let symbol = "";
            let color = "black"; // domyślny kolor

            if (card.color == "Pik") {
              symbol = "♠";
            } else if (card.color == "Kier") {
              symbol = "♥";
              color = "red";
            } else if (card.color == "Karo") {
              symbol = "♦";
              color = "red";
            } else if (card.color == "Trefl") {
              symbol = "♣";
            } else {
              // jeśli inny kolor, po prostu pokaż tekst
              li.textContent = card.color + " " + card.number;
              return;
            }

            // używamy innerHTML, aby dodać kolor
            li.innerHTML = `<span style="color: ${color};">${symbol}</span> ${card.number}`;
          } else {
            li.textContent = "???";
          }
          list.appendChild(li);
        });
      }
      printCommonCards();
    </script>

    <h2>Twoje karty</h2>

    <ul id="yourCards"></ul>
    <h3 id="currentPlayer"></h3>
    <h3>Inni gracze:</h3>
    <ul id="players"></ul>
    <script>
      async function printYourCards() {
        const res = await fetch("/yourCards");
        const data = await res.json();
        const list = document.getElementById("yourCards");
        list.innerHTML = "";
        data.cards.forEach(function (card) {
          const li = document.createElement("li");
          if (card.visible) {
            let symbol = "";
            let color = "black"; // domyślny kolor

            if (card.color == "Pik") {
              symbol = "♠";
            } else if (card.color == "Kier") {
              symbol = "♥";
              color = "red";
            } else if (card.color == "Karo") {
              symbol = "♦";
              color = "red";
            } else if (card.color == "Trefl") {
              symbol = "♣";
            } else {
              // jeśli inny kolor, po prostu pokaż tekst
              li.textContent = card.color + " " + card.number;
              return;
            }

            // używamy innerHTML, aby dodać kolor
            li.innerHTML = `<span style="color: ${color};">${symbol}</span> ${card.number}`;
          } else {
            li.textContent = "???";
          }
          list.appendChild(li);
        });
      }
      async function whatRoundIs() {
        const res = await fetch("/whoseRound");
        const data = await res.json();
        const currentPlayer = document.getElementById("currentPlayer");
        if (data.round == -2) window.location.href = "/end";
        if (data.round == -1) window.location.href = "/";
        if (data.yourId == data.round) window.location.href = "/action";
        currentPlayer.innerHTML = "Trwa runda gracza: " + data.playerName;

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
      printYourCards();
      setInterval(whatRoundIs, 1000);
    </script>
*/