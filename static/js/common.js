function updateRound(data) {
    const curNick = document.getElementById("curNick");
    if (curNick != null) {
        curNick.innerHTML = "Trwa runda gracza: " + data.curNick;
    }

    const playersNum = document.getElementById("playersNum");
    if (playersNum != null) {
        if (data.playersNum == 0) {
            playersNum.innerHTML = "Dołącz do lobby jako pierwszy";
        } else {
            playersNum.innerHTML = "W lobby czeka: " + data.playersNum + " graczy";
        }
    }

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
        console.log(player.id, data.curID);
        if (player.id != data.curID) {
            const li = document.createElement("li");
            console.log(player);
            li.textContent =
                player.nickname + " - " + player.credits;
            playersList.appendChild(li);
        }
    }
}

export function processGameData(data) {
    updateRound(data.roundData);
    updateCommonCards(data.commonCards);
    updatePlayerCards(data.playerCards);
    updatePlayers(data.players);
}