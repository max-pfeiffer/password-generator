"""Test Utilities"""
# pylint: disable=duplicate-code

from docker.models.containers import Container


def get_uvicorn_processes(container: Container) -> list[str]:
    """Get a list of Uvicorn processes

    :param container: Container
    :return: list[str]
        List of processes
    """
    top = container.top()
    process_commands: list[str] = [p[7] for p in top["Processes"]]
    uvicorn_processes: list[str] = [
        p for p in process_commands if "/usr/application/.venv/bin/uvicorn" in p
    ]
    return uvicorn_processes


def get_uvicorn_config(container: Container) -> dict[str, any]:
    """Get the Uvicorn configuration from a container

    :param container: Container
    :return: dict[str, any]
        Dictionary containing the Uvicorn config
    """
    uvicorn_config: dict[str, any] = {}
    uvicorn_processes = get_uvicorn_processes(container)
    first_process = uvicorn_processes[0]

    # pylint: disable=unused-variable
    first_part: str
    partition: str
    last_part: str
    first_part, partition, last_part = first_process.partition(
        "/usr/application/.venv/bin/uvicorn"
    )

    uvicorn_arguments: list[str] = last_part.strip().split()
    app: str = uvicorn_arguments.pop()
    uvicorn_config["app"] = app

    for index, element in enumerate(uvicorn_arguments):
        option: str
        value: any
        if element.startswith("--"):
            option = element.lstrip("--")
            try:
                next_element = uvicorn_arguments[index + 1]
                if next_element.startswith("--"):
                    # It is an option without value
                    value = True
                else:
                    # add the value for the current option
                    value = next_element
            except IndexError:
                # It is an option without value at the end of options list
                value = True

        uvicorn_config[option] = value
    return uvicorn_config
