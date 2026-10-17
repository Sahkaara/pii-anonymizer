# src/pii_anonymizer/cli.py
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .core import anonymize_text

# Create the Typer application. The help text is shown when running
# `pii-anonymizer --help`.
app = typer.Typer(
    help="Anonymize personally identifiable information (PII) in text files."
)


@app.command()
def anonymize(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input file to anonymize.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    output_file: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Path to the output file. If omitted, the result is printed to stdout.",
        ),
    ] = None,
    language: Annotated[
        str,
        typer.Option(
            "--lang",
            "-l",
            help="Language of the input text (e.g. 'en').",
        ),
    ] = "en",
) -> None:
    """
    Read a text file, anonymize any PII found in it, and write the result.

    If no output file is provided, the anonymized text is printed to the
    standard output. This makes the tool easy to combine with other
    command-line utilities via pipes.
    """
    try:
        # Read the entire input file as UTF-8. Using `errors="replace"`
        # would silently corrupt data, so we let a UnicodeDecodeError surface.
        text = input_file.read_text(encoding="utf-8")

        typer.echo(f"Analyzing '{input_file}'...", err=True)

        # Run the anonymization pipeline (detection + transformation).
        anonymized = anonymize_text(text, language=language)

        if output_file is not None:
            # Write the anonymized text to the requested output path.
            output_file.write_text(anonymized, encoding="utf-8")
            typer.echo(f"Anonymized file written to '{output_file}'.", err=True)
        else:
            # No output file specified: print to stdout so the user can
            # redirect the result or pipe it into another tool.
            typer.echo(anonymized)

    except UnicodeDecodeError as exc:
        typer.echo(
            f"Error: the file '{input_file}' is not valid UTF-8. "
            f"Please convert it to UTF-8 and try again. "
            f"Details: {exc}",
            err=True,
        )
        raise typer.Exit(code=1)

    except ValueError as exc:
        # Raised by `anonymize_text` for unsupported languages.
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)

    except Exception as exc:  # noqa: BLE001 - top-level guard for the CLI
        # Catch-all so the user sees a clean message instead of a traceback.
        typer.echo(f"Unexpected error: {exc}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()