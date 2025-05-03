# ♟️ Chess_Game (AI Based Chess)

Welcome to **Chess_Game** — an AI-powered chess game with a rich graphical interface and smart opponent logic.  
Battle against an intelligent AI, improve your strategy, and experience a dynamic chessboard with customizable themes!

---

## 🚀 Features

- 🎯 **AI Opponent:** Smart moves generated using Minimax with Alpha-Beta Pruning.
- 🎨 **Customizable Themes:** Change piece sets and board colors on the fly.
- 🔄 **Undo Moves:** Rewind your last moves, including undoing AI moves.
- 🔥 **Real-Time Hints:** Highlighting available moves and selected pieces.
- ⚡ **Smooth Gameplay:** Built with Pygame for a responsive and interactive experience.
- 🧠 **Dynamic AI Depth:** AI analyzes multiple moves ahead (adjustable depth).

---

## 🏗️ Built With

- **Python 3**
- **Pygame** (for GUI)
- **python-chess** (for board representation and move validation)
- **Custom AI Engine** (`chess_ai.py`)

---

## 📂 Project Structure

```
Chess_Game/
├── chess_gui.py       # Graphical interface and main game logic
├── chess_ai.py        # AI logic and board evaluation
├── pieces/            # (Optional) Piece images for different themes
├── README.md          # Project documentation
```

---

## 📥 Installation and Running

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Chess_Game.git
   cd Chess_Game
   ```

2. **Install the required libraries:**
   ```bash
   pip install pygame python-chess
   ```

3. **Run the game:**
   ```bash
   python chess_gui.py
   ```

---

## 🧠 How the AI Works

- **Minimax Algorithm:** Evaluates possible game states to choose the optimal move.
- **Alpha-Beta Pruning:** Cuts off branches that don't need to be evaluated, making the AI faster.
- **Evaluation Metrics:** Material value, pawn structure, and piece mobility.
- **Depth Customization:** By default, the AI searches 3 moves ahead, adjustable in `chess_ai.py`.

---

## 🎨 Customization Options

- **Piece Sets:** Discover and switch between different sets of chess pieces (`pieces/` folder).
- **Board Themes:** Choose from classic, green, blue, gray, or purple board styles.
- **Flip Board:** Change player perspective during the match.
- **Switch Sides:** Instantly swap between playing White or Black.

---

## 📈 Future Enhancements

- Add time controls (timers).
- Implement stronger AI using advanced heuristics or neural networks.
- Online multiplayer mode.
- Opening book integration for smarter early-game moves.

---

## 🤝 Contributing

Pull requests and feature suggestions are welcome!  
Feel free to fork this project, create a branch, make changes, and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---
## 🙏 Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/en/latest/)
- [Pygame](https://www.pygame.org/)
- Inspiration from classic chess engines and open-source chess GUIs.
---
