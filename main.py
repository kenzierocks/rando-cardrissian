"""
Launches the Rando Cardrissian client.

Also loads and merges configuration sources.
"""
from randocardrissian.config import load


def main():
    with open('config/config.py') as f:
        cfg = load(f)
    print(cfg)


if __name__ == '__main__':
    main()
