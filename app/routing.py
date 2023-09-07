"""Routing for the app."""

import os
import shlex
import requests
import docker
from flask import render_template, Flask, request
from ratelimit import limits, sleep_and_retry
from app import cache

# Create a Docker client
client = docker.from_env()

# Define resource limits
memory_limit = '110m'
time_limit = 10

def register(app: Flask):
    """ Registers the routes. """

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/run-code', methods=['POST'])
    @sleep_and_retry
    @limits(calls=1, period=1) # Max 1 call per second
    def run_code():
        data = request.get_json()
        code = data.get('code')
        if code is None:
            return {"output": "Code execution failed, API issue. Please contact the website developer to solve this."}

        try:
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            with open("tmp/vache.va", "w", encoding="utf-8") as file:
                # Write the content to the file
                file.write(code)

            # Create a Docker container with resource constraints
            print(os.getcwd() + '/tmp')
            command = f"echo {shlex.quote(code)} > vache.va; vache run vache.va"
            command = f"sh -c {shlex.quote(command)}"
            print(command)
            container = client.containers.run(
                "docker.io/library/vache",
                command=command,
                mem_limit=memory_limit,
                user="user",
                working_dir="/home/user",
                auto_remove=False,
                detach=True,
                network_disabled=True,
            )
            # Wait for the container to finish (timeout in seconds)
            exit_code = container.wait(timeout=time_limit)

            if exit_code['StatusCode'] == 0:
                output = container.logs().decode('utf-8')
                return {"output": output}
            else:
                output = container.logs().decode('utf-8')
                return {"output": output}

        except docker.errors.NotFound:
            return {"output": "Internal error: container image not found. Please report to the website developer."}

        except docker.errors.APIError as exc:
            return {"output": f"Internal error. Please report to the website developer.\nDetails: {str(exc)}"}
        
        except requests.exceptions.ConnectionError as _exc:
            return {"output": "Your program timed out."}
        
        return { "output": "no wow :(" }

    @app.errorhandler(404)
    @cache.cached()
    def not_found_error(_error):
        """ Not found page. """
        return render_template('404.html'), 404