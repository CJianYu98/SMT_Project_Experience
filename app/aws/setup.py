from .lambda_service import create_iam_role_permission_policy, create_lambda_iam_role

# from .s3 import s3_setup

# s3_setup()
permission_policy_name = create_iam_role_permission_policy()
create_lambda_iam_role(permission_policy_name)
