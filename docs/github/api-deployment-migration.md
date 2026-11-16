# API deployment checkout migration

The library's production and staging release workflows now fetch the private
`Crypto-TII/cryptographic-estimators-api` repository from GitHub, explicitly at
`master`. Both API environments currently share that branch; Dockerfile selection
separates their configuration. The checked-out API commit is recorded in the log.

| Workflow | API Dockerfile | Library image used by that Dockerfile |
| --- | --- | --- |
| Production (`main`) | `Dockerfile` | `public.ecr.aws/h0m6q0n8/estimators-lib` |
| Staging (`develop`) | `Dockerfile.integration` | `public.ecr.aws/h0m6q0n8/staging/estimators/lib:latest` |

The API checkout is moved into a unique runner-temporary directory before any
image build. This keeps the private API source outside the public library image's
Docker build context. Checkout credentials are not persisted in Git configuration.
The existing library checkout stays at the workspace root for documentation/Pages.

## Required configuration before merging or deploying

The default workflow token only reads its own repository. An organization
administrator must configure a GitHub App installation with **Contents: read**
access to **only** `Crypto-TII/cryptographic-estimators-api`, and set these values
on `Crypto-TII/CryptographicEstimators`:

- Actions variable `API_CHECKOUT_APP_ID`: the App ID.
- Actions secret `API_CHECKOUT_APP_PRIVATE_KEY`: the App's private key.

The workflows request a short-lived installation token narrowed to that one API
repository and read-only contents. The action revokes it at job completion. Neither
personal credentials nor browser tokens are reused. Missing App configuration
fails the workflow before AWS login, image publication or ECS restart.

`BITBUCKET_ORG`, `BITBUCKET_REPOSITORY`, `BITBUCKET_API_TOKEN` and `API_KEY_ARG` are no
longer referenced by these two workflows. Check for other consumers before removing
those repository secrets. Do not print or copy their values into the PR or logs.

The mail credential must be injected into the API's ECS task at runtime as
`SANIC_SENDGRID_API_KEY`; it is not supplied as a Docker build argument. Confirm
runtime secret injection, prior credential rotation and the actual ingress proxy
CIDRs before rollout. Production uses the API security defaults for its origin and
canonical URL; staging's Dockerfile supplies staging-specific values. See the API
repository's `docs/security-remediation.md` for the remaining deployment settings.

## Release behavior and review

AWS credential inputs, registry names, ECS service names and workflow triggers are
preserved. The obsolete Node 16 AWS credential action is upgraded to a pinned v6
release; ECR login uses pinned v2. Checkout and App-token actions are also pinned. This PR does not migrate AWS authentication to OIDC or change release
policy. The production workflow still publishes documentation to `gh-pages`,
with explicit write permission for its library-repository workflow token.

**Merging into `develop` triggers staging deployment; promoting `develop` to `main`
triggers production deployment.** Keep this PR unmerged until the configuration
above and release approval are complete. Opening/pushing the feature branch does
not trigger either deployment workflow. No workflow dispatch or deployment is
needed for syntax validation or the isolated command dry-run.
