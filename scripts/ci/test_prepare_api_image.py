"""Isolated preparation checks; no Docker, AWS or cluster access is used."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("prepare_api_image.py")
BASE = "FROM public.ecr.aws/h0m6q0n8/estimators-lib\nWORKDIR /home/api\nCOPY . .\n"


class PrepareApiImageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.api = self.root / "private-api"
        self.api.mkdir()
        self.runner = self.root / "runner"
        self.runner.mkdir()
        (self.api / "Dockerfile").write_text(BASE)
        subprocess.run(["git", "init", "-q", str(self.api)], check=True)
        subprocess.run([
            "git", "-C", str(self.api), "-c", "user.name=Test fixture",
            "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
            "commit", "--allow-empty", "-qm", "fixture",
        ], check=True)
        self.env = {
            **os.environ,
            "GITHUB_SHA": "a" * 40,
            "API_SOURCE_DIR": str(self.api),
            "PLATFORM_RELEASE": "estimators-devops",
            "GITHUB_REF": "refs/heads/develop",
            "GITHUB_RUN_ID": "12345",
            "GITHUB_RUN_ATTEMPT": "1",
            "RUNNER_TEMP": str(self.runner),
            "GITHUB_ENV": str(self.root / "env"),
            "GITHUB_STEP_SUMMARY": str(self.root / "summary"),
        }

    def invoke(self, **overrides):
        return subprocess.run(
            [sys.executable, str(SCRIPT)], env={**self.env, **overrides},
            text=True, capture_output=True,
        )

    def test_devops_candidate_uses_local_library_and_leaves_checkout_unchanged(self):
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.runner / "api-promotion.json").read_text())
        self.assertEqual(record["releaseName"], "estimators-devops")
        self.assertTrue(record["image"].startswith(
            "450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-api:lib-"))
        self.assertEqual(record["library_revision"], "a" * 40)
        self.assertIn(record["api_revision"][:12], record["imageApiTag"])
        self.assertNotIn(record["imageApiTag"], ["latest", "devops"])
        self.assertEqual((self.api / "Dockerfile").read_text(), BASE)
        self.assertEqual((self.runner / "Dockerfile.api-candidate").read_text(),
                         f"FROM estimators-library:{'a' * 40}\n" + BASE.partition("\n")[2])
        self.assertIn("API_IMAGE=" + record["image"], (self.root / "env").read_text())

    def test_production_candidate(self):
        result = self.invoke(GITHUB_REF="refs/heads/main", PLATFORM_RELEASE="estimators-production")
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads((self.runner / "api-promotion.json").read_text())
        self.assertEqual(record["releaseName"], "estimators-production")

    def test_rerun_has_a_different_tag(self):
        self.assertEqual(self.invoke().returncode, 0)
        original = json.loads((self.runner / "api-promotion.json").read_text())["imageApiTag"]
        self.assertEqual(self.invoke(GITHUB_RUN_ATTEMPT="2").returncode, 0)
        rerun = json.loads((self.runner / "api-promotion.json").read_text())["imageApiTag"]
        self.assertNotEqual(original, rerun)

    def test_branch_cannot_select_another_environment(self):
        for overrides in [
            {"PLATFORM_RELEASE": "estimators-production"},
            {"GITHUB_REF": "refs/pull/322/merge"},
            {"GITHUB_REF": "refs/heads/feature"},
        ]:
            with self.subTest(overrides=overrides):
                self.assertNotEqual(self.invoke(**overrides).returncode, 0)
                self.assertFalse((self.root / "env").exists())

    def test_changed_base_requires_review(self):
        (self.api / "Dockerfile").write_text("FROM different-base\nCOPY . .\n")
        self.assertNotEqual(self.invoke().returncode, 0)
        self.assertFalse((self.root / "env").exists())

    def test_invalid_revision_or_run_metadata_is_rejected(self):
        for overrides in [{"GITHUB_SHA": "invalid"}, {"GITHUB_RUN_ID": "x\nunsafe"}]:
            with self.subTest(overrides=overrides):
                self.assertNotEqual(self.invoke(**overrides).returncode, 0)
                self.assertFalse((self.root / "env").exists())


if __name__ == "__main__":
    unittest.main()
