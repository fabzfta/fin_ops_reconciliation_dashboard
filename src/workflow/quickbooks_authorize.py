"""
Run the QuickBooks Online OAuth 2.0 authorization flow locally.

The script:
1. Starts a temporary local callback server.
2. Opens the Intuit authorization page.
3. Receives the OAuth callback.
4. Validates the state parameter.
5. Exchanges the authorization code for tokens.
6. Stores the credentials locally.
"""

import json
import threading
import webbrowser

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from integrations.quickbooks.oauth import QuickBooksOAuth


HOST = "localhost"
PORT = 8000

TOKEN_FILE = Path(".quickbooks_tokens.json")

oauth = QuickBooksOAuth()

authorization_url, expected_state = (
    oauth.generate_authorization_url()
)

oauth_result = {}
callback_received = threading.Event()


class OAuthCallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed_url.query)

        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        realm_id = params.get("realmId", [None])[0]
        error = params.get("error", [None])[0]

        if error:
            self.send_response(400)
            self.end_headers()

            self.wfile.write(
                b"QuickBooks authorization failed. "
                b"You can close this window."
            )

            oauth_result["error"] = error
            callback_received.set()
            return

        if state != expected_state:
            self.send_response(400)
            self.end_headers()

            self.wfile.write(
                b"Invalid OAuth state. "
                b"You can close this window."
            )

            oauth_result["error"] = "invalid_state"
            callback_received.set()
            return

        if not code or not realm_id:
            self.send_response(400)
            self.end_headers()

            self.wfile.write(
                b"Missing authorization data. "
                b"You can close this window."
            )

            oauth_result["error"] = "missing_oauth_data"
            callback_received.set()
            return

        oauth_result["code"] = code
        oauth_result["realm_id"] = realm_id

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.end_headers()

        self.wfile.write(
            b"""
            <html>
                <body>
                    <h2>QuickBooks connected successfully.</h2>
                    <p>You can close this window.</p>
                </body>
            </html>
            """
        )

        callback_received.set()

    def log_message(self, format, *args):
        # Disable the default HTTP server logs.
        return


def save_tokens(
    token_data: dict,
    realm_id: str,
) -> None:
    """
    Persist QuickBooks OAuth credentials locally.

    This file must never be committed to source control.
    """

    credentials = {
        "realm_id": realm_id,
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expires_in": token_data.get("expires_in"),
        "x_refresh_token_expires_in":
            token_data.get("x_refresh_token_expires_in"),
    }

    TOKEN_FILE.write_text(
        json.dumps(credentials, indent=2),
        encoding="utf-8",
    )


def main() -> None:

    server = HTTPServer(
        (HOST, PORT),
        OAuthCallbackHandler,
    )

    print("")
    print("QuickBooks OAuth")
    print("----------------")
    print("")
    print(
        f"Waiting for callback at "
        f"http://{HOST}:{PORT}/callback"
    )

    print("")
    print("Opening Intuit authorization page...")

    webbrowser.open(authorization_url)

    while not callback_received.is_set():
        server.handle_request()

    server.server_close()

    if "error" in oauth_result:
        raise RuntimeError(
            f"OAuth authorization failed: "
            f"{oauth_result['error']}"
        )

    print("")
    print("Authorization callback received.")
    print("OAuth state validated.")

    token_data = oauth.exchange_code(
        oauth_result["code"]
    )

    save_tokens(
        token_data=token_data,
        realm_id=oauth_result["realm_id"],
    )

    print("")
    print("Authorization successful.")
    print(
        "QuickBooks credentials saved locally "
        f"to {TOKEN_FILE}"
    )
    print("")
    print(
        "No OAuth tokens were printed "
        "to the terminal."
    )


if __name__ == "__main__":
    main()