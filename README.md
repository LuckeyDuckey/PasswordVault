# PasswordVault
![python 3.8](https://img.shields.io/badge/python-3.8-blue) ![pygame-ce 2.5.2](https://img.shields.io/badge/pygamece-2.5.2-green)

A simple, secure, desktop password vault built with Python and Pygame, featuring a GUI built with a custom library called PYRA. It was designed for my personal use, it focuses on minimalism, functionality, and aesthetics.

![alt text](https://github.com/LuckeyDuckey/PasswordVault/blob/main/Data/Banner.png)

## Usage

To run the PasswordVault simply follow these steps (you’ll need Python 3.8 or newer):

1. Clone or download this repository:
   ```bash
   git clone https://github.com/LuckeyDuckey/PasswordVault.git
   ```

2. Install dependencies using pip:
   ```bash
   pip install pygame-ce numpy cryptography
   ```

3. Run the program:
   ```bash
   cd PasswordVault
   python Main.py
   ```

4. Set or Enter Your Master Password, on first launch, you’ll be prompted to set a master password. On subsequent launches, use the same password to unlock your vault. To reset everything, simply delete `Data/Vault.json` plus all the images inside `Data/PasswordIcons/...` this removes all saved data.

## Technical Details

### PYRA UI Library

This project’s entire interface is built using [PYRA (Pygame Rendering Assistant)](https://github.com/LuckeyDuckey/PYRA) a UI framework I created to simplify  UI design in Python using pygame-ce. PYRA uses a clean parameter based architecture, where every element (like buttons, containers, or text inputs) are defined using flexible “Parameter Objects” that control layout, visuals, and behavior. It supports automatic placement, animations, and an intuitive container system for managing layouts. Its still in development and only has a few elements right now, but PYRA is still a solid choise for any developers looking to make desktop applications using pygame-ce.

### Encryption and Data Security

All stored passwords are encrypted using Fernet (an implementation of AES-128 in CBC mode with SHA256 HMAC) along with salting to protect against brute force and rainbow table attacks. Data is securely stored in a local JSON file (`Data/Vault.json`), and decryption requires the user’s master password. This ensures that even if someone gets access to the vault file, the contents remain unreadable without the master password. While this isn’t intended to replace enterprise grade password managers, it provides solid encryption and safe local storage for personal use.

## Disclaimer

This project was originally built for my personal use, and I decided to open source it on a whim. While it’s fully functional, it may not be the most user friendly or polished application for everyone. Use it, explore it, or tweak it as you wish, but don't expect it to be perfect!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
