from dataclasses import dataclass

@dataclass
class Result:
    ok: bool
    error: str | None = None
    info: str | None = None