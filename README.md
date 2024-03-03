# Discord Vanity Sniper

This project is a Python script that automates the process of sniping vanity URLs on Discord. It uses a list of tokens and proxies to attempt to claim a specified vanity URL for a given guild.

## Features

- Automated vanity URL sniping
- Proxy support
- Configurable delay between snipe attempts
- Console logging with different levels of severity

## Usage

1. Clone the repository.
2. Install the required Python packages
3. Configure the `config.toml` file with your desired settings.
4. Insert your tokens and proxies into the `tokens.txt` and `proxies.txt` files, respectively.
5. Run the script using `python main.py`.

## Configuration

The `config.toml` file contains the following options:

- `delay`: The delay between snipe attempts, in seconds.
- `guild_id`: The ID of the guild for which to snipe the vanity URL.
- `new_vanity_url`: The vanity URL to snipe.

## Credits

Some of the code in this project was copied from [User319183's Discord Joiner](https://github.com/User319183/Discord-Joiner), which is a modified version of [this project](https://github.com/imvast/Discord-Joiner). The original code has been modified to suit the needs of this project.

## Disclaimer

This script is for educational purposes only. Misuse of this script may violate Discord's Terms of Service. The author is not responsible for any actions taken by those who use this script.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.