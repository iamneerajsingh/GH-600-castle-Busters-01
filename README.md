
# Castle Busters

Now with agents


A tiny catapult-and-castle game in Python, used to demonstrate the GH-600 (Developing in Agentic AI Systems) skills.

## Play
```
python -m castle_busters.game
```
This starts a local Python server and opens http://127.0.0.1:8000 in your browser.
No extra runtime packages are needed. Keep the terminal open; press Ctrl+C to stop.

Grab the boulder in the catapult sling, pull **left and down**, and release to
launch. Longer pulls add power; the dotted arc previews your aim. Defeat the
cartoon guards Sir Clanks and Captain Grumble, and Moss the Monster, to topple
their castle blocks. There are eight boulders per round. Wood, stone, and tower
targets award 10, 25, and 50 points; every shot after the first costs 5 points.
Use **New round** to restart.

Mouse and touch controls are supported. For keyboard play, focus the battlefield
with Tab, adjust the pull with the arrow keys, and press Space to fire.
Collisions along the flight path now count, rather than only the landing point.
The existing standalone physics and scoring helpers remain unchanged.

If the browser does not open automatically, visit the printed URL. To choose
another port or avoid opening a browser:
```
python -m castle_busters.game --port 8001 --no-browser
```

## Test
```
pip install -r requirements-dev.txt
python -m pytest -q
ruff check .
```
