function updateRound(data) {
    const pot = document.getElementById("pot");
    pot.innerHTML = "Całkowita pula wynosi: " + data.pot;
    const credits = document.getElementById("credits");
    credits.innerHTML =
        "Twoje żetony " + data.curCredit + " Do wyrównania: " + data.bet;

    const callBut = document.getElementById("call");
    callBut.innerHTML = "Sprawdź ( " + data.bet + " )";
}

function updateCommonCards(data) {
    const commonCardsList = document.getElementById("commonCards");
    commonCardsList.innerHTML='';

    for(const card of data.cards) {
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
}

function updatePlayerCards(data) {
    const playerCardsList = document.getElementById("yourCards");
    playerCardsList.innerHTML='';

    for(const card of data.cards) {
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
}

function updatePlayers(data) {
    const playersList = document.getElementById("players");
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