import sys
import copy

import pygame
from stopit import ThreadingTimeout

from omok import Omok, OmokState
import user_agent
import ai_agent
from util import random_act

TIMEOUT = 5
HUMAN = True


def update(state: OmokState, omok_ui: Omok, x_pos, y_pos, auto_result=True):
    state.update(x_pos, y_pos)
    omok_ui.update(state)
    pygame.display.update()

    status = state.check_status()
    if status is not None:
        state.result_status = status
        omok_ui.show_result_banner(status)


def play_ai_vs_human(state: OmokState, omok_ui: Omok):
    while True:
        mouse_clicked = False
        pos = None
        do_action = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and hasattr(state, "result_status"):
                state.reset()
                pygame.draw.rect(omok_ui.game_screen, omok_ui.black,
                                 (0, 0, omok_ui.screen_width, 80))
                omok_ui.board_draw()
                omok_ui.title_msg()
                omok_ui.turn_msg(state.turn)
                pygame.display.update()
                del state.result_status
                break  # 루프 재시작

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    valid, pos = omok_ui.is_valid_click(state, mouse_pos)
                    mouse_clicked = valid

        # 게임이 끝났으면 더 이상 수를 두지 않음
        if hasattr(state, "result_status"):
            continue

        if state.turn == 1:  # AI
            with ThreadingTimeout(TIMEOUT) as context_manager:
                y_pos, x_pos = user_agent.act(copy.deepcopy(state))
            if context_manager.state == context_manager.TIMED_OUT:
                print("Timeout!")
                y_pos, x_pos = random_act(state)
            do_action = True

        elif state.turn == -1 and mouse_clicked and pos is not None:
            y_pos, x_pos = pos
            do_action = True

        if do_action:
            update(state, omok_ui, x_pos, y_pos)


def play_ai_vs_ai(state: OmokState, omok_ui: Omok):
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and hasattr(state, "result_status"):
                state.reset()
                omok_ui.board_draw()
                pygame.draw.rect(omok_ui.game_screen, omok_ui.black,
                                 (0, 0, omok_ui.screen_width, 80))
                omok_ui.title_msg()
                omok_ui.turn_msg(state.turn)
                pygame.display.update()
                del state.result_status
                continue

        if hasattr(state, "result_status"):
            continue

        with ThreadingTimeout(TIMEOUT) as context_manager:
            if state.turn == 1:
                y_pos, x_pos = user_agent.act(copy.deepcopy(state))
            elif state.turn == -1:
                y_pos, x_pos = ai_agent.act(copy.deepcopy(state))

        if context_manager.state == context_manager.TIMED_OUT:
            print("Timeout!")
            y_pos, x_pos = random_act(state)

        update(state, omok_ui, x_pos, y_pos)


if __name__ == '__main__':
    pygame.init()
    state = OmokState()

    omok_ui = Omok()
    omok_ui.board_draw()  # 오목 바둑판 그리기
    omok_ui.title_msg()  # 오목 타이틀 그리기
    omok_ui.turn_msg(state.turn)  # 오목 턴 메시지 띄우기
    pygame.display.update()

    if HUMAN:
        play_ai_vs_human(state, omok_ui)
    else:
        play_ai_vs_ai(state, omok_ui)
