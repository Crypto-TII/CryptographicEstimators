"""Prepare an API candidate without changing the API checkout or GitOps repository."""

import json
import os
from pathlib import Path
import re
import subprocess


def prepare_build_dockerfile(api_source, library_image, runner_temp):
    """Use the locally built library without modifying the private checkout."""
    dockerfile = (api_source / "Dockerfile").read_text()
    base, separator, body = dockerfile.partition("\n")
    if base.strip() != "FROM public.ecr.aws/h0m6q0n8/estimators-lib" or not separator:
        raise ValueError("API Dockerfile base changed; review the build integration")
    generated = runner_temp / "Dockerfile.api-candidate"
    generated.write_text(f"FROM {library_image}\n{body}")
    return generated


def prepare():
    library_sha = os.environ["GITHUB_SHA"]
    api_source = Path(os.environ["API_SOURCE_DIR"])
    api_sha = subprocess.check_output(
        ["git", "-C", str(api_source), "rev-parse", "HEAD"], text=True
    ).strip()
    if not all(re.fullmatch(r"[0-9a-f]{40}", sha) for sha in (library_sha, api_sha)):
        raise ValueError("Expected full library and API commit SHAs")
    release = os.environ["PLATFORM_RELEASE"]
    expected_release = {
        "refs/heads/develop": "estimators-devops",
        "refs/heads/main": "estimators-production",
    }.get(os.environ["GITHUB_REF"])
    if release != expected_release:
        raise ValueError("Release does not match the library branch")
    run_id, attempt = os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"]
    if not run_id.isdecimal() or not attempt.isdecimal():
        raise ValueError("Expected numeric GitHub run ID and attempt")
    repository = "450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-api"
    tag = f"lib-{library_sha[:12]}-api-{api_sha[:12]}-{run_id}-{attempt}"
    library_image = f"estimators-library:{library_sha}"
    image = f"{repository}:{tag}"
    # Both EKS environments use the same image; Kubernetes supplies runtime settings.
    # Replace only the reviewed base line, leaving all API build instructions intact.
    runner_temp = Path(os.environ["RUNNER_TEMP"])
    generated = prepare_build_dockerfile(api_source, library_image, runner_temp)
    record = {
        "platform_repository": "Crypto-TII/estimators-platform",
        "platform_file": "argocd-apps/environments/estimators-eks/estimators-applicationset.yaml",
        "releaseName": release,
        "imageApiTag": tag,
        "image": image,
        "library_revision": library_sha,
        "api_revision": api_sha,
        "workflow_run": f"https://github.com/Crypto-TII/CryptographicEstimators/actions/runs/{run_id}",
        "deployment": "Requires a reviewed platform PR; no platform files were changed.",
    }
    (runner_temp / "api-promotion.json").write_text(json.dumps(record, indent=2) + "\n")
    with open(os.environ["GITHUB_ENV"], "a") as output:
        output.write(f"LIBRARY_IMAGE={library_image}\nAPI_IMAGE={image}\n")
        output.write(f"API_BUILD_DOCKERFILE={generated}\n")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as output:
        output.write(f"### API image candidate for {release}\n\n`{image}`\n\n")
        output.write("After publication succeeds, use the promotion artifact in a reviewed "
                     "`estimators-platform` PR. This workflow does not deploy to EKS.\n")


if __name__ == "__main__":
    prepare()
