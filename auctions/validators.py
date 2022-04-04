from django import db
from django.core.exceptions import ValidationError


def validate_negative_bid(bid):
    # bids must be greater than $0

    if bid < 0.01:
        raise ValidationError(
            "$%(bid).2f cannot be a negative value", params={"bid": bid}
        )
