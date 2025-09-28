import os
import subprocess

class Runner:
    def __init__(self, script_path: str):
        # absolutna ścieżka = mniej niespodzianek
        self.script_path = os.path.abspath(script_path)

    def prepare_and_run(self) -> subprocess.CompletedProcess:
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"Nie znaleziono: {self.script_path}")

        # uruchom .bat w jego katalogu, tym razem z widoczną konsolą
        return subprocess.run(
            ["cmd", "/c", self.script_path],
            cwd=os.path.dirname(self.script_path),
            check=False
        )

#bat_path = r"scripts\netspeed_checker.bat"  # ścieżka do Twojego .bat
#runner = Runner(bat_path)
#result = runner.prepare_and_run()
