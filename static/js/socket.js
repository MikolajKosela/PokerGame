const socket = io();

socket.on("connect", () => {
    socket.emit("handshake", {
        token : localStorage.getItem("token"),
    });
});

socket.on("handshakeAnswer", (data) => {
    const ok = data.ok;

    console.log(ok);

    if (ok == false) {
        localStorage.clear("token");
        localStorage.clear("nickname");
        localStorage.clear("admin");
    } else {
        localStorage.setItem("admin", data.admin);
    }
    socket.emit("checkStateRequest");
})
