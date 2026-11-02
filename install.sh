#!/usr/bin/env bash
set -euo pipefail
umask 077

# Readable bootstrap. Each release pins the exact core and manager it executes.
REPOSITORY="xemadx/pengutunnel-offline"
PACKAGE_VERSION="v5.1.3-r4"
CORE_SHA="495044c59b0d9515e0ca9b741e81cecabb04a0698a7ad252259de0e52906a250"
MANAGER_SHA="ee2073c3ba1edca80bb7a24b0b435445afbef3ef6d0f9ae20cc7ecef01b42a18"
VERIFY_ONLY=false
REF=""
SOURCE_DIR=""
die(){ printf 'Error: %s\n' "$*" >&2; exit 1; }
while (($#)); do
  case "$1" in
    --verify-only) VERIFY_ONLY=true; shift ;;
    --ref) (($# >= 2)) || die '--ref needs a Git ref'; REF="$2"; shift 2 ;;
    --source-dir) (($# >= 2)) || die '--source-dir needs a directory'; SOURCE_DIR="$2"; shift 2 ;;
    -h|--help)
      printf '%s\n' 'Usage: bash install.sh [--verify-only] [--ref REF] [--source-dir DIR]' \
        'Default: fetch this tagged release, verify it, install the persistent pengu CLI and open its menu.' \
        '--verify-only performs no installation or service changes.'
      exit 0 ;;
    *) die "unknown option: $1" ;;
  esac
done
[[ "$(uname -s)" == Linux ]] || die 'Linux is required'
[[ "$(uname -m)" == x86_64 ]] || die 'this core supports x86_64 only'
command -v sha256sum >/dev/null || die 'sha256sum is required'
[[ -z "$REF" || ( "$REF" =~ ^[[:alnum:]_.-]+$ && "$REF" != .* ) ]] || die 'invalid Git ref'

if [[ -z "$SOURCE_DIR" && -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  candidate="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
  if [[ -f "$candidate/pengutunnel.offline.elf" && -f "$candidate/install-offline.sh" ]]; then
    SOURCE_DIR="$candidate"
  fi
fi
work="$(mktemp -d)"
stage=""; next=""
trap 'rm -rf -- "$work"; [[ -z "$stage" ]] || rm -rf -- "$stage"; [[ -z "$next" ]] || rm -f -- "$next"' EXIT
fetch(){
  curl --fail --show-error --location --proto '=https' --tlsv1.2 \
    --connect-timeout 15 --max-time 600 --retry 2 "$1" --output "$2"
}
for filename in pengutunnel.offline.elf install-offline.sh; do
  if [[ -n "$SOURCE_DIR" ]]; then
    [[ -f "$SOURCE_DIR/$filename" ]] || die "missing $filename"
    cp -- "$SOURCE_DIR/$filename" "$work/$filename"
  else
    command -v curl >/dev/null || die 'curl and CA certificates are required'
    if [[ -n "$REF" ]]; then
      fetch "https://raw.githubusercontent.com/$REPOSITORY/$REF/$filename" "$work/$filename" || die "download failed: $filename"
    else
      printf 'Downloading %s (%s)...\n' "$filename" "$PACKAGE_VERSION" >&2
      fetch "https://github.com/$REPOSITORY/releases/download/$PACKAGE_VERSION/$filename" "$work/$filename" || \
        fetch "https://raw.githubusercontent.com/$REPOSITORY/$PACKAGE_VERSION/$filename" "$work/$filename" || die "download failed: $filename"
    fi
  fi
done
(
  cd -- "$work"
  printf '%s  %s\n' "$CORE_SHA" pengutunnel.offline.elf "$MANAGER_SHA" install-offline.sh | sha256sum --check --strict -
) || die 'checksum mismatch; nothing installed'
bash -n "$work/install-offline.sh"
if "$VERIFY_ONLY"; then
  printf '%s\n' 'Verified core and manager. No installation or service change was performed.'
  exit 0
fi
[[ "$EUID" -eq 0 ]] || die 'run with sudo, for example: curl -fsSL INSTALL_URL | sudo bash'
command -v systemctl >/dev/null || die 'systemd is required'
[[ -d /run/systemd/system ]] || die 'systemd must be running (WSL needs systemd enabled)'
( test -t 0 </dev/tty ) 2>/dev/null || die 'an interactive terminal is required'

# Keep reviewed files so reopening the menu never needs a deleted temp directory.
base=/opt/pengutunnel-offline
release="$base/releases/$PACKAGE_VERSION"
if [[ -e /usr/local/bin/pengu ]] && ! grep -q '^# PenguTunnel offline CLI$' /usr/local/bin/pengu; then
  die '/usr/local/bin/pengu already belongs to another installation; it was not replaced'
fi
mkdir -p "$base/releases" /usr/local/bin
stage="$(mktemp -d "$base/releases/.install.XXXXXXXX")"
cp -- "$work/pengutunnel.offline.elf" "$work/install-offline.sh" "$stage/"
chmod 700 "$stage" "$stage/pengutunnel.offline.elf" "$stage/install-offline.sh"
if [[ -e "$release" ]]; then
  cmp -s "$stage/pengutunnel.offline.elf" "$release/pengutunnel.offline.elf" && \
    cmp -s "$stage/install-offline.sh" "$release/install-offline.sh" || die "existing release differs: $release"
  rm -rf -- "$stage"
else
  mv -- "$stage" "$release"
fi
next="$base/.current.$$"
ln -s "$release" "$next"
mv -Tf -- "$next" "$base/current"
cat > "$work/pengu" <<'CLI'
#!/usr/bin/env bash
# PenguTunnel offline CLI
set -euo pipefail
case "${1:-menu}" in
  menu) exec bash /opt/pengutunnel-offline/current/install-offline.sh ;;
  update)
    [[ "$EUID" -eq 0 ]] || { echo 'Run: sudo pengu update [TAG]' >&2; exit 1; }
    (($# <= 2)) || { echo 'Usage: pengu update [TAG]' >&2; exit 1; }
    ref="${2:-}"
    url="https://github.com/xemadx/pengutunnel-offline/releases/latest/download/install.sh"
    if [[ -n "$ref" ]]; then
      [[ "$ref" =~ ^v[0-9]+\.[0-9]+\.[0-9]+-r[1-9][0-9]*$ ]] || { echo 'Invalid tag' >&2; exit 1; }
      url="https://github.com/xemadx/pengutunnel-offline/releases/download/$ref/install.sh"
    fi
    file="$(mktemp)"; trap 'rm -f -- "$file"' EXIT
    curl -fSL --proto '=https' --tlsv1.2 --connect-timeout 15 --max-time 120 \
      "$url" -o "$file"
    grep -q '^PACKAGE_VERSION=' "$file" || { echo 'This older tag does not support the versioned CLI bootstrap.' >&2; exit 1; }
    bash "$file"
    ;;
  *) echo 'Usage: sudo pengu [menu | update [TAG]]' >&2; exit 1 ;;
esac
CLI
install -m 755 "$work/pengu" /usr/local/bin/pengu
printf '\nInstalled %s. Open this menu later with: sudo pengu\n\n' "$PACKAGE_VERSION"
bash "$release/install-offline.sh" </dev/tty
