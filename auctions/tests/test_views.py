import pytest
from django.test import Client, TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_index(self):
        client = Client()
        url = reverse("auctions:index")
        response = client.get(url)
        self.assertTemplateUsed(response, "auctions/index.html")
        assert response.status_code == 200


@pytest.mark.django_db
def test_watchlist_owner(user_watchlist):
    assert user_watchlist.user.username == "seyamack"


@pytest.mark.django_db
def test_watchlist_listing(user_watchlist):
    assert user_watchlist.listing.title == "puppies for sale"
