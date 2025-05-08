import pygame
import numpy as np
import sys


class OmokState:
    def __init__(self, game_board=None, board_size=19, win_stones=5):
        self.game_board = game_board if game_board is not None else np.zeros(
            [board_size, board_size])
        self.board_size = board_size
        self.win_stones = win_stones
        self.num_stones = 0
        self.history = []
        self.turn = 1  # black turn: 1, white turn: -1

    def reset(self):
        self.game_board = np.zeros([self.board_size, self.board_size])
        self.num_stones = 0
        self.history = []
        self.turn = 1

    def check_status(self):
        if self.num_stones == self.board_size * self.board_size:
            return 3

        # 수평선 상에서 5개가 연속인 경우
        for row in range(self.board_size):
            for col in range(self.board_size - self.win_stones + 1):
                # 흑 승!
                if np.sum(self.game_board[row, col:col + self.win_stones]) == self.win_stones:
                    return 1
                # 백 승!
                if np.sum(self.game_board[row, col:col + self.win_stones]) == -self.win_stones:
                    return 2

        # 수직선 상에서 5개가 연속인 경우
        for row in range(self.board_size - self.win_stones + 1):
            for col in range(self.board_size):
                # 흑 승!
                if np.sum(self.game_board[row: row + self.win_stones, col]) == self.win_stones:
                    return 1
                # 백 승!
                if np.sum(self.game_board[row: row + self.win_stones, col]) == -self.win_stones:
                    return 2

        # 대각선 상에서 5개가 연속인 경우
        for row in range(self.board_size - self.win_stones + 1):
            for col in range(self.board_size - self.win_stones + 1):
                count_sum = 0
                for i in range(self.win_stones):
                    if self.game_board[row + i, col + i] == 1:
                        count_sum += 1
                    if self.game_board[row + i, col + i] == -1:
                        count_sum -= 1

                # 흑 승!
                if count_sum == self.win_stones:
                    return 1

                # 백 승!
                if count_sum == -self.win_stones:
                    return 2

        for row in range(self.win_stones - 1, self.board_size):
            for col in range(self.board_size - self.win_stones + 1):
                count_sum = 0
                for i in range(self.win_stones):
                    if self.game_board[row - i, col + i] == 1:
                        count_sum += 1
                    if self.game_board[row - i, col + i] == -1:
                        count_sum -= 1

                # 흑 승!
                if count_sum == self.win_stones:
                    return 1

                # 백 승!
                if count_sum == -self.win_stones:
                    return 2

    def is_valid_position(self, x_pos, y_pos):
        if x_pos == -1 or y_pos == -1:
            return False

        if self.game_board[y_pos, x_pos] == 1 or self.game_board[y_pos, x_pos] == -1:
            return False

        return True

    def update(self, x_pos, y_pos):
        self.game_board[y_pos, x_pos] = 1 if self.turn == 1 else -1
        self.history.append((x_pos, y_pos))
        self.turn *= -1  # reverse
        self.num_stones += 1


class Omok:
    def __init__(self, board_size=19):
        # self.screen_width, self.screen_height = 640, 780  # 게임화면 너비, 높이 설정
        self.screen_width, self.screen_height = 840, 980  # 게임화면 너비, 높이 설정

        self.side_margin = 20  # 옆 여백
        self.top_margin = 140  # 위 여백
        self.board_margin = 40  # 판 여백

        # 게임 화면 설정
        self.game_screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        self.board_size = board_size
        self.board_color = (220, 179, 92)
        # 판 사이즈
        self.grid_size = self.screen_width - 2 * \
            (self.board_margin + self.side_margin)

        # 초기 X, Y 칸 사이즈 설정
        self.X_coord = [self.side_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))
                        for i in range(self.board_size)]
        self.Y_coord = [self.top_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))
                        for i in range(self.board_size)]

        # 색 모음 (R, G, B)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def update(self, state):
        game_board = state.game_board
        # 바둑돌 표시
        for i in range(game_board.shape[0]):
            for j in range(game_board.shape[1]):
                if game_board[i, j] == 1:
                    pygame.draw.circle(
                        self.game_screen, self.black, (self.X_coord[j], self.Y_coord[i]), 15, 0)

                if game_board[i, j] == -1:
                    pygame.draw.circle(
                        self.game_screen, self.white, (self.X_coord[j], self.Y_coord[i]), 15, 0)

        self.turn_msg(state.turn)

    def board_draw(self):
        # 바둑판 그리기
        pygame.draw.rect(
            self.game_screen,
            self.board_color,
            pygame.Rect(self.side_margin, self.top_margin, self.screen_width - 2 * self.side_margin,
                        self.screen_width - 2 * self.side_margin)
        )

        # 수직선
        for i in range(self.board_size):
            pygame.draw.line(self.game_screen, self.black, (self.side_margin + self.board_margin,
                                                            self.top_margin + self.board_margin + i * int(
                                                                self.grid_size / (self.board_size - 1))), (
                self.screen_width - (self.side_margin + self.board_margin),
                self.top_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))),
                1)

        # 수평선
        for i in range(self.board_size):
            pygame.draw.line(self.game_screen, self.black, (
                self.side_margin + self.board_margin + i *
                int(self.grid_size / (self.board_size - 1)),
                self.top_margin + self.board_margin), (
                self.side_margin + self.board_margin + i *
                    int(self.grid_size / (self.board_size - 1)),
                self.top_margin + self.board_margin + self.grid_size), 1)

        # 가운데 점
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i in [3, 9, 15] and j in [3, 9, 15]:
                    pygame.draw.circle(self.game_screen, self.black, (
                        self.side_margin + self.board_margin + i *
                        int(self.grid_size / (self.board_size - 1)),
                        self.top_margin + self.board_margin + j * int(self.grid_size / (self.board_size - 1))), 5, 0)

    def is_valid_click(self, state, pos):
        x_pos, y_pos = -1, -1
        for i, x in enumerate(self.X_coord):
            if x - 20 < pos[0] < x + 20:
                x_pos = i

        for i, y in enumerate(self.Y_coord):
            if y - 20 < pos[1] < y + 20:
                y_pos = i

        valid_pos = state.is_valid_position(x_pos, y_pos)
        return valid_pos, (y_pos, x_pos)

    def title_msg(self):
        font = pygame.font.Font('freesansbold.ttf', 20)  # 글꼴
        title_surf = font.render('Omok', True, self.white)
        title_rect = title_surf.get_rect()
        title_rect.topleft = (30, 10)
        self.game_screen.blit(title_surf, title_rect)

    def turn_msg(self, turn):
        font = pygame.font.Font('freesansbold.ttf', 20)  # 글꼴
        # 검은돌 차례
        turn_surf = font.render("Black's Turn!" if turn ==
                                1 else "White's Turn!", True, self.white)
        turn_rect = turn_surf.get_rect()
        position = (30, 110) if turn == 1 else (self.screen_width - 175, 110)
        pygame.draw.rect(
            self.game_screen,
            self.black,
            pygame.Rect(position[0], position[1], 150, 30)
        )
        turn_rect.topleft = (self.screen_width - 175,
                             110) if turn == 1 else (30, 110)
        self.game_screen.blit(turn_surf, turn_rect)

    def show_result_banner(self, status):
        font_title = pygame.font.SysFont('malgungothic', 36)
        font_click = pygame.font.SysFont('malgungothic', 24)

        # ✅ 글자색은 항상 하얀색으로 고정
        text_color = self.white

        if status == 1:
            msg = "Black Win!"
        elif status == 2:
            msg = "White Win!"
        elif status == 3:
            msg = "DRAW!"
        else:
            return

        # 상단 영역 클리어
        pygame.draw.rect(self.game_screen, self.black,
                         (0, 0, self.screen_width, 80))

        # 메시지 출력
        msg_surf = font_title.render(msg, True, text_color)
        msg_rect = msg_surf.get_rect(center=(self.screen_width // 2, 20))
        self.game_screen.blit(msg_surf, msg_rect)

        click_surf = font_click.render(
            "Click anywhere to restart!", True, text_color)
        click_rect = click_surf.get_rect(center=(self.screen_width // 2, 55))
        self.game_screen.blit(click_surf, click_rect)

        pygame.display.update()
