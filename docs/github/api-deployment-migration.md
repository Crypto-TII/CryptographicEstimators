# API image publication and GitOps migration

The old library workflows fetched the API from Bitbucket and targeted the retired
ECS deployment. The current platform configuration is EKS / Argo CD in Canada.
PR #322 now replaces those workflows with API **candidate publication**, not a
cluster restart. See [AWS and platform administrator setup](aws-oidc-deployment.md)
for the existing DevOps role, GitHub App settings, runtime prerequisites and rollout steps.

The workflows fetch private `Crypto-TII/cryptographic-estimators-api` at `master`
with a short-lived GitHub App token limited to read-only Contents. The checkout
moves outside the public library Docker context and credentials are not persisted.
`API_CHECKOUT_APP_ID` and `API_CHECKOUT_APP_PRIVATE_KEY` remain required.

The checked-out library is built locally, then used as the API base through a
generated temporary Dockerfile. This ties the API candidate to both source
revisions without pulling/publishing the old public ECR base. The standard API
Dockerfile is used in both EKS environments. Environment-specific settings belong
in Kubernetes; the retired integration Dockerfile's staging domains are not used.
Neither API_KEY_ARG nor a mail secret is passed as a build argument.

| Library branch | Proposed platform environment | Published repository |
| --- | --- | --- |
| `develop` | `estimators-devops` (confirm with platform owner) | Canadian private ECR `estimators-api` |
| `main` | `estimators-production` | Canadian private ECR `estimators-api` |

Each publication uses a new tag, records library/API commits and saves an
`api-promotion.json` artifact. A reviewed change to the selected environment's
`imageApiTag` in the platform repository authorizes Argo CD deployment. The
workflow has no platform write token and no cluster/ECS access. It does not change
the frontend image or push any shared `latest` tag. Production's existing
`gh-pages` documentation publishing is preserved.

The API's runtime SendGrid credential must be rotated and provided from a
Kubernetes Secret as `SANIC_SENDGRID_API_KEY`; confirm proxy trust, origins and
canonical URLs for the selected environment before promotion. The current chart
shows only Redis environment settings, so runtime configuration needs review.

Opening/pushing this draft runs normal CI only. A library release-branch merge
would publish an image; merging a platform tag change would deploy it. Neither is
authorized yet. The old ECS permissions, me-central-1 targets, four-role/public ECR
proposal and S3 frontend publishing are not part of this release path. Audit other
consumers before retiring old AWS or Bitbucket secrets.
