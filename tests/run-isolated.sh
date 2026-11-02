#!/usr/bin/env bash
# Requires Linux root, cgroup v2, namespaces, iproute2 and libseccomp.so.2.
# Does not install packages, modify host services or give test processes internet.
set -euo pipefail
if [[ "${1:-}" != inner ]]; then
  [[ $EUID -eq 0 ]] || { echo 'Run this test with sudo on Linux/WSL.' >&2; exit 1; }
  HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
  TARGET="$(cd -- "$HERE/.." && pwd)"
  OUT="$(realpath -m -- "${1:-/var/tmp/pengu-results-$(date +%Y%m%d-%H%M%S)-$$}")"
  [[ "$OUT" != "$TARGET" && "$OUT" != "$TARGET/"* ]] || { echo 'Results must be outside the read-only target.' >&2; exit 1; }
  mkdir -p "$OUT"
  BASE="$(mktemp -d /var/tmp/pengu-sandbox.XXXXXXXX)"
  CG="/sys/fs/cgroup/pengu-test-$$"
  mkdir -p "$BASE/root" "$BASE/scratch" "$CG"
  echo 1073741824 > "$CG/memory.max"
  echo 0 > "$CG/memory.swap.max"
  echo 192 > "$CG/pids.max"
  echo '200000 100000' > "$CG/cpu.max"
  export HERE TARGET OUT BASE CG
  cleanup(){
    [[ ! -f "$CG/cgroup.kill" ]] || echo 1 > "$CG/cgroup.kill"
    rmdir "$BASE/root" "$BASE/scratch" "$BASE" 2>/dev/null || true
    rmdir "$CG" 2>/dev/null || true
  }
  trap cleanup EXIT
  echo "Results: $OUT/results.json"
  ( echo "$BASHPID" > "$CG/cgroup.procs"; exec timeout -k 5 1800 unshare --mount --net --pid --fork --kill-child --uts --ipc bash "$HERE/run-isolated.sh" inner )
  exit
fi
mount --make-rprivate /
mkdir -p /run/netns
mount -t tmpfs -o size=1m,nosuid,nodev tmpfs /run/netns
ip netns add qa-a
ip netns add qa-b
ip link add qa-va type veth peer name qa-vb
ip link set qa-va netns qa-a
ip link set qa-vb netns qa-b
for side in a b; do
  n=1; [[ "$side" == b ]] && n=2
  ip -n qa-$side link set lo up
  ip -n qa-$side addr add 10.203.0.$n/30 dev qa-v$side
  ip -n qa-$side -6 addr add fd42:203::$n/64 dev qa-v$side nodad
  ip -n qa-$side link set qa-v$side up
done
mount -t tmpfs -o size=512m,nosuid,nodev,mode=1777 tmpfs "$BASE/scratch"
ROOT="$BASE/root"
mount -t tmpfs -o size=4m,nosuid,nodev tmpfs "$ROOT"
mkdir -p "$ROOT"/{usr,input,package,scratch,proc,dev/net,etc/alternatives,opt/pengutunnel-offline,run/systemd/system}
mount --bind /usr "$ROOT/usr"
mount -o remount,bind,ro,nosuid,nodev "$ROOT/usr"
mount --bind /etc/alternatives "$ROOT/etc/alternatives"
mount -o remount,bind,ro,nosuid,nodev "$ROOT/etc/alternatives"
mount --bind "$HERE" "$ROOT/input"
mount -o remount,bind,ro,nosuid,nodev "$ROOT/input"
mount --bind "$TARGET" "$ROOT/package"
mount -o remount,bind,ro,nosuid,nodev "$ROOT/package"
mount --bind "$BASE/scratch" "$ROOT/scratch"
mkdir -p "$BASE/scratch"/{root,packages,localbin}
ln -s scratch/root "$ROOT/root"
mount --bind "$BASE/scratch/packages" "$ROOT/opt/pengutunnel-offline"
mount --bind "$BASE/scratch/localbin" "$ROOT/usr/local/bin"
for name in bin sbin lib lib64; do ln -s usr/$name "$ROOT/$name"; done
ln -s scratch/tmp "$ROOT/tmp"
ln -s /proc/self/fd "$ROOT/dev/fd"
ln -s /proc/self/fd/0 "$ROOT/dev/stdin"
ln -s /proc/self/fd/1 "$ROOT/dev/stdout"
ln -s /proc/self/fd/2 "$ROOT/dev/stderr"
for name in null zero random urandom; do touch "$ROOT/dev/$name"; mount --bind /dev/$name "$ROOT/dev/$name"; done
touch "$ROOT/dev/tty"; mount --bind /dev/tty "$ROOT/dev/tty"
touch "$ROOT/dev/net/tun"
mount --bind /dev/net/tun "$ROOT/dev/net/tun"
mount -t proc -o ro,nosuid,nodev,noexec proc "$ROOT/proc"
printf '127.0.0.1 localhost\n' > "$ROOT/etc/hosts"
printf 'hosts: files\n' > "$ROOT/etc/nsswitch.conf"
mount -o remount,ro,nosuid,nodev "$ROOT"
mkdir -p "$BASE/scratch"/{home,tmp}
chmod 1777 "$BASE/scratch"/{home,tmp}
exec env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8 HOME="$BASE/scratch/home" TMPDIR="$BASE/scratch/tmp" \
 python3 -I "$HERE/integration.py" "$BASE" "$OUT" "${PENGU_TEST_SUITE:-all}"
