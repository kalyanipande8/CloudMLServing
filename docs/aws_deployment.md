# AWS deployment notes (unexecuted)

No AWS account/credentials are available in this environment. The
intended production deployment: build the Docker image from this repo's
`Dockerfile`, push to ECR, deploy on ECS Fargate behind an Application
Load Balancer, and use the GitHub Actions workflow in
`.github/workflows/ci.yml` as the CI stage of a CD pipeline that would
push to ECR on a passing `main` build. This is disclosed as an unexecuted
deployment plan, not claimed as a running deployment. The CI workflow
itself IS real and executable — GitHub Actions will genuinely run the test
suite on every push to this repo.
