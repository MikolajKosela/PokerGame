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
/*
    <script>
      let AmIadmin = false;

      async function showSummary() {
        const res = await fetch("/summary");
        const data = await res.json();

        const r = await fetch("/whoseRound");
        const d = await r.json();

        const container = document.getElementById("summaryC");
        container.innerHTML = "";

        data.forEach((player) => {
          const div = document.createElement("div");
          div.innerHTML = `<h3>${player.nickname} - ${player.credits}</h3>`;
          if (AmIadmin && !player.fold && d.pot != 0) {
            const button = document.createElement("button");
            button.className = "btn";
            button.textContent = player.nickname;
            button.type = "submit";
            button.name = "action";
            button.value = player.id;
            button.id = "Button" + player.id;
            div.appendChild(button);
          }
          const ul = document.createElement("ul");
          player.cards.forEach((card) => {
            const li = document.createElement("li");
            if (card.visible) {
              let symbol = "";
              let color = "black";

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
                li.textContent = card.color + " " + card.number;
                return;
              }

              li.innerHTML = `<span style="color: ${color};">${symbol}</span> ${card.number}`;
            } else {
              li.textContent = "???";
            }
            ul.appendChild(li);
          });
          div.appendChild(ul);
          container.appendChild(div);
        });
        if (AmIadmin && d.pot == 0) {
          button = document.createElement("button");
          button.className = "btn";
          button.textContent = "Kolejne rozdanie";
          button.name = "action";
          button.value = "again";
          container.appendChild(button);
        }
      }

      async function takeData() {
        const res = await fetch("/whoseRound");
        const data = await res.json();
        if (data.round == 0) window.location.href = "/wait";
        if (data.round == -1) window.location.href = "/";
        if (data.pot != 0) {
          pot = document.getElementById("gamePot");
          pot.innerHTML = "Pula wynosi: " + data.pot;
        }
        if (data.yourId == 0) AmIadmin = true;
        showSummary();
      }
      takeData();
      setInterval(takeData, 1000);
    </script>
    */