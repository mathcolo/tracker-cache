# tracker-cache
tracker-cache is the backend for [https://newtrains.today](https://newtrains.today). The browser display components are located [here](https://github.com/mathcolo/tracker-static).

## Installation requirements
- Python 3.6+ with [pipenv](https://pipenv.readthedocs.io/en/latest/) installed
- Redis


## Development instructions
1. In the project root, create a file named `secrets.py` and populate it with your MBTA v3 API key: `API_KEY = <KEY>`
2. Install and run [Redis](https://redis.io/) locally
3. In the root directory, run `pipenv install` to install Python dependencies
4. Run `python pull.py` to populate your Redis cache a single time (in production this is run every minute via cron)
5. Run `python server.py` to begin serving the API locally
6. Set up [tracker-static](https://github.com/mathcolo/tracker-static) to see the API consumed by the front-end JavaScript.