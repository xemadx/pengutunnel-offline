"""Trusted parent-side PTY fixture for the root bootstrap's actual file layout.

Target execution remains chrooted, network isolated, seccomp filtered and
capability-free. systemctl/dpkg are local fixtures; no host service is used.
"""
import errno
import fcntl
import hashlib
import os
from pathlib import Path
import pty
import select
import signal
import subprocess
import termios
import time


def check_bootstrap_cli(base, root):
    scratch = base / "scratch"
    commands = scratch / "cli-mocks"
    commands.mkdir()
    for name, content in {
        "dpkg": "#!/bin/bash\nexit 0\n",
        "systemctl": "#!/bin/bash\ncase \"$1\" in is-enabled|is-active) exit 1;; esac\nexit 0\n",
        "apt-get": "#!/bin/bash\necho 'Unexpected package install' >&2\nexit 99\n",
        "curl": "#!/bin/bash\necho 'Unexpected network fetch' >&2\nexit 99\n",
    }.items():
        path = commands / name
        path.write_text(content)
        path.chmod(0o755)
    script = scratch / "bootstrap-cli.sh"
    script.write_text('''#!/bin/bash
set -euo pipefail
export PATH=/scratch/cli-mocks:/usr/sbin:/usr/bin:/sbin:/bin
if [[ "${1:-}" == reopen ]]; then exec /usr/local/bin/pengu; fi
if [[ "${1:-}" == update ]]; then exec /usr/local/bin/pengu update; fi
if [[ "${1:-}" == tagged ]]; then exec /usr/local/bin/pengu update v99.0.0-r1; fi
cat /package/install.sh | bash -s -- --source-dir /package
''')
    script.chmod(0o755)

    def session(mode=None):
        master, slave = pty.openpty()

        def terminal():
            os.setsid()
            fcntl.ioctl(slave, termios.TIOCSCTTY, 0)

        command = ["nsenter", "--net=/run/netns/qa-a", "chroot", str(root),
                   "/usr/bin/setpriv", "--reuid=0", "--regid=0", "--clear-groups",
                   "--bounding-set=-all", "--inh-caps=-all", "--ambient-caps=-all", "--no-new-privs",
                   "/usr/bin/python3", "-I", "/input/guard.py", "/bin/bash", "/scratch/bootstrap-cli.sh"]
        if mode:
            command.append(mode)
        process = subprocess.Popen(command, stdin=slave, stdout=slave, stderr=slave,
                                   close_fds=True, preexec_fn=terminal)
        os.close(slave)
        output = bytearray()
        os.write(master, b"0\n")
        deadline = time.monotonic() + 25
        try:
            while time.monotonic() < deadline:
                if select.select([master], [], [], .2)[0]:
                    try:
                        data = os.read(master, 32768)
                    except OSError as error:
                        if error.errno == errno.EIO:
                            break
                        raise
                    if not data:
                        break
                    output.extend(data)
                    if len(output) > 200000:
                        raise RuntimeError("PTY output limit")
                elif process.poll() is not None:
                    break
            if process.poll() is None:
                process.wait(timeout=2)
            if process.returncode != 0:
                raise AssertionError(output.decode("utf-8", "replace"))
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            os.close(master)
        return output.decode("utf-8", "replace")

    initial = session()
    if "Installed v" not in initial or "Configure a new tunnel" not in initial:
        raise AssertionError("Bootstrap did not open the interactive menu")
    if not (scratch / "localbin/pengu").is_file():
        raise AssertionError("Persistent CLI missing")
    reopened = session("reopen")
    if "Configure a new tunnel" not in reopened:
        raise AssertionError("Persistent CLI did not reopen the menu")
    installed = scratch / "root/pengutunnel/pengutunnel"
    if not installed.is_file():
        raise AssertionError("Core was not installed inside the fixture")
    # Check actual installed update command: latest release by default, exact
    # release asset for an explicit tag. The mock never accesses the network.
    (commands / "curl").write_text('''#!/bin/bash
set -euo pipefail
url=""; output=""
while (($#)); do
  case "$1" in
    -o) output="$2"; shift 2;;
    https://*) url="$1"; shift;;
    *) shift;;
  esac
done
case "$url" in
  https://github.com/xemadx/pengutunnel-offline/releases/latest/download/install.sh) marker=LATEST_RELEASE;;
  https://github.com/xemadx/pengutunnel-offline/releases/download/v99.0.0-r1/install.sh) marker=EXACT_RELEASE;;
  *) echo "Unexpected update URL" >&2; exit 99;;
esac
printf 'PACKAGE_VERSION="fixture"\\necho %s\\n' "$marker" > "$output"
''')
    if "LATEST_RELEASE" not in session("update") or "EXACT_RELEASE" not in session("tagged"):
        raise AssertionError("CLI did not select the correct published release")
    return dict(initial_menu=True, reopened_menu=True,
                update_latest_release=True, update_exact_release=True,
                installed_core_sha256=hashlib.sha256(installed.read_bytes()).hexdigest(),
                real_host_services=False, network_fetches=False)
