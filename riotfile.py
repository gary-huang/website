from riot import latest, Venv

venv = Venv(
    pys="3.8",
    venvs=[
        Venv(
            pkgs={
                "black": "==20.8b1",
            },
            venvs=[
                Venv(
                    name="black",
                    command="black {cmdargs}",
                ),
                Venv(
                    name="fmt",
                    command="black --exclude migrations .",
                ),
            ],
        ),
        Venv(
            name="flake8",
            command="flake8 {cmdargs}",
            pkgs={
                "flake8": latest,
                "flake8-builtins": latest,
                "flake8-logging-format": latest,
            },
        ),
        Venv(
            name="mypy",
            command="mypy {cmdargs}",
            pkgs={
                "mypy": latest,
            },
        ),
    ],
)
