import subprocess

def test_cli_help():
    result = subprocess.run(["poetry", "run", "python", "-m", "arinja.cli", "--help"], capture_output=True, text=True)
    assert "Arinja" in result.stdout
