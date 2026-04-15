import json
import boto3

def lambda_handler(event, context):
    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event.get("configurationItem")

    if not configuration_item:
        return

    resource_type = configuration_item["resourceType"]
    resource_id = configuration_item["resourceId"]
    compliance = "COMPLIANT"
    annotation = "Resource is compliant."

    # Rule 1: S3 bucket must not be public
    if resource_type == "AWS::S3::Bucket":
        supplementary = configuration_item.get("supplementaryConfiguration", {})
        public_access = supplementary.get("PublicAccessBlockConfiguration", {})
        if not all([
            public_access.get("BlockPublicAcls"),
            public_access.get("BlockPublicPolicy"),
            public_access.get("IgnorePublicAcls"),
            public_access.get("RestrictPublicBuckets"),
        ]):
            compliance = "NON_COMPLIANT"
            annotation = "S3 bucket does not have all public access blocks enabled."

    # Rule 2: IAM user must have MFA enabled
    elif resource_type == "AWS::IAM::User":
        supplementary = configuration_item.get("supplementaryConfiguration", {})
        mfa_devices = supplementary.get("MFADevices", [])
        if len(mfa_devices) == 0:
            compliance = "NON_COMPLIANT"
            annotation = "IAM user has no MFA device attached."

    # Rule 3: Security group must not allow unrestricted SSH
    elif resource_type == "AWS::EC2::SecurityGroup":
        config = configuration_item.get("configuration", {})
        inbound_rules = config.get("ipPermissions", [])
        for rule in inbound_rules:
            if rule.get("fromPort") == 22 and rule.get("toPort") == 22:
                for ip_range in rule.get("ipv4Ranges", []):
                    if ip_range.get("cidrIp") == "0.0.0.0/0":
                        compliance = "NON_COMPLIANT"
                        annotation = "Security group allows SSH from 0.0.0.0/0."

    # Report result back to AWS Config
    config_client = boto3.client("config")
    config_client.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType": resource_type,
                "ComplianceResourceId": resource_id,
                "ComplianceType": compliance,
                "Annotation": annotation,
                "OrderingTimestamp": configuration_item["configurationItemCaptureTime"],
            }
        ],
        ResultToken=event["resultToken"],
    )