"""
STEP 8a - Log in to Google once (Gmail + Pub/Sub).

Before running this, follow "Step 8: Gmail + Pub/Sub" in README.md and put
the credentials.json file you downloaded from Google Cloud in this folder.

This script:
  1. Prints a Google login link
  2. You log in and click "Allow"
  3. Your browser then goes to a "localhost" page that FAILS TO LOAD.
     That's expected! Copy the full address from the browser's address bar
     and paste it here.
  4. It saves token.json, so you don't have to log in again.

Run:  python step8_gmail_auth.py
"""
import os

from google_auth_oauthlib.flow import InstalledAppFlow

# Needed because the localhost address you paste starts with http://, not https://
# (only that pasted address is http; the talk with Google itself is https)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",  # read your emails
    "https://www.googleapis.com/auth/pubsub",  # receive the notifications
]


def main():
    if not os.path.exists("credentials.json"):
        raise SystemExit(
            "❌ credentials.json not found in this folder.\n"
            "   Create it in Google Cloud first: see 'Step 8' in README.md (8.1 - 8.4)."
        )
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES, redirect_uri="http://localhost:8080/"
    )
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")

    print("1. Open this link in your browser and log in:\n")
    print(auth_url)
    print("\n2. After you click 'Allow', the page will fail to load. That's OK.")
    print("   Copy the FULL address from the browser's address bar")
    print("   (it starts with http://localhost:8080/?state=...)\n")
    redirected_url = input("3. Paste it here and press Enter: ").strip()

    flow.fetch_token(authorization_response=redirected_url)

    with open("token.json", "w") as f:
        f.write(flow.credentials.to_json())
    print("\n✅ Logged in! Saved token.json. Next: python step8_gmail_agent.py")


if __name__ == "__main__":
    main()
