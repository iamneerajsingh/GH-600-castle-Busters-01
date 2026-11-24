"""Local browser game. Run with python -m castle_busters.game."""

import argparse
import json
import math
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from itertools import pairwise
from pathlib import Path

from .castle import level_one
from .physics import Shot, trajectory
from .scoring import final_score, score_hit

MAX_SHOTS = 8
MAX_PULL = 100


def func_launch(var_pull_x: float, var_pull_y: float) -> Shot:
    """Convert a backward/downward screen-space pull into a launch."""
    if not all(math.isfinite(var_value) for var_value in (var_pull_x, var_pull_y)):
        raise ValueError("Pull coordinates must be finite numbers.")
    if var_pull_x >= 0 or var_pull_y <= 0:
        raise ValueError("Pull the boulder left and down from the sling.")
    var_length = math.hypot(var_pull_x, var_pull_y)
    if var_length < 8:
        raise ValueError("Pull farther back before releasing.")
    return Shot(
        math.degrees(math.atan2(var_pull_y, -var_pull_x)),
        min(var_length, MAX_PULL) * 0.5,
    )


def func_intersection(
    var_start: tuple[float, float],
    var_end: tuple[float, float],
    var_left: float,
    var_right: float,
    var_top: float,
) -> float | None:
    """Return segment entry time into a target, including the boulder radius."""
    var_enter, var_exit = 0.0, 1.0
    for var_axis, var_low, var_high in (
        (0, var_left - 1.4, var_right + 1.4),
        (1, -1.4, var_top + 1.4),
    ):
        var_delta = var_end[var_axis] - var_start[var_axis]
        if var_delta == 0:
            if not var_low <= var_start[var_axis] <= var_high:
                return None
            continue
        var_a = (var_low - var_start[var_axis]) / var_delta
        var_b = (var_high - var_start[var_axis]) / var_delta
        var_enter = max(var_enter, min(var_a, var_b))
        var_exit = min(var_exit, max(var_a, var_b))
        if var_enter > var_exit:
            return None
    return var_enter


class Game:
    def __init__(self) -> None:
        self.func_reset()

    def func_reset(self) -> dict:
        self.var_castle = level_one()
        self.var_points = 0
        self.var_shots = 0
        return self.func_state()

    def func_state(self) -> dict:
        var_names = ("Sir Clanks", "Moss the Monster", "Captain Grumble")
        var_heights = (12, 16, 14)
        return {
            "targets": [
                {
                    "kind": var_block.kind,
                    "x": var_block.x,
                    "width": var_block.width,
                    "standing": var_block.standing,
                    "name": var_name,
                    "height": var_height,
                    "character": "monster" if var_block.kind == "stone" else "guard",
                }
                for var_block, var_name, var_height in zip(
                    self.var_castle.blocks, var_names, var_heights
                )
            ],
            "shots": self.var_shots,
            "remaining": MAX_SHOTS - self.var_shots,
            "score": final_score(self.var_points, max(1, self.var_shots)),
            "won": self.var_castle.destroyed,
            "over": self.var_castle.destroyed or self.var_shots >= MAX_SHOTS,
        }

    def func_fire(self, var_pull_x: float, var_pull_y: float) -> dict:
        if self.func_state()["over"]:
            raise ValueError("This round is finished. Start a new round.")
        var_shot = func_launch(var_pull_x, var_pull_y)
        var_path = trajectory(var_shot, steps=300)
        var_targets = self.func_state()["targets"]
        var_hit = None
        for var_index, (var_start, var_end) in enumerate(pairwise(var_path)):
            var_impacts = []
            for var_target in var_targets:
                if not var_target["standing"]:
                    continue
                var_entry = func_intersection(
                    var_start,
                    var_end,
                    var_target["x"],
                    var_target["x"] + var_target["width"],
                    var_target["height"],
                )
                if var_entry is not None:
                    var_impacts.append((var_entry, var_target))
            if var_impacts:
                var_entry, var_hit = min(var_impacts, key=lambda var_item: var_item[0])
                var_impact = tuple(
                    var_a + (var_b - var_a) * var_entry
                    for var_a, var_b in zip(var_start, var_end)
                )
                var_path = var_path[: var_index + 1] + [var_impact]
                self.var_points += score_hit(self.var_castle.hit(var_hit["x"]))
                break
        self.var_shots += 1
        return {
            **self.func_state(),
            "path": var_path,
            "angle": var_shot.angle_deg,
            "power": var_shot.power,
            "hit": var_hit["name"] if var_hit else None,
        }


def func_handler(var_game: Game) -> type[BaseHTTPRequestHandler]:
    var_lock = threading.Lock()
    var_page = Path(__file__).with_name("index.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def func_send(self, var_status: int, var_body: bytes, var_type: str) -> None:
            self.send_response(var_status)
            self.send_header("Content-Type", var_type)
            self.send_header("Content-Length", str(len(var_body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(var_body)

        def do_GET(self) -> None:
            if self.path == "/":
                self.func_send(200, var_page, "text/html; charset=utf-8")
            elif self.path == "/api/state":
                with var_lock:
                    var_state = var_game.func_state()
                self.func_send(200, json.dumps(var_state).encode(), "application/json")
            else:
                self.send_error(404)

        def do_POST(self) -> None:
            if self.path not in ("/api/shot", "/api/reset"):
                self.send_error(404)
                return
            # Reject cross-origin writes to this local game.
            var_origin = self.headers.get("Origin")
            if var_origin and var_origin != f"http://{self.headers.get('Host')}":
                self.send_error(403, "Cross-origin requests are not allowed.")
                return
            try:
                var_length = int(self.headers.get("Content-Length", "0"))
                if not 0 <= var_length <= 1024:
                    raise ValueError("Request body is too large.")
                var_data = json.loads(self.rfile.read(var_length) or b"{}")
                if not isinstance(var_data, dict):
                    raise TypeError("Request must be a JSON object.")
                with var_lock:
                    if self.path == "/api/reset":
                        var_result = var_game.func_reset()
                    else:
                        var_x, var_y = var_data.get("pull_x"), var_data.get("pull_y")
                        if any(
                            isinstance(var_value, bool)
                            or not isinstance(var_value, (int, float))
                            for var_value in (var_x, var_y)
                        ):
                            raise TypeError("Pull coordinates must be numbers.")
                        var_result = var_game.func_fire(var_x, var_y)
            except (ValueError, TypeError) as var_error:
                self.log_error("Invalid game request: %s", var_error)
                self.func_send(
                    400, json.dumps({"error": str(var_error)}).encode(), "application/json"
                )
                return
            self.func_send(200, json.dumps(var_result).encode(), "application/json")

    return Handler


def play() -> None:
    var_parser = argparse.ArgumentParser(description=__doc__)
    var_parser.add_argument("--port", type=int, default=8000)
    var_parser.add_argument("--no-browser", action="store_true")
    var_args = var_parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", var_args.port), func_handler(Game())) as var_server:
        var_url = f"http://127.0.0.1:{var_server.server_port}"
        print(f"Castle Busters: {var_url}\nPress Ctrl+C to stop.", flush=True)
        if not var_args.no_browser:
            webbrowser.open(var_url)
        try:
            var_server.serve_forever()
        except KeyboardInterrupt:
            print("\nCastle Busters stopped.")


if __name__ == "__main__":
    play()
