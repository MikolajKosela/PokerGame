const welcome=document.getElementById("welcome");
let nickname=localStorage.getItem("nickname");
welcome.innerHTML="Witaj "+nickname;

socket.on("checkState", (data) => {
    const target = data.state;
    if(window.location.pathname != target) {
        window.location.href = target;
    } else {
        if (localStorage.getItem("admin") == "true") {
            document.getElementById("start").className = "btn";
        }
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

function start() {
    if (localStorage.getItem("admin") == "true") {
        socket.emit("startGame");
    }
}

socket.on("started", () => {
    socket.emit("checkStateRequest");
})