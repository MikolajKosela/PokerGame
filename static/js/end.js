import { processGameData } from "./common.js";
import { drawCards } from "./common.js";

socket.on("gameData", (data) => {
  console.log(data);
  processGameData(data, window.location.pathname);
});

const players = new Map();

function displayHistory(data) {
  const div = document.getElementById("history");
  if (div == null) {
    return;
  }
  while (div.children.length > 0) {
    div.removeChild(div.lastChild);
  }

  for (const log of data) {
    const p = document.createElement("p");
    p.innerHTML = log.message;
    div.append(p);
  }
}

socket.on("summary", (data) => {
  console.log("Podsumowanie");
  console.log(data);

  let AmIadmin = false;
  if (localStorage.getItem("admin") == "true") {
    AmIadmin = true;
  }
  const container = document.getElementById("summary");

  if (container == null) {
    return;
  }

  container.innerHTML = '';

  for(const player of data.players) {
    console.log(player);
    const div = document.createElement("div");
    div.innerHTML = `<h3>${player.nickname} - ${player.credits}</h3>`;

    const list = document.createElement("ul");
    list.className = "cards";

    drawCards(player.cards, list);

    div.appendChild(list);
  
    if(player.result != null) {
      const result = document.createElement("h3");
      result.innerHTML = player.result;
      div.appendChild(result);
    }

    if (AmIadmin == true && !player.fold && data.gamePot > 0) {
      players.set(player.id, {selected: false});

      const button = document.createElement("button");
      button.className = "btn";
      button.textContent = player.nickname;
      button.id = "Button" + player.id;
      button.addEventListener("click", () => choose(player.id));
      div.appendChild(button);

      const chosen = document.createElement("a");
      chosen.id = "chosen" + player.id;
      chosen.innerHTML = "";
      div.append(chosen);
    }
    container.appendChild(div);
  }
  console.log("gracze: ");
  console.log(players);

  if (AmIadmin == true) {
    document.getElementById("sendForm").className = true;
    const button = document.getElementById("send");
    button.addEventListener("click", () => sendWinners());
  }

  displayHistory(data.history);
})

function choose(id) {
  console.log(id);
  players.get(id).selected = !players.get(id).selected;
  const chosen = document.getElementById("chosen" + id);
  if (players.get(id).selected == true) {
    chosen.innerHTML = "Wybrany";
  } else {
    chosen.innerHTML = "";
  }
  console.log(players);
}

function sendWinners() {
  const winners = [];
  for (const [id, player] of players) {
    console.log(player.selected);

    if (player.selected == true) {
      winners.push(id);
    }
  }
  socket.emit("winners", winners);
}

socket.on("creditsGranted", () => {
  socket.emit("gameDataRequest");
  if (localStorage.getItem("admin") == "true") {
    const button = document.getElementById("send");
    button.innerHTML = "Nowe rozdanie";
    button.addEventListener("click", () => newDeal());

    console.log("USUWAM PRZYCISKI");
    console.log(players);
    for (const [id, _] of players) {
      const pbutton = document.getElementById("Button" + id);
      console.log(pbutton);
      console.log(id);
      if (pbutton != null) {
        pbutton.className = "hidden";
      }
    }
  }
})

function newDeal() {
  socket.emit("newDeal");
}
