import subprocess
import webbrowser


def partition_count(disk_number: int = 0) -> int:
    cmd = [
        "powershell", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass",
        "-Command",
        f"(Get-Partition -DiskNumber {disk_number} | Measure-Object).Count"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        raise RuntimeError(f"PowerShell error ({res.returncode}): {res.stderr.strip()}")

    out = (res.stdout or "").strip()
    if not out:
        raise RuntimeError("No result on STDOUT (empty result in PowerShell).")

    try:
        return f'Number of partition on disk C: {int(out)}'
    except ValueError:
        raise ValueError(f"Cannot into int. STDOUT='{out}', STDERR='{res.stderr.strip()}'")


def yt_usability():
    user = webbrowser.open("https://www.youtube.com/watch?v=LXb3EKWsInQ")
    return user


def yt_batt():
    bean = webbrowser.open("https://www.youtube.com/watch?v=agBuBFbGZAQ")
    return bean


