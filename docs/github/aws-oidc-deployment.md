# AWS OIDC access for EKS / Argo CD image publication

This guide supersedes the earlier ECS / me-central-1 instructions and four-role
proposal. Do not configure the old ECS roles, public ECR roles or their variables.

## Confirmed repository configuration

The private [estimators-platform repository](https://github.com/Crypto-TII/estimators-platform)
defines EKS cluster `estimators` in `ca-central-1`, account `450891466448`, and:

- API: `450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-api`.
- Frontend: `450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-frontend`.
- Argo CD environments `estimators-devops` and `estimators-production`, both in
  namespace `estimators`. DevOps confirmed `estimators-devops` is AWS staging;
  the retired on-premises staging deployment no longer exists.
- Argo CD watches platform `main` and automatically syncs the Helm configuration.
  The ApplicationSet currently assigns API tag `latest` to both environments.

Read-only verification on 23 November confirmed the running estimator
Deployments observed their latest generations, completed rollout and have ready
containers. Both API pods contain the configured HTTPS/origin/proxy variables and
required mail Secret reference. Direct AWS staging HTTPS checks passed with
normal certificate verification. Current application behavior still lacks the
remediated session/CSRF handling, so publishing and promoting updated images
remains necessary. Registry uploads and email delivery have not been tested.

## New release path

1. A library `develop` / `main` push builds the checked-out library and GitHub API
   `master` source together. Both EKS environments use the API's standard
   `Dockerfile`; the retired staging Dockerfile contains obsolete staging URLs.
   A generated runner-temporary Dockerfile substitutes the locally built library
   base. No API checkout file changes, public ECR push or remote library base pull
   is needed. Private API source remains outside the library build context.
2. GitHub obtains a one-hour OIDC session scoped to Canadian ECR image publication.
   Each run publishes a unique tag containing library/API revisions and run ID /
   attempt. It never overwrites `latest` or `devops`.
3. The workflow saves `api-promotion.json` as an artifact, identifying both source
   revisions, image, environment and exact platform file/field to update.
4. After checks and release approval, a separate reviewed platform PR changes
   only the selected environment's `imageApiTag` in
   `argocd-apps/environments/estimators-eks/estimators-applicationset.yaml` to that
   published tag. Merging the platform PR lets Argo CD roll out the new image.

GitHub does not call ECS, kubectl, the EKS API or Argo CD. It has no platform-repo
write token and does not open or merge platform PRs automatically. Image-tag
changes cause a Kubernetes rollout; `imagePullPolicy: Always` alone does not
restart running pods when an existing tag is overwritten. Pin environment tags
and use reviewed tag changes rather than relying on mutable `latest` images.

This PR does not build or publish the frontend. Its existing EKS image stays
unchanged. Production documentation publishing to `gh-pages` is preserved; that
is separate from application deployment. Library merges publish candidates;
platform merges authorize application deployment. Full automatic promotion would
be a separate agreed change after confirming existing release ownership.

## Existing DevOps role (configuration checked)

DevOps has configured
`arn:aws:iam::450891466448:role/github-actions-estimators-ecr-push`.
Both publication workflows now use this role directly in `ca-central-1`. No
publisher role-ARN variables or new IAM roles are required for these workflows.

The source of truth is the DevOps-owned Terraform module:

- [ECR push configuration](https://github.com/Crypto-TII/terraform-aws/blob/main/terraform/iam-ecr-push/config.yaml)
- [IAM trust and permissions](https://github.com/Crypto-TII/terraform-aws/blob/main/terraform/iam-ecr-push/main.tf)

The configuration lists all three repositories: `CryptographicEstimators`,
`cryptographic-estimators-api` and `cryptographicestimators-webapp` under
`Crypto-TII`. It currently allows every branch (`*`) and `v*` tags in each repo,
with a maximum session duration of 3,600 seconds. Thus the library's `develop`
and `main` branch subjects are allowed. The OIDC audience is `sts.amazonaws.com`.
The library repository uses default non-immutable subject claims, matching the
Terraform-generated trust subjects.

**Do not add `environment: stage`.** No environments are listed for this role in
`config.yaml`; the Terraform module only trusts environment subjects when they
are explicitly configured. Adding an environment changes the OIDC subject from
`repo:Crypto-TII/CryptographicEstimators:ref:refs/heads/develop` (or `main`) to
`repo:Crypto-TII/CryptographicEstimators:environment:stage`, which this configuration
does not allow. The library repository currently has only `github-pages`, not
`stage`, as a GitHub Environment.

The shared role allows push/pull on `estimators-api` and `estimators-frontend` in
Canadian ECR. The library workflows publish only an API candidate and do not
use frontend permissions. No cluster access is granted by this Terraform policy.
Its permissions include image download and description for cache/pull support,
as well as uploads and registry login. Workflows clear ambient credentials and
validate AWS's returned account ID before publication.

The wildcard branch trust is explicitly marked as temporary developer-testing
access by DevOps. Before production cutover, ask DevOps to narrow allowed branches
per repository to approved release branches (library `develop` / `main`), and
review whether the shared API/frontend permissions remain appropriate. The
library publication triggers stay limited to release branches; do not broaden
them to match the temporary IAM wildcard. Protect those branches and review
workflow changes.

Live read-only verification passed on 2026-11-19: GitHub assumed the expected AWS
role, confirmed account `450891466448`, authenticated to ECR and read API image
metadata. The [diagnostic workflow](https://github.com/Crypto-TII/CryptographicEstimators/actions/runs/44497749014)
does not build, push or deploy images. Actual upload permissions and the full IAM
policy were not tested/read. Subsequent read-only cluster checks verified the
existing rollouts; a release of the new images remains unverified.

The earlier two-role templates and the four-role ECS/public-ECR proposal are
superseded. Their duplicate JSON templates have been removed from this PR; DevOps
should maintain IAM in its existing Terraform module. No action is needed on the
old proposed role variables. Audit consumers before removing any existing keys.

## Other prerequisites and rollout

The private checkout configuration is complete and verified as of 2026-11-19:

- App: [peacker-estimators-api-checkout](https://github.com/apps/peacker-estimators-api-checkout),
  owned by `peacker`, App ID `5832804`.
- Crypto-TII installation `183675601` selects **only** the private API repository,
  with **Contents: read** and mandatory **Metadata: read**. No write permissions,
  OAuth user authorization or webhook subscriptions are used.
- Repository variable `API_CHECKOUT_APP_ID` and encrypted Actions secret
  `API_CHECKOUT_APP_PRIVATE_KEY` are configured on the library repository.
- The diagnostic workflow successfully created a restricted installation token,
  read the private API README and revoked the token after verification. Temporary
  local key files were removed after secure secret storage and verification.

The App is installable on other accounts so the personal registration can be
installed on Crypto-TII. This does not publish the private API source. Its private
repository access is limited by the selected installation. No personal/browser
token is reused. Future App key rotation requires updating the Actions secret;
never put a key in Git or chat. The AWS role and the library's default workflow
token do not supply this separate private-repository checkout access.

## Current release readiness (23 November 2026)

- API PR #3 and webapp PR #4 are merged. Private API checkout and the API build
  against `master` passed. The diagnostic API override variable was removed.
- The webapp's read-only OIDC/registry check passed again on 23 November. No
  reusable AWS key is needed for GitHub image publication.
- The platform now injects the runtime security settings and mail Secret
  reference. API pods started successfully with that required reference;
  credential rotation and actual email delivery are not inferred from readiness.
- Platform PR #2 is merged. Public CORS preflight checks confirmed each
  environment allows its own frontend and no longer allows localhost.
- AWS staging HTTPS works. One internal DNS resolver still returns the retired
  staging destination; the DNS owner must reconcile that view for normal access.
- Read-only Kubernetes access verifies Deployments, Pods and Ingresses. Secret
  values and Argo CD internal Application resources remain forbidden; do not
  broaden Secret access just for verification. Never place cluster credentials
  in this public repository or chat.

PR #322 is ready for one required reviewer approval and passing checks. Do not
bypass branch protection or self-approve. A merge to `develop` starts API candidate
publication; it does not update Argo CD or deploy the application. Preserve both
current image digests as rollback evidence before any staging promotion.

For staging, obtain the API promotion artifact and a matching devops frontend
candidate. Review their source revisions, keep production fields unchanged, and
change only staging image tags through an authorized platform PR. Verify HTTPS,
CSRF/session handling, cookie flags, allowed origins, calculations and rollout
health before considering a separately approved production promotion. Record
known-good image identifiers for a reviewed GitOps rollback.

Only after a verified cutover, audit other consumers before revoking old AWS keys
or deleting their GitHub secrets. Do not reinstate permanent-key fallback.

## References

- [GitHub OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [AWS ECR push permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html)
- [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
