"""CLI Command definitions."""

# Standard Library
import sys
from getpass import getuser
from pathlib import Path

# Third Party
import inquirer
from click import group, option, confirm

# Project
from hyperglass.cli.echo import error, label, cmd_help
from hyperglass.cli.util import build_ui, start_web_server
from hyperglass.cli.static import LABEL, CLI_HELP, E
from hyperglass.cli.formatting import HelpColorsGroup, HelpColorsCommand, random_colors

# Define working directory
WORKING_DIR = Path(__file__).parent

supports_color = "utf" in sys.getfilesystemencoding().lower()


@group(
    cls=HelpColorsGroup,
    help=CLI_HELP,
    context_settings={"color": supports_color},
    help_headers_color=LABEL,
    help_options_custom_colors=random_colors("build-ui", "start", "secret", "setup"),
)
def hg():
    """Initialize Click Command Group."""
    pass


@hg.command(
    "build-ui", help=cmd_help(E.BUTTERFLY, "Create a new UI build", supports_color)
)
def build_frontend():
    """Create a new UI build.

    Raises:
        click.ClickException: Raised on any errors.
    """
    return build_ui()


@hg.command(
    "start",
    help=cmd_help(E.ROCKET, "Start web server", supports_color),
    cls=HelpColorsCommand,
    help_options_custom_colors=random_colors("-b"),
)
@option("-b", "--build", is_flag=True, help="Render theme & build frontend assets")
def start(build):
    """Start web server and optionally build frontend assets."""
    try:
        from hyperglass.api import start, ASGI_PARAMS
    except ImportError as e:
        error("Error importing hyperglass: {e}", e=e)

    if build:
        build_complete = build_ui()

        if build_complete:
            start_web_server(start, ASGI_PARAMS)

    if not build:
        start_web_server(start, ASGI_PARAMS)


@hg.command(
    "secret",
    help=cmd_help(E.LOCK, "Generate agent secret", supports_color),
    cls=HelpColorsCommand,
    help_options_custom_colors=random_colors("-l"),
)
@option(
    "-l", "--length", "length", default=32, help="Number of characters [default: 32]"
)
def generate_secret(length):
    """Generate secret for hyperglass-agent.

    Arguments:
        length {int} -- Length of secret
    """
    import secrets

    gen_secret = secrets.token_urlsafe(length)
    label("Secret: {s}", s=gen_secret)


@hg.command(
    "setup",
    help=cmd_help(E.TOOLBOX, "Run the setup wizard", supports_color),
    cls=HelpColorsCommand,
    help_options_custom_colors=random_colors("-d"),
)
@option(
    "-d",
    "--use-defaults",
    "unattended",
    default=False,
    is_flag=True,
    help="Use hyperglass defaults (requires no input)",
)
def setup(unattended):
    """Define application directory, move example files, generate systemd service."""
    from hyperglass.cli.util import create_dir, move_files, make_systemd, write_to_file

    user_path = Path.home() / "hyperglass"
    root_path = Path("/etc/hyperglass/")

    install_paths = [
        inquirer.List(
            "install_path",
            message="Choose a directory for hyperglass",
            choices=[user_path, root_path],
        )
    ]
    if not unattended:
        answer = inquirer.prompt(install_paths)
        install_path = answer["install_path"]
    elif unattended:
        install_path = user_path

    ui_dir = install_path / "static" / "ui"
    custom_dir = install_path / "static" / "custom"

    create_dir(install_path)
    create_dir(ui_dir, parents=True)
    create_dir(custom_dir, parents=True)

    example_dir = WORKING_DIR.parent / "examples"
    files = example_dir.iterdir()

    do_move = True
    if not unattended and not confirm(
        "Do you want to install example configuration files? (This is non-destructive)"
    ):
        do_move = False

    if do_move:
        move_files(example_dir, install_path, files)

    if install_path == user_path:
        user = getuser()
    else:
        user = "root"

    do_systemd = True
    if not unattended and not confirm(
        "Do you want to generate a systemd service file?"
    ):
        do_systemd = False

    if do_systemd:
        systemd_file = install_path / "hyperglass.service"
        systemd = make_systemd(user)
        write_to_file(systemd_file, systemd)
