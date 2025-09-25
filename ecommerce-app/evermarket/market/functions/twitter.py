from requests_oauthlib import OAuth1Session
from django.conf import settings


class Tweet:
    """
    Singleton Tweet class for handling Twitter OAuth and making tweets
    Only one instance will exist during runtime.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the Tweet object")
            cls._instance = super(Tweet, cls).__new__(cls)
            # By default, use saved tokens
            cls._instance._init_oauth()
        return cls._instance

    def _init_oauth(self):
        """Initialize OAuth session with saved tokens"""
        self.oauth = OAuth1Session(
            settings.TWITTER_CONSUMER_KEY,
            client_secret=settings.TWITTER_CONSUMER_SECRET,
            resource_owner_key=settings.TWITTER_ACCESS_TOKEN,
            resource_owner_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
        )

    def authenticate(self):
        """
        Runs the OAuth flow on demand (check README for instructions):
        - Get request token
        - Ask user to authorize app in browser
        - Enter PIN back into app
        - Exchange for access tokens
        """
        # Part 1: Get request token
        request_token_url = (
            "https://api.twitter.com/oauth/request_token"
            "?oauth_callback=oob&x_auth_access_type=write"
        )

        oauth = OAuth1Session(
            settings.TWITTER_CONSUMER_KEY,
            client_secret=settings.TWITTER_CONSUMER_SECRET,
        )

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print("Invalid consumer key/secret — check your settings")
            return

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got request token:", resource_owner_key)

        # Part 2: Direct user to authorize
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize:", authorization_url)

        verifier = input("Paste the PIN here: ")

        # Part 3: exchange for access tokens
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            settings.TWITTER_CONSUMER_KEY,
            client_secret=settings.TWITTER_CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        print("Save these tokens in settings.py for future use!")
        print("Access Token:", access_token)
        print("Access Token Secret:", access_token_secret)

        # Store session for this run
        self.oauth = OAuth1Session(
            settings.TWITTER_CONSUMER_KEY,
            client_secret=settings.TWITTER_CONSUMER_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def make_tweet(self, text, media_id=None):
        """
        Post a tweet with optional media.
        Raises an exception if the request fails.
        """
        # Check if tweet object has the auth attribute
        # or if it's not None.
        if not hasattr(self, "oauth") or not self.oauth:
            raise Exception("You must authenticate first!")

        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}

        if media_id:
            payload["media"] = {"media_ids": [media_id]}

        response = self.oauth.post(url, json=payload)

        if response.status_code != 201:
            raise Exception(
                f"Tweet failed ({response.status_code}): {response.text}"
            )

        data = response.json()
        print("Tweet sent:", data)
        return data

    def upload_media(self, file_path, mime_type="image/jpeg"):
        """
        Uploads media to Twitter and returns the media_id_string.
        Supports jpg, png, gif. Raises exception if upload fails.
        """
        url = "https://upload.twitter.com/1.1/media/upload.json"

        try:
            with open(file_path, "rb") as f:
                files = {"media": (file_path, f, mime_type)}
                response = self.oauth.post(url, files=files)
        except FileNotFoundError:
            raise Exception(f"Media file not found: {file_path}")

        if response.status_code != 200:
            raise Exception(
                f"Media upload failed ({response.status_code}): "
                f"{response.text}"
            )

        data = response.json()
        print("Media uploaded:", data)
        return data["media_id_string"]
