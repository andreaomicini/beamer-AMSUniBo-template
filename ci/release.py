#!/usr/bin/env python3
"""Release the built template on GitLab and on GitHub, from the GitLab CI.

The tag is "<version>-<UTC time-stamp>", the version read from the template's macros
(compute-version.py). On GitLab the PDF goes to the project's generic package registry and the
release links it (with the job token); on GitHub a release with the same tag carries the PDF as an
asset (with GITHUB_TOKEN, a fine-grained token kept as a masked, protected CI variable).

Usage (in the CI, from the project root):  release.py <file.tex> <file.pdf> <description>
"""
import datetime, json, os, subprocess, sys, urllib.parse, urllib.request

tex, pdf, what = sys.argv[1], sys.argv[2], sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
version = subprocess.run([sys.executable, os.path.join(here, 'compute-version.py'), tex],
                         check=True, capture_output=True, text=True).stdout.strip()
tag = f"{version}-{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H%M%S}"
name = f"{os.path.splitext(os.path.basename(pdf))[0]}-{tag}.pdf"
sha = os.environ['CI_COMMIT_SHA']
notes = f"{what} {version}, released from {sha}."
data = open(pdf, 'rb').read()


def call(method, url, headers, body=None):
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        text = r.read().decode()
        return json.loads(text) if text.strip() else {}


# GitLab: the PDF in the generic package registry, then the release linking it
api, pid = os.environ['CI_API_V4_URL'], os.environ['CI_PROJECT_ID']
job = {'JOB-TOKEN': os.environ['CI_JOB_TOKEN']}
pkg = f"{api}/projects/{pid}/packages/generic/{os.environ['CI_PROJECT_NAME']}/{tag}/{urllib.parse.quote(name)}"
call('PUT', pkg, job, data)
call('POST', f"{api}/projects/{pid}/releases", {**job, 'Content-Type': 'application/json'},
     json.dumps({'tag_name': tag, 'ref': sha, 'name': tag, 'description': notes,
                 'assets': {'links': [{'name': name, 'url': pkg, 'link_type': 'package'}]}}).encode())
print(f"GitLab release {tag}: {os.environ['CI_PROJECT_URL']}/-/releases/{tag}")

# GitHub: the same release on the mirror, the PDF as its asset
repo = os.environ.get('GITHUB_REPO', f"andreaomicini/{os.environ['CI_PROJECT_NAME']}")
gh = {'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}", 'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28'}
rel = call('POST', f"https://api.github.com/repos/{repo}/releases", {**gh, 'Content-Type': 'application/json'},
           json.dumps({'tag_name': tag, 'target_commitish': sha, 'name': tag, 'body': notes}).encode())
call('POST', f"https://uploads.github.com/repos/{repo}/releases/{rel['id']}/assets?name={urllib.parse.quote(name)}",
     {**gh, 'Content-Type': 'application/pdf'}, data)
print(f"GitHub release {tag}: {rel['html_url']}")
