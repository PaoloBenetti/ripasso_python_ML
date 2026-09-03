import typer

app = typer.Typer()

@app.callback()
def callback() -> None:
    """Gridpath CLI - simulazione di agenti su griglia."""
    pass

@app.command()
def simulate(
    n: int = 5,
    agents: int = 3,
    steps: int = 10,
) -> None:
    """Simula il movimento di N agenti su una griglia per un certo numero di step."""
    from core.gridpath import Grid, Agent
    import random

    g = Grid(n)
    lista_agenti = [
        Agent(g, f"agente_{i}", random.randint(0, n-1), random.randint(0, n-1))
        for i in range(agents)
    ]

    for step in range(steps):
        for a in lista_agenti:
            a.move_casual()

    g.recap_agenti()


if __name__ == "__main__":
    app()
