const socket = io();

socket.on("connect", () => {
    console.log("Łącze...");
    socket.emit("handshake", {
        token : localStorage.getItem("token"),
    });
});

socket.on("handshakeAnswer", (data) => {
    const ok = data.ok;
    console.log("Połączono. Czy znaleziono token?:");

    console.log(ok);

    if (ok == false) {
        localStorage.clear("token");
        localStorage.clear("nickname");
        localStorage.clear("admin");
    } else {
        localStorage.setItem("admin", data.admin);
    }
    socket.emit("gameDataRequest");
})
