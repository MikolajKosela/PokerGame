function updateRound(data) {
    const pot = document.getElementById("pot");
    if (pot != null) {
        pot.innerHTML = "Całkowita pula wynosi: " + data.pot;
    }

    const credits = document.getElementById("credits");
    if (credits != null) {
        credits.innerHTML =
         "Twoje żetony " + data.yourCredits + " Do wyrównania: " + data.bet;
    }

    const callBut = document.getElementById("call");
    if (callBut != null) {
        callBut.innerHTML = "Sprawdź ( " + data.bet + " )";
    }

    if (data.lastRoundSkipped == true) {
        addMessage("infoBox", "Poprzednia runda została pominięta, <br>ponieważ żaden z graczy nie miał decyzji do podjęcia<br>");
    }

    if (data.yourRoundSkipped == true) {
        addMessage("infoBox", "Twoja kolejka została pominięta, <br>poniważ nie miałeś decyzji do pojęcia<br>");
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
    console.log(data);
    if (checkState(data, where) == 0) {
        window.location.href = data.state;
        return 0;
    } else {
        clearContent("errorInfo");
        clearContent("infoBox");

        updateRound(data.roundData);
        updateCommonCards(data.commonCards);
        updatePlayerCards(data.playerCards);
        updatePlayers(data.players);
        return 1;
    }
}

function clearContent(id) {
    const box = document.getElementById(id);
    if (box == null) {
        return;
    }

    while (box.children.length > 0) {
        box.removeChild(box.firstChild);
    }
}

function addMessage(id, content, style) {
    const box = document.getElementById(id);

    if (box == null) {
        return;
    }

    const p = document.createElement("p");
    p.innerHTML = content;
    p.className = style;
    box.append(p);

    while (box.children.length > 5) {
        box.removeChild(box.firstChild);
    }
}

socket.on("message", (data) => {
    addMessage("infoBox", data.content, data.style);
})