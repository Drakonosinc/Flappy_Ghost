# Flappy_Ghost

[![Ask DeepWiki](https://img.shields.io/badge/Ask-DeepWiki-4B32C3?logo=read-the-docs&logoColor=white)](https://deepwiki.com/Drakonosinc/Flappy_Ghost)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5%2B-00A86B.svg)](https://pyga.me/)
[![PyForgeUI](https://img.shields.io/badge/UI-PyForgeUI-orange.svg)](https://pypi.org/project/pyforgeui/)
[![PyForgeAI](https://img.shields.io/badge/AI-PyForgeAI-EE4C2C.svg)](https://pypi.org/project/pyforgeai-engine/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

**Flappy_Ghost** is an object-oriented Flappy Bird-inspired arcade game built with **Pygame** and **PyTorch**. It integrates a multi-agent neuroevolution system powered by [**PyForgeAI**](https://github.com/Drakonosinc/PyForgeAI) (`pyforgeai-engine` on PyPI) and an interactive menu interface built with [**PyForgeUI**](https://github.com/Drakonosinc/PyForgeUI) (`pyforgeui` on PyPI).

---

## Features

- **Playable & Autonomous Modes**:
  - **Player Mode**: Manual control with customizable key bindings.
  - **AI Mode**: Watch a pre-trained 16-input neural network navigate through dynamic pipe gaps.
  - **Training AI Mode**: Simultaneous multi-agent neuroevolution where an entire population of ghosts learns in real time across generations.
- **Modular Ecosystem Integration**:
  - **UI Layer (`pyforgeui`)**: Menus, dynamic buttons, and scrollable AI configuration panels.
  - **AI Layer (`pyforgeai-engine`)**: Population initialization, batch fitness evaluation, elitism, crossover, adaptive mutation, and PyTorch model serialization.
- **Customizable Visuals, Audio & Controls**: Persistent JSON settings (`Config/config.json`) for flyers, pipes, audio toggles, and key bindings.

---

## Installation & Quick Start

```bash
# 1. Install dependencies (including pyforgeui and pyforgeai-engine from PyPI)
pip install -r requirements.txt

# 2. Launch the game
python src/Main.py
```

---

## License

This project is licensed under the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Author

Developed by [Drakonosinc](https://github.com/Drakonosinc)
