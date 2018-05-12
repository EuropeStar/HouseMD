def jwt_response_payload_handler(token, user=None, request=None):
    from api_v0.serializers import ProfileSerializer
    if user:
        return {
            'token': token,
            'user': ProfileSerializer(user.profile, context={'request': request}).data
        }
    else:
        return {
            'token': token
        }