# Short-lived AWS deployment access

The release workflows obtain one-hour AWS sessions using GitHub OIDC. They no
longer read `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY`. Each workflow obtains
fresh credentials for public ECR in `us-east-1`, then for private ECR and ECS in
`me-central-1`. The second login clears the first session before requesting its
own OIDC session; it does not chain roles or fall back to stored AWS keys.

This changes authentication only. Pushes to `develop` still deploy staging;
pushes to `main` still deploy production. No additional manual approval is added.
PRs and feature-branch pushes do not trigger these deployment workflows.

## AWS administrator setup (before merging)

1. Confirm which AWS account owns public ECR alias `h0m6q0n8` and which owns the
   private ECR repositories and ECS cluster. They may be different accounts.
2. In each account that will contain a deployment role, create or reuse an IAM
   OpenID Connect provider with URL `https://token.actions.githubusercontent.com`
   and audience `sts.amazonaws.com`.
3. Create the roles below. The suggested names are optional; set their maximum
   session duration to at least 3,600 seconds. Use the environment's trust JSON
   for both roles, replacing `<AWS_ACCOUNT_ID>` with the account containing that
   role and the OIDC provider. Attach only the corresponding permission policy,
   replacing its account placeholder with the resource-owning account ID.

| Suggested role | Trust template | Permissions template |
| --- | --- | --- |
| `github-estimators-staging-public-ecr` | [staging-trust.json](aws-oidc/staging-trust.json) | [staging-public-ecr-policy.json](aws-oidc/staging-public-ecr-policy.json) |
| `github-estimators-staging-deploy` | [staging-trust.json](aws-oidc/staging-trust.json) | [staging-deploy-policy.json](aws-oidc/staging-deploy-policy.json) |
| `github-estimators-production-public-ecr` | [production-trust.json](aws-oidc/production-trust.json) | [production-public-ecr-policy.json](aws-oidc/production-public-ecr-policy.json) |
| `github-estimators-production-deploy` | [production-trust.json](aws-oidc/production-trust.json) | [production-deploy-policy.json](aws-oidc/production-deploy-policy.json) |

The public role publishes only its library repository. The deployment role
publishes only its private API repository and can update only its ECS service.
Registry authentication requires wildcard resources; image publication and ECS
updates are scoped to explicit resources. No repository creation, IAM changes,
task-definition registration or `iam:PassRole` is granted by these templates.
Confirm actual resource ARNs and any organizational SCP, permission-boundary or
repository-policy restrictions. These are configuration templates, not evidence
that the live AWS permissions have been tested.

The staging trust accepts only
`repo:Crypto-TII/CryptographicEstimators:ref:refs/heads/develop`; production accepts
only `repo:Crypto-TII/CryptographicEstimators:ref:refs/heads/main`. Neither accepts
the PR subject or another repository. Do not replace these with broad wildcards.
Any workflow running on the trusted branch with `id-token: write` can request
that branch's role, so protect release branches and review workflow changes.

The repository OIDC configuration was checked during preparation: it uses the
default subject with `use_immutable_subject: false`. If this setting changes,
update the trust policies to match before rollout. Adding a GitHub Environment
to a deployment job also changes its OIDC subject and requires corresponding
trust and environment branch restrictions. These workflows add no Environment.

## GitHub repository configuration

An administrator of `Crypto-TII/CryptographicEstimators` must set these **Actions
repository variables**, using the full IAM role ARNs supplied by the AWS admin:

| Variable | Role |
| --- | --- |
| `AWS_STAGING_PUBLIC_ECR_ROLE_ARN` | Staging public ECR publisher |
| `AWS_STAGING_DEPLOY_ROLE_ARN` | Staging private ECR / ECS deployment |
| `AWS_PRODUCTION_PUBLIC_ECR_ROLE_ARN` | Production public ECR publisher |
| `AWS_PRODUCTION_DEPLOY_ROLE_ARN` | Production private ECR / ECS deployment |

Role ARNs identify roles; they are not secret access keys. No AWS credential
secret is needed. A missing or malformed ARN stops the workflow before AWS
authentication, image publication or service restart. The existing GitHub App
configuration for reading the private API repository is also still required;
see [API deployment migration](api-deployment-migration.md).

## Validation and rollout

Preparing this change does not create AWS roles, configure live trust, publish
images or restart services. Syntax and isolated command tests do not validate
actual AWS authorization. There is deliberately no manual dispatch added here.

Before approving a merge, the AWS administrator must confirm the provider,
trust policies, role permissions and resource/account IDs, and the GitHub admin
must populate the four variables and API checkout settings. Keep the PR draft
until configuration and release timing have been agreed: merging it into
`develop` automatically starts a real staging deployment.

During the first authorized staging rollout, verify successful role assumption,
public and private image publication, and ECS service health. Session names
include environment, purpose, GitHub run ID and attempt for CloudTrail tracing.
Only promote to `main` after staging and production configuration are verified.

After successful cutover, identify other consumers of the old AWS keys before
disabling them and removing their GitHub secrets. Do not revoke a shared key
blindly. If authentication fails, correct the trust/permissions or configuration;
do not reintroduce permanent keys as an automatic fallback.

## References

- [GitHub: configuring OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [AWS: private ECR image push permissions](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html)
- [AWS: public ECR repository policies and authentication](https://docs.aws.amazon.com/AmazonECR/latest/public/public-repository-policies.html)
