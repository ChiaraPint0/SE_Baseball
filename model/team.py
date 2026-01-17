from dataclasses import dataclass

@dataclass(frozen=True)
class Team:
    id: int
    year: int
    team_code: str

    def __str__(self):
        return self.team_code

    def __repr__(self):
        return self.team_code


