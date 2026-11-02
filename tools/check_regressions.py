#!/usr/bin/env python3
"""Reproduce fixed installer bugs with temporary files and a mock systemctl.

Run inside tests/run-isolated.sh. No root entrypoint or real service is run.
"""
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parent.parent


def main():
    source = (ROOT / "install-offline.sh").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="pengu-regressions-") as directory:
        work = Path(directory)
        library = work / "library.sh"
        library.write_text(source.rsplit("\nneed_root\n", 1)[0], encoding="utf-8")
        prefix = '''source "$1"
INSTALL_DIR="$2/install"; SERVICE_DIR="$2/services"; BIN_PATH=/bin/true
mkdir -p "$INSTALL_DIR" "$SERVICE_DIR"
banner(){ :; }; pause(){ :; }; core_at_least(){ return 0; }; detect_cpu_mem(){ echo '2 1024'; }; sleep(){ :; }
systemctl(){
 printf '%s\\n' "$*" >> "$2_PLACEHOLDER/calls"
 local unit="${@: -1}"
 case "$*" in 'is-active x-ui'|'is-active fail2ban') return 1;; esac
 case "$1" in
  is-active) [[ -f "$2_PLACEHOLDER/active-$unit" ]];;
  start) [[ "${FAIL_START:-0}" != 1 ]] || return 1; touch "$2_PLACEHOLDER/active-$unit";;
  restart) touch "$2_PLACEHOLDER/active-$unit";;
 esac
}
'''.replace("$2_PLACEHOLDER", str(work))
        passed = 0

        def check(name, code, data="", expected=0):
            nonlocal passed
            result = subprocess.run(["bash", "-c", prefix + code, "test", str(library), str(work)],
                                    input=data, text=True, capture_output=True, timeout=6)
            if result.returncode != expected:
                raise AssertionError((name, result.returncode, result.stdout, result.stderr))
            passed += 1
            print("PASS:", name)
            return result

        check("port validation", 'for p in 0 65536 -1 abc "1;id" 00080; do ! valid_port "$p" || exit 1; done; valid_port 65535')
        check("retry invalid health port", 'wport health 1234; test "$WIZ_VAL" = 1234', "70000\n1234\n")
        quoted = check("TOML string escaping", 'printf "psk = %s\\n" "$(toml_string \'a"b\\c\')"')
        assert tomllib.loads(quoted.stdout)["psk"] == 'a"b\\c'
        check("forward grammar", 'valid_forward_spec "24555=10.204.0.11:24556" && valid_forward_spec "200-300 proxy_protocol=true" && ! valid_forward_spec \'25"oops\' && ! valid_forward_spec "0=80" && ! valid_forward_spec "1-2-3"')
        check("explicit custom TUN destination", 'test "$(forward_to_peer 24555=24556 10.204.0.11)" = 24555=10.204.0.11:24556')
        for role in ("watcher", "enforcer"):
            conf = work / (role + ".toml")
            conf.write_text('[transport]\ntype="tcpfwd"\nmode="client"\nremote="10.203.0.1:24443"\n')
            override = '''systemctl(){ case "$*" in 'is-active x-ui') return XUI;; 'is-active fail2ban') return 1;; esac; }
command(){ if [[ "$*" == '-v iptables' ]]; then return 1; else builtin command "$@"; fi; }
'''.replace("XUI", "0" if role == "watcher" else "1")
            result = check("ban-sync warning stays outside TOML: " + role,
                           override + f'_ipl_enable demo "{conf}"', "\n\n\n")
            assert tomllib.loads(conf.read_text())["xui_iplimit"]["mode"] == role
            assert "[!]" not in conf.read_text() and "[!]" in result.stderr

        def inputs(health, psk="dummy", replace=False, eof=False):
            values = ["1", "1", "24443", "fast", "1", "2", "1", "0", "aes-256-gcm", health, psk, "n", "24555=24556"]
            if not eof:
                values.append("")
                if replace:
                    values.append("y")
            return "\n".join(values) + "\n"

        check("L4 initial creation", "configure_l4 1 tcpfwd", inputs("21301"))
        (work / "calls").write_text("")
        check("replacing active tunnel restarts it", "configure_l4 1 tcpfwd", inputs("21301", "changed", True))
        calls = (work / "calls").read_text()
        assert "restart pengutunnel-iran21301" in calls
        assert tomllib.loads((work / "install/iran21301.toml").read_text())["security"]["psk"] == "changed"
        check("quoted PSK remains valid TOML", "configure_l4 1 tcpfwd", inputs("21302", 'a"b'))
        assert tomllib.loads((work / "install/iran21302.toml").read_text())["security"]["psk"] == 'a"b'
        result = check("start failure propagates", "FAIL_START=1; configure_l4 1 tcpfwd", inputs("21303"), expected=1)
        assert "[ok] tunnel" not in result.stdout
        check("EOF does not commit a partial tunnel", "configure_l4 1 tcpfwd", inputs("21304", eof=True), expected=1)
        assert not (work / "install/iran21304.toml").exists()
        check("zero cannot select last tunnel", 'list_ids(){ printf "first\\nsecond\\n"; }; conf_of(){ echo "$2/watcher.toml"; }; xui_iplimit_menu', "0\n", expected=1)
        check("missing package manager fails closed", "command(){ return 1; }; install_prereqs", expected=1)
        check("duplicate health port rejected", 'printf "[tun]\\nhealth_port = 21400\\n" > "$INSTALL_DIR/other.toml"; check_tunnel_slot new 21400', expected=1)
        result = check("HTTP failures are not fast mirrors", 'curl(){ if [[ "$*" == *bad.example* ]]; then printf 0.001; return 22; else printf 0.100; fi; }; _bench_mirrors "http://bad.example http://good.example" noble')
        assert "good.example" in result.stdout and "bad.example" not in result.stdout
        result = check("DNS benchmark requires a DNS answer", '''command(){ if [[ "$*" == '-v dig' ]]; then return 0; else builtin command "$@"; fi; }
timeout(){ shift; "$@"; }
dig(){ if [[ "$*" == *'@1.1.1.1'* ]]; then echo REFUSED; else echo 198.18.0.1; fi; }
_bench_dns '1.1.1.1,1.0.0.1:bad 9.9.9.9,149.112.112.112:good'
''')
        assert "good" in result.stdout and "bad" not in result.stdout
        check("invalid DNS address rejected", "_set_dns invalid ''", expected=1)
        check("DNS restore without backup does not invent a configuration", "_dns_restore", expected=1)
        check("read-only DNS backup failure propagates", "_set_dns 1.1.1.1 1.0.0.1", expected=1)
        result = check("apt restore failure propagates", 'APT_BAK="$2/sources.bak"; APT_SRC="$2/sources"; echo original > "$APT_BAK"; cp(){ return 1; }; _mirror_restore', expected=1)
        assert "[ok]" not in result.stdout
        print(f"PASS: {passed} regression checks")


if __name__ == "__main__":
    main()
