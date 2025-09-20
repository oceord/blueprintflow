import nox  # pyright: ignore[reportMissingImports]


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", "src", "tests")


@nox.session
def typing(session):
    session.install("mypy", "types-PyYAML", "types-requests")
    session.run("mypy", "src")


@nox.session(python=["3.12", "3.13"])
def tests(session):
    session.install(".")
    session.install("pytest")
    session.run("pytest", "tests")
