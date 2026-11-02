#!/usr/bin/env python3
"""Publish already verified release assets using GitHub's Releases API."""
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from check_package import ROOT, verify


def main():
    manifest = verify()
    tag = manifest["package_version"]
    ref = os.environ.get("GITHUB_REF", "")
    if ref != "refs/tags/" + tag:
        raise SystemExit("Only the matching package tag can publish a release")
    repository = os.environ.get("GITHUB_REPOSITORY", "xemadx/pengutunnel-offline")
    if os.environ.get("GITHUB_REPOSITORY_ID") != "1438976927":
        raise SystemExit("Unexpected repository identity")
    token = os.environ["GITHUB_TOKEN"]

    def request(url, method="GET", body=None, binary=None):
        host = urllib.parse.urlparse(url).hostname
        if host not in ("api.github.com", "uploads.github.com"):
            raise ValueError("Unexpected GitHub API host")
        headers = {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
                   "X-GitHub-Api-Version": "2026-03-10", "User-Agent": "pengutunnel-release"}
        data = json.dumps(body).encode() if body is not None else binary
        if data is not None:
            headers["Content-Type"] = "application/json" if body is not None else "application/octet-stream"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.load(response)

    base = f"https://api.github.com/repos/{repository}"
    try:
        release = request(base + "/releases/tags/" + tag)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        body = (ROOT / "docs/RELEASE-NOTES.fa.md").read_text(encoding="utf-8")
        release = request(base + "/releases", "POST", dict(tag_name=tag, name=tag, body=body,
                                                           draft=True, prerelease=False))
    existing = {item["name"]: item for item in request(release["assets_url"] + "?per_page=100")}
    files = [ROOT / "dist" / "SHA256SUMS", ROOT / "dist" / "install.sh",
             ROOT / "dist" / "install-offline.sh", ROOT / "dist" / "pengutunnel.offline.elf",
             ROOT / "dist" / "offline-package-manifest.json",
             ROOT / "dist" / f"pengutunnel-offline-{tag}-linux-amd64.tar.gz"]
    files.extend(ROOT / "dist" / name for name in (
        f"engine-functions-{tag}.tsv", f"engine-assembly-{tag}.asm.gz", f"engine-analysis-{tag}.json"))
    for file in files:
        data = file.read_bytes()
        digest = "sha256:" + hashlib.sha256(data).hexdigest()
        if file.name in existing:
            if existing[file.name].get("digest") != digest:
                raise SystemExit("Existing release asset differs: " + file.name)
            continue
        upload = release["upload_url"].split("{", 1)[0] + "?name=" + urllib.parse.quote(file.name)
        result = request(upload, "POST", binary=data)
        if result.get("digest") != digest:
            raise SystemExit("Uploaded asset digest differs: " + file.name)
        print("Uploaded:", file.name)
    if release["draft"]:
        release = request(release["url"], "PATCH", dict(draft=False, make_latest="true"))
    print("Published:", release["html_url"])


if __name__ == "__main__":
    main()
