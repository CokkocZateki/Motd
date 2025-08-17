# Alliance Auth
from allianceauth.authentication.models import User

# AA Motd
from motd.models import MotdMessage


def create_motd(user: User, **kwargs) -> MotdMessage:
    """Create a MotdMessage"""
    params = {
        "created_by": user,
    }
    params.update(kwargs)
    motd = MotdMessage(**params)
    motd.save()
    return motd
