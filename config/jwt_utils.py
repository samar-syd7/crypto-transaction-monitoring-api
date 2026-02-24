from rest_framework_simplejwt.tokens import AccessToken


def issue_service_token(*, role: str, service_name: str):
    token = AccessToken()

    # REQUIRED: must be int (Django User PK compatibility)
    token["user_id"] = 0  # synthetic system identity

    # Internal service claims
    token["role"] = role
    token["service"] = service_name

    return str(token)