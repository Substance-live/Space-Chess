# 🧠 Space Chess

![GitHub last commit](https://img.shields.io/github/last-commit/Substance-live/Space-Chess)

A strategy-based chess-inspired game with custom units, skills, animations, and resource mechanics. Made with pygame.

![Gameplay](assets/gameplay.gif)

---

## 🎮 Instructions

This is not your average chess. Each side commands a fantasy army of custom units with unique roles and powerful skills. The game is turn-based and requires a mouse to interact.

### 🧩 Objective
Defeat the enemy king using tactical movement, mana crystals, and five powerful skills.

### 🎮 Controls
| Mouse Action     | Function                              |
|------------------|---------------------------------------|
| Left Click       | Select piece, activate skill          |
| Right Click      | Move piece, cancel selection or skill |

---

## ⚔️ Skills

Each player can choose from 5 powerful skills:

| Skill Name         | Description                 | Mana Cost |
|--------------------|-----------------------------|-----------|
| Castling           | Swap pieces defensively     | 2         |
| Overload           | Push your unit to move again| 10        |
| Time Rewind        | Undo your last move         | 15        |
| Return             | Teleport piece to previous pos| 50      |
| Last Chance        | Revive fallen ally briefly  | 99        |

---

## 🧪 Installation

> Python 3.6+ required. Game built using [pygame](https://www.pygame.org/).

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Substance-live/Space-Chess.git
   cd Space-Chess
   ```
2. **Create and activate a virtual environment**:
   * On windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
### 🎮 Start Game
To start the game, run either:
```bash
$ python main.py
```

## 🧠 Features
* Turn-based tactical chess combat
* Custom fantasy units and teams
* Mana-based skill system
* Animation effects for kills, skills, and game over
* Two-player mode on one machine
* Rich UI with timers, skill panels, and mana counters

## 💡 Future Improvements
- AI opponent
- Network multiplayer
- Skill editor / mod support
- Sound effects and music

## 🤝 Contributions
Have ideas or want to help? Fork the repo and make it better — whether it's new features, better graphics, or bug fixes!

Issues and pull requests are welcome. ✨
