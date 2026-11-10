# Flappy_Ghost

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Engine-Pygame--CE-green)
![PyForgeUI](https://img.shields.io/badge/UI-PyForgeUI-blueviolet)
![PyForgeAI](https://img.shields.io/badge/AI-PyForgeAI-orange)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Drakonosinc/Flappy_Ghost)

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
