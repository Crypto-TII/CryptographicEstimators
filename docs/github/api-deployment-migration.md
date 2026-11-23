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

| Library branch | Platform environment | Published repository |
| --- | --- | --- |
| `develop` | `estimators-devops` (AWS staging) | Canadian private ECR `estimators-api` |
| `main` | `estimators-production` | Canadian private ECR `estimators-api` |

Each publication uses a new tag, records library/API commits and saves an
`api-promotion.json` artifact. A reviewed change to the selected environment's
`imageApiTag` in the platform repository authorizes Argo CD deployment. The
workflow has no platform write token and no cluster/ECS access. It does not change
the frontend image or push any shared `latest` tag. Production's existing
`gh-pages` documentation publishing is preserved.

The API's runtime SendGrid credential must be rotated and provided from a
Kubernetes Secret as `SANIC_SENDGRID_API_KEY`; confirm proxy trust, origins and
canonical URLs for the selected environment before promotion. Read-only cluster
inspection on 23 November confirmed both API pods received these settings and
the required mail Secret reference resolved at startup. Rotation and delivery
remain separate checks; ready pods do not prove those.

Feature-branch pushes and PR checks run CI without publication. A library
release-branch merge publishes a candidate; a reviewed platform tag change
deploys it. PR #322 still needs one other maintainer approval. Production
promotion remains a separate release decision. The old ECS permissions, me-central-1 targets, four-role/public ECR
proposal and S3 frontend publishing are not part of this release path. Audit other
consumers before retiring old AWS or Bitbucket secrets.

## Non-publishing container validation

`api-container-build-check.yml` checks out the API with the read-only App, builds
the library and API on a disposable runner, then tests runtime imports with no
network. It has no AWS credentials or registry publication step.

The first real build found a Python 3.12 incompatibility in the API's test-only
Lua dependencies. [Merged API PR #3](https://github.com/Crypto-TII/cryptographic-estimators-api/pull/3)
separates runtime and test requirements. `API_BUILD_CHECK_REF` was cleared after
that merge; the diagnostic and publication workflows now both read API `master`.
A non-publishing build against the merged API passed.

The EKS frontend container and devops API target were merged in
[webapp PR #4](https://github.com/Crypto-TII/cryptographicestimators-webapp/pull/4).
Its production/devops container checks and unit/Cypress tests passed. Frontend
publication remains disabled until a coordinated release; these library release
workflows do not build or publish the frontend.

The running images do not yet exhibit the remediated session/CSRF behavior.
Publish and promote the matching API and frontend together, then verify the
staging session, cookie flags, allowed origins and calculation flow before any
production promotion. Kubernetes reports both environments' existing Deployments
rolled out and available; that does not prove the new application code is running.
