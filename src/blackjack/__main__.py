"""Entry point: python -m blackjack"""
import webbrowser
import threading
from blackjack.web.app import create_app


def main():
    import os
    app = create_app()
    port = int(os.environ.get("PORT", 5000))

    if not os.environ.get("PORT"):
        def open_browser():
            webbrowser.open(f"http://localhost:{port}")
        threading.Timer(1.0, open_browser).start()

    print(f"\n  \u2665 BlackJack running at http://localhost:{port}\n")
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    main()
