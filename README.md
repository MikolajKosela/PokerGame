# PokerGame

A simple poker game for playing with friends over the Internet. Host your own server, invite your friends, and take your seats at the poker table.

## Installation

You need Python 3, a virtual environment (`venv`), and the required Python dependencies.

On Debian-based systems:

```bash
sudo apt install python3 python3-pip python3-venv
```

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/MikolajKosela/PokerGame
cd PokerGame

python3 -m venv venv
source venv/bin/activate

pip install flask flask-socketio
python3 app.py
```

The server will start on port `5000`.

## Example

Once your server is running on port `5000`, you can expose it to the Internet using a Cloudflare Tunnel.

On Debian-based systems:

```bash
sudo apt install cloudflared
cloudflared tunnel --url http://localhost:5000
```

You should see something similar to:

```text
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
|  https://???-???-???-???.trycloudflare.com                                                 |
```

Simply copy the generated URL and send it to your friends.

## Screenshots

*Coming soon.*

## Language Support

The interface is currently available only in **Polish**.

English localization is planned for a future release.

## Roadmap

* [ ] English translation
* [ ] Complete type annotations
* [ ] More game rule customization options
* [ ] Better handling of player disconnections
* [ ] User interface improvements
* [ ] Additional features
