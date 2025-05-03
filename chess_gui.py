import pygame
import sys
import time
import os
import chess
try:
    try:
        from chess_ai import ChessAI
    except ImportError:
        print("Error: 'chess_ai' module not found. Ensure 'chess_ai.py' exists in the same directory.")
        sys.exit(1)
except ImportError:
    print("Error: 'chess_ai' module not found. Ensure 'chess_ai.py' exists in the same directory.")
    sys.exit(1)

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 750
BOARD_SIZE = 600
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (180, 180, 180)


class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess with AI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.big_font = pygame.font.SysFont('Arial', 24)

        self.board = chess.Board()
        self.ai = ChessAI(depth=3)

        # Game state
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.player_color = chess.WHITE

        # Theme management
        self.piece_sets = self.discover_piece_sets()
        self.board_themes = self.discover_board_themes()
        self.current_piece_set = "default"
        self.current_board_theme = "classic"
        self.piece_images = self.load_piece_images()
        self.board_colors = self.get_board_colors()

        # UI state
        self.show_theme_menu = False

    def discover_piece_sets(self):
        """Discover available piece sets in the pieces directory"""
        sets = ["default"]  # Always have the default set
        if os.path.exists("pieces"):
            for item in os.listdir("pieces"):
                if os.path.isdir(os.path.join("pieces", item)):
                    sets.append(item)
        return sets

    def discover_board_themes(self):
        """Discover available board themes"""
        return {
            "classic": {
                "light": (240, 217, 181),
                "dark": (181, 136, 99)
            },
            "green": {
                "light": (240, 240, 210),
                "dark": (120, 160, 80)
            },
            "blue": {
                "light": (220, 230, 240),
                "dark": (100, 140, 180)
            },
            "gray": {
                "light": (220, 220, 220),
                "dark": (150, 150, 150)
            },
            "purple": {
                "light": (230, 210, 240),
                "dark": (150, 100, 180)
            }
        }

    def get_board_colors(self):
        """Get the current board theme colors"""
        return self.board_themes.get(self.current_board_theme, self.board_themes["classic"])

    def load_piece_images(self):
        """Load images for all chess pieces (macOS compatible)"""
        # Map pieces to filenames (macOS friendly)
        piece_to_file = {
            'b': 'bb.png',  # Black bishop
            'k': 'bk.png',  # Black king
            'n': 'bn.png',  # Black knight
            'p': 'bp.png',  # Black pawn
            'q': 'bq.png',  # Black queen
            'r': 'br.png',  # Black rook
            'B': 'wb.png',  # White bishop
            'K': 'wk.png',  # White king
            'N': 'wn.png',  # White knight
            'P': 'wp.png',  # White pawn
            'Q': 'wq.png',  # White queen
            'R': 'wr.png'  # White rook
        }

        images = {}
        set_path = os.path.join("pieces", self.current_piece_set) if self.current_piece_set != "default" else "pieces"

        for piece_symbol, filename in piece_to_file.items():
            try:
                # Try to load from the specified set
                img_path = os.path.join(set_path, filename)
                if os.path.exists(img_path):
                    images[piece_symbol] = pygame.image.load(img_path)
                else:
                    # Fall back to default naming if specific file doesn't exist
                    alt_path = os.path.join(set_path, f"{piece_symbol}.png")
                    if os.path.exists(alt_path):
                        images[piece_symbol] = pygame.image.load(alt_path)
                    else:
                        raise FileNotFoundError

                images[piece_symbol] = pygame.transform.scale(images[piece_symbol], (SQUARE_SIZE, SQUARE_SIZE))
            except:
                # Create a placeholder if image not found
                surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                color = (200, 200, 200) if piece_symbol.isupper() else (100, 100, 100)
                pygame.draw.rect(surf, color, (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(surf, BLACK, (0, 0, SQUARE_SIZE, SQUARE_SIZE), 2)
                text = self.font.render(piece_symbol, True, BLACK if piece_symbol.isupper() else WHITE)
                surf.blit(text, (SQUARE_SIZE // 2 - text.get_width() // 2,
                                 SQUARE_SIZE // 2 - text.get_height() // 2))
                images[piece_symbol] = surf

        return images

    def square_to_pos(self, square):
        """Convert chess square index to pixel position on board"""
        row = 7 - (square // 8)
        col = square % 8
        return (col * SQUARE_SIZE, row * SQUARE_SIZE)

    def pos_to_square(self, pos):
        """Convert pixel position to chess square index"""
        x, y = pos
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            col = x // SQUARE_SIZE
            row = 7 - (y // SQUARE_SIZE)
            return row * 8 + col
        return None

    def draw_board(self):
        """Draw the chess board with current theme"""
        colors = self.board_colors

        # Draw squares
        for row in range(8):
            for col in range(8):
                color = colors["light"] if (row + col) % 2 == 0 else colors["dark"]
                pygame.draw.rect(self.screen, color,
                                 (col * SQUARE_SIZE, row * SQUARE_SIZE,
                                  SQUARE_SIZE, SQUARE_SIZE))

        # Highlight selected square
        if self.selected_square is not None:
            x, y = self.square_to_pos(self.selected_square)
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill((247, 247, 105, 150))
            self.screen.blit(highlight, (x, y))

        # Highlight valid moves
        for move in self.valid_moves:
            x, y = self.square_to_pos(move.to_square)
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            highlight.fill((124, 252, 0, 150))
            self.screen.blit(highlight, (x, y))

        # Draw pieces
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x, y = self.square_to_pos(square)
                self.screen.blit(self.piece_images[piece.symbol()], (x, y))

    def draw_info_panel(self):
        """Draw the information panel below the board"""
        panel_rect = pygame.Rect(0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.line(self.screen, BLACK, (0, BOARD_SIZE), (WIDTH, BOARD_SIZE), 2)

        # Game status
        if self.game_over:
            status = f"Game Over - {self.board.result()}"
            color = (200, 0, 0)
        elif self.board.turn == self.player_color:
            status = "Your turn"
            color = (0, 100, 0)
        else:
            status = "AI is thinking..."
            color = (0, 0, 200)

        status_text = self.big_font.render(status, True, color)
        self.screen.blit(status_text, (20, BOARD_SIZE + 20))

        # Move history
        moves_text = "Moves: " + " ".join([str(move) for move in self.board.move_stack[-6:]])
        moves_render = self.font.render(moves_text, True, TEXT_COLOR)
        self.screen.blit(moves_render, (20, BOARD_SIZE + 50))

        # Buttons
        self.draw_button("New Game", WIDTH - 320, BOARD_SIZE + 15, 100, 30)
        self.draw_button("Undo Move", WIDTH - 320, BOARD_SIZE + 55, 100, 30)
        self.draw_button("Change Theme", WIDTH - 200, BOARD_SIZE + 15, 120, 30)
        self.draw_button("Flip Board", WIDTH - 200, BOARD_SIZE + 55, 120, 30)
        self.draw_button("Switch Color", WIDTH - 70, BOARD_SIZE + 15, 120, 30)

        # Theme menu
        if self.show_theme_menu:
            self.draw_theme_menu()

    def draw_button(self, text, x, y, w, h, hover=False):
        """Draw a button with text"""
        color = BUTTON_HOVER if hover else BUTTON_COLOR
        pygame.draw.rect(self.screen, color, (x, y, w, h))
        pygame.draw.rect(self.screen, BLACK, (x, y, w, h), 2)

        text_surf = self.font.render(text, True, TEXT_COLOR)
        self.screen.blit(text_surf, (x + w // 2 - text_surf.get_width() // 2,
                                     y + h // 2 - text_surf.get_height() // 2))
        return pygame.Rect(x, y, w, h)

    def draw_theme_menu(self):
        """Draw the theme selection menu"""
        menu_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 300)
        pygame.draw.rect(self.screen, WHITE, menu_rect)
        pygame.draw.rect(self.screen, BLACK, menu_rect, 2)

        title = self.big_font.render("Select Theme", True, TEXT_COLOR)
        self.screen.blit(title, (menu_rect.x + menu_rect.width // 2 - title.get_width() // 2,
                                 menu_rect.y + 20))

        # Piece sets
        piece_label = self.font.render("Piece Sets:", True, TEXT_COLOR)
        self.screen.blit(piece_label, (menu_rect.x + 20, menu_rect.y + 60))

        for i, set_name in enumerate(self.piece_sets[:3]):  # Show first 3 sets
            btn_rect = pygame.Rect(menu_rect.x + 20 + i * 100, menu_rect.y + 90, 80, 30)
            hover = btn_rect.collidepoint(pygame.mouse.get_pos())
            self.draw_button(set_name.capitalize(), btn_rect.x, btn_rect.y,
                             btn_rect.width, btn_rect.height, hover)

        # Board themes
        board_label = self.font.render("Board Themes:", True, TEXT_COLOR)
        self.screen.blit(board_label, (menu_rect.x + 20, menu_rect.y + 140))

        theme_names = list(self.board_themes.keys())
        for i, theme_name in enumerate(theme_names[:4]):  # Show first 4 themes
            btn_rect = pygame.Rect(menu_rect.x + 20 + i * 70, menu_rect.y + 170, 60, 30)
            hover = btn_rect.collidepoint(pygame.mouse.get_pos())

            # Show color preview
            theme = self.board_themes[theme_name]
            pygame.draw.rect(self.screen, theme["light"], (btn_rect.x + 5, btn_rect.y + 5, 20, 20))
            pygame.draw.rect(self.screen, theme["dark"], (btn_rect.x + 30, btn_rect.y + 5, 20, 20))
            pygame.draw.rect(self.screen, BLACK, btn_rect, 1)

            # Theme name
            name_text = self.font.render(theme_name, True, TEXT_COLOR)
            self.screen.blit(name_text, (btn_rect.x + btn_rect.width // 2 - name_text.get_width() // 2,
                                         btn_rect.y + 30))

        # Close button
        close_rect = pygame.Rect(menu_rect.x + menu_rect.width // 2 - 40,
                                 menu_rect.y + menu_rect.height - 50, 80, 30)
        hover = close_rect.collidepoint(pygame.mouse.get_pos())
        self.draw_button("Close", close_rect.x, close_rect.y,
                         close_rect.width, close_rect.height, hover)

    def handle_click(self, pos):
        """Handle mouse click events"""
        if self.show_theme_menu:
            self.handle_theme_menu_click(pos)
            return

        # Check if click is in the board area
        square = self.pos_to_square(pos)

        # Check if click is in the info panel
        if pos[1] >= BOARD_SIZE:
            self.handle_panel_click(pos)
            return

        # If game is over, ignore board clicks
        if self.game_over:
            return

        # If it's AI's turn, ignore clicks
        if self.board.turn != self.player_color:
            return

        # If no square is selected and the clicked square has a piece of the player's color
        if self.selected_square is None:
            if square is not None:
                piece = self.board.piece_at(square)
                if piece and piece.color == self.player_color:
                    self.selected_square = square
                    self.valid_moves = [move for move in self.board.legal_moves
                                        if move.from_square == square]
        else:
            # If a square is already selected, try to make a move
            for move in self.valid_moves:
                if move.to_square == square:
                    self.make_move(move)
                    break

            # Deselect if clicked on another piece of the same color
            piece = self.board.piece_at(square) if square is not None else None
            if piece and piece.color == self.player_color:
                self.selected_square = square
                self.valid_moves = [move for move in self.board.legal_moves
                                    if move.from_square == square]
            else:
                self.selected_square = None
                self.valid_moves = []

    def handle_panel_click(self, pos):
        """Handle clicks in the info panel"""
        x, y = pos

        # New Game button
        if (WIDTH - 320 <= x <= WIDTH - 220 and
                BOARD_SIZE + 15 <= y <= BOARD_SIZE + 45):
            self.new_game()

        # Undo Move button
        elif (WIDTH - 320 <= x <= WIDTH - 220 and
              BOARD_SIZE + 55 <= y <= BOARD_SIZE + 85):
            self.undo_move()

        # Change Theme button
        elif (WIDTH - 200 <= x <= WIDTH - 80 and
              BOARD_SIZE + 15 <= y <= BOARD_SIZE + 45):
            self.show_theme_menu = True

        # Flip Board button
        elif (WIDTH - 200 <= x <= WIDTH - 80 and
              BOARD_SIZE + 55 <= y <= BOARD_SIZE + 85):
            self.player_color = not self.player_color

        # Switch Color button
        elif (WIDTH - 70 <= x <= WIDTH + 50 and
              BOARD_SIZE + 15 <= y <= BOARD_SIZE + 45):
            self.player_color = not self.player_color
            if not self.game_over and self.board.turn != self.player_color:
                self.ai_move()

    def handle_theme_menu_click(self, pos):
        """Handle clicks in the theme menu"""
        menu_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 150, 300, 300)

        # Close button
        close_rect = pygame.Rect(menu_rect.x + menu_rect.width // 2 - 40,
                                 menu_rect.y + menu_rect.height - 50, 80, 30)
        if close_rect.collidepoint(pos):
            self.show_theme_menu = False
            return

        # Piece set buttons
        for i, set_name in enumerate(self.piece_sets[:3]):
            btn_rect = pygame.Rect(menu_rect.x + 20 + i * 100, menu_rect.y + 90, 80, 30)
            if btn_rect.collidepoint(pos):
                self.current_piece_set = set_name
                self.piece_images = self.load_piece_images()
                self.show_theme_menu = False
                return

        # Board theme buttons
        theme_names = list(self.board_themes.keys())
        for i, theme_name in enumerate(theme_names[:4]):
            btn_rect = pygame.Rect(menu_rect.x + 20 + i * 70, menu_rect.y + 170, 60, 30)
            if btn_rect.collidepoint(pos):
                self.current_board_theme = theme_name
                self.board_colors = self.get_board_colors()
                self.show_theme_menu = False
                return

    def make_move(self, move):
        """Make a move on the board"""
        self.board.push(move)
        self.selected_square = None
        self.valid_moves = []

        # Check if game is over
        self.game_over = self.board.is_game_over()

        # If it's now AI's turn and game isn't over, make AI move
        if not self.game_over and self.board.turn != self.player_color:
            self.ai_move()

    def ai_move(self):
        """Make the AI's move"""
        # Show thinking message
        self.draw()
        pygame.display.flip()

        # Get AI move
        start_time = time.time()
        move = self.ai.find_best_move(self.board)
        end_time = time.time()

        print(f"AI played {move} (thought for {end_time - start_time:.2f}s)")
        self.make_move(move)

    def new_game(self):
        """Start a new game"""
        self.board.reset()
        self.selected_square = None
        self.valid_moves = []
        self.game_over = False
        self.player_color = chess.WHITE

    def undo_move(self):
        """Undo the last move"""
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.game_over = False
            # If we undo AI's move, we need to undo player's move too
            if self.board.turn != self.player_color and len(self.board.move_stack) > 0:
                self.board.pop()

    def draw(self):
        """Draw the entire game"""
        self.screen.fill(WHITE)
        self.draw_board()
        self.draw_info_panel()

    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = ChessGUI()
    game.run()