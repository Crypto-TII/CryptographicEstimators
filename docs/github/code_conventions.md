# Code style

- Line width: 120 characters.
- Use absolute imports instead of relative imports.

# GIT Conventions

## Commits

We use a subset of the
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) types,
given by:

- docs: Documentation only changes
- feat: A new feature
- fix: A bug fix
- refactor: A code change that neither fixes a bug nor adds a feature

## Branching

Branch names should be snake_case. Which means that all the text must be
lowercase and replace spaces with dashes. Also, we should add as a prefix based
on the type of implementation. For example:

```
refactor/modify_base_problem
feature/implement_dummy_estimator
fix/algorithm_parameter
```

## Pull request

1. Only create pull requests targeting the `develop` branch.
2. Fulfill the template.
