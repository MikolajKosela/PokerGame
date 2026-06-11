socket.on("checkState", (data) => {
  const target = data.state;
    if (window.location.pathname != target) {
      window.location.href = target;
    }
  });

socket.on("joined", (data) => {
  localStorage.setItem("token", data.token);
  window.location.href = "/lobby";
});

function join() {
  let nickname = document.getElementById("nickname").value;
  localStorage.setItem("nickname", nickname);

  socket.emit("join", {
    nickname : nickname
  });
}