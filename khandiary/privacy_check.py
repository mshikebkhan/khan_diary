def privacy_check(request, profile):
    """Check the profile is user's or public."""
    if profile.user == request.user or profile.public == True:
        status = "green"
    else:
        status = "red"

    return status
