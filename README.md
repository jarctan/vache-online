# Installation

You will need:

- `git`
- `python` version 3.10
- `pip`
- `node`

And a Linux-like shell environment (either with Linux or on Windows via WSL), needed to run the `Makefile` correctly.

Clone the repository.

Create a new virtual environment and switch to it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the `pip` requirements:

```bash
pip install -r requirements.txt
```

If you ever need to change the requirements, do:

```bash
pipreqs
```

(you can install `pipreqs` with `pip install pipreqs`)

Put the secrets inside:
`app/.env`
By default, and for debug mode, put this:

```
SECRET_KEY = "SECRET_KEY"
```

# Recompile the Docker image

This will recompile the Vache docker image on your system.

```bash
make setup
```

# Run the server in development mode

This will run the server on your `localhost`, with debug mode.

```bash
make run
```
