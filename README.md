# Blackjack CLI

A simple, terminal-based Blackjack game written in Python.
It follows standard casino rules and is built with clean, modular code so it’s easy to read, test, and extend.

---

## Overview

This project started as a small experiment in building a Blackjack engine that separates game logic from user interaction.
It uses object-oriented design with distinct classes for the deck, dealer, player, and game engine.
The CLI layer only handles input/output, keeping the core logic testable and reusable.

---

## Features

* Full Blackjack gameplay with betting and chip tracking
* Dealer AI that stands or hits according to configurable soft 17 rules
* CLI interface for player input (`hit`, `stand`, `double`, `quit`)
* Support for multiple decks and customizable chip count
* Clean, readable structure

---

## How to Run

Clone the repo and run it directly:

```bash
git clone https://github.com/kunlxo/blackjack-cli.git
cd blackjack-cli
python main.py
```

---

## Controls

* **h** – Hit
* **s** – Stand
* **d** – Double (if you have enough chips)
* **q** – Quit round or exit game

You’ll start with a set number of chips. Place bets each round and see how long you can stay alive.

---

## Example

```
=============================================
🂡  BLACKJACK  🂮
=============================================
Dealer: K♣ ??
Player: 10♦ 6♠             16
(h)it | (s)tand | (d)ouble: h

Dealer: K♣ ??
Player: 10♦ 6♠ 4♥           20
(h)it | (s)tand | (d)ouble: s

Dealer: K♣ 9♦              19
You win!
Chips remaining: 115.0
```

---

## Project Structure

```
blackjack/
├── cli/
│   └── cli.py             # Handles player input and display
├── engine/
│   └── blackjack_game.py            # Main game loop
├── models/
│   ├── card.py, deck.py, hand.py, player.py, dealer.py, enums.py, config.py
│   └── participant.py     # Base class for Player/Dealer
└── constants/
    └── messages.py        # All printed messages
```

## Future Ideas

* Add split and surrender options
* Persistent player stats or leaderboard
* Colored CLI output
* Multiplayer or network mode
