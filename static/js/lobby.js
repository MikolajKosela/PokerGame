const welcome=document.getElementById("welcome");
let nickname=localStorage.getItem("nickname");
welcome.innerHTML="Witaj "+nickname;

socket.on("checkState", (data) => {
    const target = data.state;
    if(window.location.pathname != target) {
        window.location.href = target;
    } else {
        socket.emit("amIAdmin");
        socket.emit("playersListRequest");
    }
});

socket.on("playersList", (data) => {
    const list=document.getElementById("players");
    list.innerHTML=""
    var cnt=0;

    data.forEach(function(player)
    {
        const li=document.createElement("li");
        if(cnt==0)
            li.textContent=player.nickname+" - "+player.credits+" (admin)";
        else
            li.textContent=player.nickname+" - "+player.credits;
        list.appendChild(li);
        cnt+=1;
    });

    const p_num=document.getElementById("playersNum");
    p_num.innerHTML="Graczy w lobby: "+cnt;
})

socket.on("areYouAdmin", (data) => {
    if (data.yes == true) {
        const start=document.createElement("button");
        
        start.textContent="Zacznij";
        start.id="start";
        start.type="submit";
        start.className="btn";

        start.onclick=function() {
            socket.emit("startGame");
        };

        const form=document.getElementById("startButton");
        form.appendChild(start);
    }
})

socket.on("started", () => {
    socket.emit("checkStateRequest");
})