# AWS Automated Compliance & Drift Detection Pipeline

A cloud security portfolio project that automatically detects AWS resource misconfigurations using AWS Config, Lambda, and SNS.

## What It Does

Monitors AWS resources in real time and flags non-compliant configurations:

- **S3 buckets** — detects missing public access blocks
- **IAM users** — detects missing MFA
- **EC2 security groups** — detects unrestricted SSH (0.0.0.0/0 on port 22)

When a violation is detected, AWS Config invokes a custom Lambda evaluator which marks the resource as `NON_COMPLIANT` and logs an annotation describing the issue.

## Architecture
AWS Config Recorder
│
▼
Config Rule (Custom Lambda)
│
▼
Lambda: evaluate_compliance.py
│
├── NON_COMPLIANT → Config Dashboard
└── SNS Topic → Email Alert

## Stack

- **Terraform** — all infrastructure defined as code
- **AWS Config** — resource change recording and rule evaluation
- **AWS Lambda** (Python 3.12) — custom compliance logic
- **SNS** — email alerting on violations
- **S3** — Config snapshot delivery

## Project Structure
aws-compliance-drift-pipeline/
├── terraform/
│   ├── main.tf          # All AWS infrastructure
│   ├── variables.tf     # Input variables
│   ├── outputs.tf       # Output values
│   └── providers.tf     # AWS provider config
├── config-rules/
│   └── evaluate_compliance.py   # Lambda compliance evaluator
├── docs/
│   └── runbook.md
└── README.md
## Deployment

Prerequisites: AWS CLI authenticated, Terraform installed.

```bash
cd terraform
terraform init
terraform apply
```

You will be prompted for:
- `alert_email` — email to receive compliance alerts
- `aws_account_id` — your AWS account ID

## Compliance Rules

| Rule | Resource | Violation Condition |
|------|----------|-------------------|
| Public Access Block | S3 Bucket | Any public access block disabled |
| MFA Required | IAM User | No MFA device attached |
| No Open SSH | EC2 Security Group | Port 22 open to 0.0.0.0/0 |

## Test

To trigger a test violation:

```bash
aws s3api create-bucket --bucket your-test-bucket --region us-east-1
aws s3api delete-public-access-block --bucket your-test-bucket
```

Then check:

```bash
aws configservice get-compliance-details-by-resource \
  --resource-type AWS::S3::Bucket \
  --resource-id your-test-bucket \
  --region us-east-1
```

## Author

Bestin Varghese — Cloud Security Portfolio  
[GitHub](https://github.com/Bestin11)
