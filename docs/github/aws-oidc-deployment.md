# AWS OIDC access for EKS / Argo CD image publication

This guide supersedes the earlier ECS / me-central-1 instructions and four-role
proposal. Do not configure the old ECS roles, public ECR roles or their variables.

## Confirmed repository configuration

The private [estimators-platform repository](https://github.com/Crypto-TII/estimators-platform)
defines EKS cluster `estimators` in `ca-central-1`, account `450891466448`, and:

- API: `450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-api`.
- Frontend: `450891466448.dkr.ecr.ca-central-1.amazonaws.com/estimators-frontend`.
- Argo CD environments `estimators-devops` and `estimators-production`, both in
  namespace `estimators`. The existing devops environment is not assumed to be
  identical to the retired staging environment; confirm the intended mapping.
- Argo CD watches platform `main` and automatically syncs the Helm configuration.
  The ApplicationSet currently assigns API tag `latest` to both environments.

These are repository findings, not a verification of the running cluster, image
architecture, registry ownership, credentials or current publishing pipeline.
The platform owner must confirm them before merging this draft PR.

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

This verifies the **checked-in Terraform configuration**, not the live IAM role's
applied policy or successful role assumption. No AWS login, role assumption,
image publication or infrastructure change was performed for this check. The
administrator should confirm this configuration has been applied; the first
explicitly authorized publication must verify role assumption and ECR access.

The earlier two-role templates and the four-role ECS/public-ECR proposal are
superseded. Their duplicate JSON templates have been removed from this PR; DevOps
should maintain IAM in its existing Terraform module. No action is needed on the
old proposed role variables. Audit consumers before removing any existing keys.

## Other prerequisites and rollout

The GitHub administrator must still provide `API_CHECKOUT_APP_ID` and
`API_CHECKOUT_APP_PRIVATE_KEY` for a GitHub App with **Contents: read** on only
`Crypto-TII/cryptographic-estimators-api`. The library's default token cannot read
that private repository. No personal or browser token is used. These names are
absent from repository-level Actions variables/secrets. Organization-level
settings could not be inspected with the current GitHub permissions, so check
whether inherited organization settings already supply them before creating new
credentials. The AWS publishing role does not provide GitHub repository access.

Before promotion, the platform owner must confirm Argo CD actually watches this
repo, can read it, and can pull the published ECR images. Confirm access to Argo CD
application sync/health and Kubernetes rollout logs. Preserve existing frontend
settings and arrange runtime API configuration in Kubernetes, including
`SANIC_SENDGRID_API_KEY` from a Secret and ingress proxy trust/CORS/canonical URL
settings. Devops needs its own frontend/API hostnames. The checked-in API Deployment
currently supplies only Redis host/port; do not assume mail/security settings are
already injected. See the API repository's security remediation guide.

Before a first devops rollout, agree how to pin the existing production image so
that both environments no longer share an unversioned mutable tag. Do not merge
platform changes during this PR's preparation: its `main` is live GitOps input.

Keep library PR #322 draft until configuration, one required reviewer approval and
CI are complete. No AWS/cluster operation was performed to prepare these files.
Feature-branch pushes/PR checks do not publish images. Merging to a library release
branch starts real ECR publication (and production's existing docs publishing),
but does not update Argo CD or deploy an application. Do not merge yet.

After an authorized candidate publication, verify the image/revisions and runtime
settings, review and merge the selected platform tag change, then verify Argo CD
sync/health and application behavior. Promote to production with its own reviewed
platform change. Reverting the environment's tag to a known-good image provides a
GitOps rollback; this still requires release authorization.

Only after a verified cutover, audit other consumers before revoking old AWS keys
or deleting their GitHub secrets. Do not reinstate permanent-key fallback.

## References

- [GitHub OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [AWS ECR push permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html)
- [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)
