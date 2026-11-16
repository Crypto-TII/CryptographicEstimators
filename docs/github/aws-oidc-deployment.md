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

## AWS administrator configuration

1. Confirm account `450891466448`, registry/repository, EKS region, node image
   architecture and the current image-publishing process with the platform owner.
   The GitHub-hosted build currently targets the runner's Linux/amd64 architecture.
   Do not change active infrastructure or existing publishers during preparation.
2. In that AWS account create/reuse an IAM OIDC provider:
   URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com`.
3. Create two roles with maximum session duration at least 3,600 seconds:

| Suggested role | Trust policy | Permission policy |
| --- | --- | --- |
| `github-estimators-devops-ecr-publisher` | [staging-trust.json](aws-oidc/staging-trust.json) | [staging-ecr-policy.json](aws-oidc/staging-ecr-policy.json) |
| `github-estimators-production-ecr-publisher` | [production-trust.json](aws-oidc/production-trust.json) | [production-ecr-policy.json](aws-oidc/production-ecr-policy.json) |

The first trusts only `repo:Crypto-TII/CryptographicEstimators:ref:refs/heads/develop`;
the second trusts only `repo:Crypto-TII/CryptographicEstimators:ref:refs/heads/main`.
Both require audience `sts.amazonaws.com`. The repository OIDC configuration was
verified as default subject, `use_immutable_subject: false`. Update trust if that
setting changes. No GitHub Environment is added; adding one changes the subject.
Any workflow with token permission on the trusted branch can assume that role,
so protect branches and review workflow changes. PR subjects are not trusted.

Permissions allow authentication plus image upload to **only** `estimators-api`.
They grant no ECS, EKS, Kubernetes, IAM, S3, frontend publication or public ECR
access. Registry login requires `Resource: "*"`; publication uses the explicit
Canadian API repository ARN. Review account SCPs, permission boundaries and ECR
policies. No repository is created by the workflow.

4. Return the two full role ARNs. The GitHub repository administrator must set:

| Actions repository variable | Role |
| --- | --- |
| `AWS_STAGING_ECR_ROLE_ARN` | Devops candidate publisher, trusted library `develop` |
| `AWS_PRODUCTION_ECR_ROLE_ARN` | Production candidate publisher, trusted library `main` |

The variable name STAGING retains the library branch/workflow terminology;
its proposed platform destination is `estimators-devops`, subject to owner approval.
No permanent AWS key is needed. The workflow validates the account, clears
ambient credentials, and checks AWS's returned account ID. The prior variables
`AWS_STAGING_PUBLIC_ECR_ROLE_ARN`, `AWS_STAGING_DEPLOY_ROLE_ARN`,
`AWS_PRODUCTION_PUBLIC_ECR_ROLE_ARN`, `AWS_PRODUCTION_DEPLOY_ROLE_ARN` are unused.

## Other prerequisites and rollout

The GitHub administrator must still configure `API_CHECKOUT_APP_ID` and
`API_CHECKOUT_APP_PRIVATE_KEY` for a GitHub App with **Contents: read** on only
`Crypto-TII/cryptographic-estimators-api`. The library's default token cannot read
that private repository. No personal or browser token is used.

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
