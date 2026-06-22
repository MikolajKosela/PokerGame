function updateRound(data) {
    if (data == null) {
        return;
    }
    const pot = document.getElementById("pot");
    if (pot != null) {
        pot.innerHTML = "Całkowita pula wynosi: " + data.pot;
    }

    const credits = document.getElementById("credits");
    if (credits != null) {
        credits.innerHTML =
         "Twoje żetony " + data.credits + " Do wyrównania: " + data.bet;
    }

    const callBut = document.getElementById("call");
    if (callBut != null) {
        callBut.innerHTML = "Sprawdź ( " + data.bet + " )";
    }

    if (data.lastRoundSkipped == true) {
        addMessage("infoBox", "Poprzednia runda została pominięta, <br>ponieważ żaden z graczy nie miał decyzji do podjęcia<br>", "info");
    }

    if (data.yourRoundSkipped == true) {
        addMessage("infoBox", "Twoja kolejka została pominięta, <br>poniważ nie miałeś decyzji do pojęcia<br>", "info");
    }
}

export function drawCards(cards, list) {
    if (list == null || cards == null) {
        return;
    }

    list.innerHTML='';

    for(const card of cards) {
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
        list.appendChild(li);
    }
}

function updateCommonCards(data) {
    if (data != null) {
        drawCards(data.cards, document.getElementById("commonCards"));
    }
}

function updatePlayerCards(data) {
    if (data != null) {
        drawCards(data.cards, document.getElementById("yourCards"));
    }
}

function updatePlayers(data) {
    const playersList = document.getElementById("players");
    if (playersList == null) {
        return;
    }
    playersList.innerHTML = '';

    for(const player of data) {
        const li = document.createElement("li");
        console.log(player);

        if (player.id == 0) {
            li.textContent = player.nickname + " - " + player.credits + " (admin)";
        } else {
            li.textContent = player.nickname + " - " + player.credits;
        }
        playersList.appendChild(li);
    }
}

export function checkState(data, where) {
    console.log("Gdzie jestem: ", where, "Gdzie mam być: ", data.state);
    if (where != data.state) {
        return 0;
    }
    return 1;
}

export function processGameData(data, where) {

    console.log("data", data);
    if (checkState(data, where) == 0) {
        window.location.href = data.state;
        return 0;
    } else {
        clearContent("infoBox");

        updateRound(data.roundData);
        updateCommonCards(data.commonCards);
        updatePlayerCards(data.playerCards);
        updatePlayers(data.players);
        return 1;
    }
}

function clearContent(id) {
    const div = document.getElementById(id);
    if (div == null) {
        return;
    }

    while (div.children.length > 0) {
        div.removeChild(div.firstChild);
    }
}

function addMessage(id, content, style) {
    const div = document.getElementById(id);

    if (div == null) {
        return;
    }

    const p = document.createElement("p");
    p.innerHTML = content;
    p.className = style;
    div.prepend(p);

    while (div.children.length > 5) {
        div.removeChild(div.lastChild);
    }
}

socket.on("message", (data) => {
    console.log(data);
    addMessage("infoBox", data.content, data.style);
})

socket.on("logs", (data) => {
    for(const log of data) {
        addMessage("gameHistory", log.message);
    }
})