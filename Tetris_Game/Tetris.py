# -*-coding:utf-8-*-
# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

from contextlib import nullcontext
import pygame
import operator

from mino import *
from random import *
from pygame.locals import *


# Define
block_size = 17  # Height, width of single block
width = 10  # Board에 가로로 들어갈 칸의 개수
height = 20  # Board에 세로로 들어갈 칸의 개수
framerate = 30  # Bigger -> Slower


total_time = 60  # 타임 어택 시간
speed_change = 2  # 레벨별 블록 하강 속도 상승 정도

board_width = 800  # 전체 창의 가로 길이
board_height = 450  # 전체 창의 세로 길이
board_rate = 0.5625  # 가로세로비율 16:9
max_level = 15
goal_achieve = 1
increase_level = 1
increase_goal = 5
levelup_img_width = 0.28
levelup_img_height = 0.1
increase_easy_speed = 0.6
increase_noraml_speed = 0.7
increase_hard_speed = 0.8
img_upload_delay = 400


min_width = 400
min_height = 225
mid_width = 1200

# 기본 볼륨
music_volume = 5
effect_volume = 5

mino_matrix_x = 4  # mino는 4*4 배열이어서 이를 for문에 사용
mino_matrix_y = 4  # mino는 4*4 배열이어서 이를 for문에 사용
board_x = 10
board_y = 20



pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE) 
pygame.time.set_timer(pygame.USEREVENT, 500)
pygame.display.set_caption("TETRIS")
icon = pygame.image.load('Tetris_Game/assets/vector/icon_tetris.png').convert_alpha()
pygame.display.set_icon(icon)

initialize = True  # Start Screen 에서 set_initial_values()로 초기화할지 여부를 boolean으로 저장


class ui_variables: #UI
    # Fonts
    font_path = "Tetris_Game/assets/fonts/a옛날사진관3.ttf"
    font_path_b = "Tetris_Game/assets/fonts/a옛날사진관3.ttf"
    font_path_i = "Tetris_Game/assets/fonts/a옛날사진관3.ttf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h3 = pygame.font.Font(font_path, 25)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    h2_i = pygame.font.Font(font_path_i, 30)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("Tetris_Game/assets/sounds/BGM1.wav")  # 음악 불러옴
    pygame.mixer.music.set_volume(0.5)  # 이 부분도 필요 없음, set_volume에 추가해야 함
    intro_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/intro.wav")
    fall_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_Fall.wav")
    break_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_Break.wav")
    click_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_ButtonUp.wav")  # 여기부터
    move_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound(
        "Tetris_Game/assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound(
        "Tetris_Game/assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound(
        "Tetris_Game/assets/sounds/SFX_SpecialLineClearTriple.wav")  # 여기까지는 기존코드
    tetris_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_SpecialTetris.wav")
    LevelUp_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_LevelUp.wav")
    GameOver_sound = pygame.mixer.Sound("Tetris_Game/assets/sounds/SFX_GameOver.wav")

    # 레벨업 이미지
    LevelUp_vector = pygame.image.load('Tetris_Game/assets/vector/Level_Up.png')

    # 피버 이미지
    fever_image = pygame.image.load("Tetris_Game/assets/images/fever.png")

    black = (10, 10, 10)  # rgb(10, 10, 10)
    black_pause = (0, 0, 0, 127)
    real_white = (255, 255, 255)  # rgb(255, 255, 255)
    white = (211, 211, 211)  # rgb(211, 211, 211) ##연회색
    grey_1 = (26, 26, 26)  # rgb(26, 26, 26)
    grey_2 = (35, 35, 35)  # rgb(35, 35, 35)
    grey_3 = (55, 55, 55)  # rgb(55, 55, 55)
    pinkpurple = (250, 165, 255)  # rgb(250, 165, 255) 핑크+보라#

    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z
    lightgreen = (192,237,112) # rgb(192,237,112) # +
    gold = (255,215,0) # rgb(255,215,0)
    brown = (139,69,19) # rgb(139,69,19)
    
    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, lightgreen, gold, brown, grey_3]
    cyan_image = 'Tetris_Game/assets/block_images/cyan.png'
    blue_image = 'Tetris_Game/assets/block_images/blue.png'
    orange_image = 'Tetris_Game/assets/block_images/orange.png'
    yellow_image = 'Tetris_Game/assets/block_images/yellow.png'
    green_image = 'Tetris_Game/assets/block_images/green.png'
    pink_image = 'Tetris_Game/assets/block_images/pink.png'
    red_image = 'Tetris_Game/assets/block_images/red.png'
    lightgreen_image = 'Tetris_Game/assets/block_images/lightgreen.png'
    gold_image = 'Tetris_Game/assets/block_images/gold.png'
    brown_image = 'Tetris_Game/assets/block_images/brown.png'
    ghost_image = 'Tetris_Game/assets/block_images/ghost.png'
    table_image = 'Tetris_Game/assets/block_images/background.png'
    linessent_image = 'Tetris_Game/assets/block_images/linessent.png'
    t_block = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
               lightgreen_image, gold_image, brown_image, ghost_image, linessent_image]
    t_block_1 = [table_image, cyan_image, blue_image, orange_image, yellow_image, green_image, pink_image, red_image,
                ghost_image, linessent_image]

# 각 이미지 주소
background_image = 'Tetris_Game/assets/images/mainpage_background.png'  # 메뉴화면(첫 화면) 배경
gamebackground_image = 'Tetris_Game/assets/images/background_nyc.png'  # 게임 배경화면 : 기본값 뉴욕
pause_board_image = 'Tetris_Game/assets/vector/pause_board.png'

fever_image = 'Tetris_Game/assets/vector/fever.png'

help_board_image = 'Tetris_Game/assets/vector/help_board.png'
select_mode_button_image = 'Tetris_Game/assets/vector/Mode.png'
clicked_select_mode_button_image = 'Tetris_Game/assets/vector/clicked_Mode.png'

setting_button_image = 'Tetris_Game/assets/vector/Setting.png'
clicked_setting_button_image = 'Tetris_Game/assets/vector/clicked_Setting.png'

pause_setting_button_image = 'Tetris_Game/assets/vector/pause_settings_button.png'
clicked_pause_setting_button_image = 'Tetris_Game/assets/vector/clicked_pause_settings_button.png'

score_board_button_image = 'Tetris_Game/assets/vector/Score.png'
clicked_score_board_button_image = 'Tetris_Game/assets/vector/clicked_Score.png'

quit_button_image = 'Tetris_Game/assets/vector/Quit.png'
clicked_quit_button_image = 'Tetris_Game/assets/vector/clicked_Quit.png'

resume_button_image = 'Tetris_Game/assets/vector/Resume.png'
clicked_resume_button_image = 'Tetris_Game/assets/vector/clicked_resume_button.png'

help_button_image = 'Tetris_Game/assets/vector/Help.png'
clicked_help_button_image = 'Tetris_Game/assets/vector/clicked_Help.png'

single_button_image = 'Tetris_Game/assets/vector/Single.png'
clicked_single_button_image = 'Tetris_Game/assets/vector/clicked_Single.png'

easy_button_image = 'Tetris_Game/assets/vector/easy.png'
clicked_easy_button_image = 'Tetris_Game/assets/vector/clicked_easy.png'

normal_button_image='Tetris_Game/assets/vector/normal.png'
clicked_normal_button_image='Tetris_Game/assets/vector/clicked_normal.png'

hard_button_image = 'Tetris_Game/assets/vector/Hard.png'
clicked_hard_button_image = 'Tetris_Game/assets/vector/clicked_Hard.png'

pvp_button_image = 'Tetris_Game/assets/vector/PvP.png'
clicked_pvp_button_image = 'Tetris_Game/assets/vector/clicked_PvP.png'


hard_training_button_image = 'Tetris_Game/assets/vector/hard_tutorial_button.png'
clicked_hard_training_button_image = 'Tetris_Game/assets/vector/clicked_hard_tutorial_button.png'


gameover_board_image = 'Tetris_Game/assets/vector/gameover_board.png'
hard_training_start_image = 'Tetris_Game/assets/images/hard_tutorial_menual.png'
multi_training_start_image = 'Tetris_Game/assets/images/multi_tutorial_menual.png'
setting_board_image = 'Tetris_Game/assets/vector/setting_board.png'
number_board = 'Tetris_Game/assets/vector/number_board.png'
mute_button_image = 'Tetris_Game/assets/vector/allmute_button.png'
clicked_mute_button_image = 'Tetris_Game/assets/vector/clicked_allmute_button.png'

background1_image = 'Tetris_Game/assets/images/background_hongkong.png'
background2_image = 'Tetris_Game/assets/images/background_nyc.png'
background3_image = 'Tetris_Game/assets/images/background_uk.png'

clicked_background1_image = 'Tetris_Game/assets/images/clicked_background_hongkong.png'
clicked_background2_image = 'Tetris_Game/assets/images/clicked_background_nyc.png'
clicked_background3_image = 'Tetris_Game/assets/images/clicked_background_uk.png'

size1_image = 'Tetris_Game/assets/images/small.png'
size2_image = 'Tetris_Game/assets/images/medium.png'
size3_image = 'Tetris_Game/assets/images/big.png'

mute_button_image = 'Tetris_Game/assets/vector/allmute_button.png'
default_button_image = 'Tetris_Game/assets/vector/default_button.png'
clicked_default_button_image = 'Tetris_Game/assets/vector/clicked_default_button.png'
number_board = 'Tetris_Game/assets/vector/number_board.png'

# img 수정
resume_button_image = 'Tetris_Game/assets/vector/Resume.png'
clicked_resume_button_image = 'Tetris_Game/assets/vector/clicked_Resume.png'
restart_button_image = 'Tetris_Game/assets/vector/Restart.png'
clicked_restart_button_image = 'Tetris_Game/assets/vector/clicked_Restart.png'

back_button_image = 'Tetris_Game/assets/vector/Back.png'
clicked_back_button_image = 'Tetris_Game/assets/vector/clicked_Back.png'
volume_vector = 'Tetris_Game/assets/vector/volume_vector.png'
clicked_volume_vector = 'Tetris_Game/assets/vector/clicked_volume_vector.png'
keyboard_vector = 'Tetris_Game/assets/vector/keyboard_vector.png'
clicked_keyboard_vector = 'Tetris_Game/assets/vector/clicked_keyboard_vector.png'
screen_vector = 'Tetris_Game/assets/vector/screen_vector.png'
clicked_screen_vector = 'Tetris_Game/assets/vector/clicked_screen_vector.png'
size_vector = 'Tetris_Game/assets/vector/size_vector.png'
clicked_size_vector = 'Tetris_Game/assets/vector/clicked_size_vector.png'
menu_button_image = 'Tetris_Game/assets/vector/Menu.png'
clicked_menu_button_image = 'Tetris_Game/assets/vector/clicked_Menu.png'
ok_button_image = 'Tetris_Game/assets/vector/Ok.png'
clicked_ok_button_image = 'Tetris_Game/assets/vector/clicked_Ok.png'
plus_button_image = 'Tetris_Game/assets/vector/plus_button.png'
clicked_plus_button_image = 'Tetris_Game/assets/vector/clicked_plus_button.png'
minus_button_image = 'Tetris_Game/assets/vector/minus_button.png'
clicked_minus_button_image = 'Tetris_Game/assets/vector/clicked_minus_button.png'

backgroundmusic_select_image = 'Tetris_Game/assets/vector/backgroundmusic_select.png'
clicked_backgroundmusic_select_image = 'Tetris_Game/assets/vector/clicked_backgroundmusic_select.png'
sound_off_button_image = 'Tetris_Game/assets/vector/sound_off_button.png'
sound_on_button_image = 'Tetris_Game/assets/vector/sound_on_button.png'
check_button_image = 'Tetris_Game/assets/vector/checkbox_button.png'
clicked_check_button_image = 'Tetris_Game/assets/vector/clicked_checkbox_button.png'


pvp_win_image = 'Tetris_Game/assets/vector/pvp_win.png'
pvp_lose_image = 'Tetris_Game/assets/vector/pvp_lose.png'
leaderboard_vector = 'Tetris_Game/assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'Tetris_Game/assets/vector/clicked_leaderboard_vector.png'
multi_win_image = 'Tetris_Game/assets/vector/multi_win.png'
multi_lose_image = 'Tetris_Game/assets/vector/multi_lose.png'
multi_game_over = 'Tetris_Game/assets/vector/multi_game_over.png'

leaderboard_vector = 'Tetris_Game/assets/vector/leaderboard_vector.png'
clicked_leaderboard_vector = 'Tetris_Game/assets/vector/clicked_leaderboard_vector.png'
scoreboard_board_image = 'Tetris_Game/assets/vector/score_board.png'

multi_gameover_image = 'Tetris_Game/assets/vector/multi_game_over.png'
multi_win_image = 'Tetris_Game/assets/vector/multi_win.png'
multi_lose_image = 'Tetris_Game/assets/vector/multi_lose.png'

multi_key_reverse_image = 'Tetris_Game/assets/vector/key_reverse.png'
hard_speed_up_image = 'Tetris_Game/assets/vector/speed_up.png'
hard_flipped_image = 'Tetris_Game/assets/vector/flipped.png'

multi_1P_break_image = 'Tetris_Game/assets/images/multi_1p_break.png'
multi_2P_break_image = 'Tetris_Game/assets/images/multi_2p_break.png'
training_box_image = 'Tetris_Game/assets/vector/box.png'

line_message_multi_break_image = 'Tetris_Game/assets/vector/line_message_multi_tutorial_break.png'
line_message_multi_win_image = 'Tetris_Game/assets/vector/line_message_multi_tutorial_win.png'

training_completed_image = 'Tetris_Game/assets/images/training_completed.png'
training_incomplete_image = 'Tetris_Game/assets/images/training_incomplete.png'

# 트레이닝모드 중간 이벤트 발생 시 나오는 설명 이미지
hard_3line_image = 'Tetris_Game/assets/images/hard_3line.png'  # 하드트레이닝 3줄 제거시 등장
hard_10s_image = 'Tetris_Game/assets/images/hard_10s.png'  # 하드트레이닝 10초 경과시 등장
hard_line_message = 'Tetris_Game/assets/vector/line_message_hard_tutorial.png'  # 하드트레이닝 시작하자마자 메시지 등장


class button():  # 버튼객체
    def __init__(self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img=''):  # 버튼생성
        self.x = board_width * x_rate  # 버튼 x좌표 (버튼이미지의 정중앙)
        self.y = board_height * y_rate  # 버튼 y좌표 (버튼이미지의 정중앙)
        self.width = int(board_width * width_rate)  # 버튼 너비
        self.height = int(board_height * height_rate)  # 버튼 높이
        self.x_rate = x_rate  # board_width * x_rate = x좌표
        self.y_rate = y_rate  # board_height * y_rate = y좌표
        self.width_rate = width_rate  # board_width * width_rate = 버튼 너비
        self.height_rate = height_rate  # board_height * height_rate = 버튼 높이
        self.image = img  # 불러올 버튼 이미지

    def change(self, board_width, board_height):  # 버튼 위치, 크기 바꾸기
        self.x = board_width * self.x_rate  # x좌표
        self.y = board_height * self.y_rate  # y좌표
        self.width = int(board_width * self.width_rate)  # 너비
        self.height = int(board_height * self.height_rate)  # 높이

    def draw(self, win, outline=None):  # 버튼 보이게 만들기

        if outline:
            draw_image(screen, self.image, self.x, self.y, self.width, self.height)

    # 마우스의 위치가 버튼이미지 위에 있는지 확인  (pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표)
    def isOver(self, pos):

        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            if pos[1] > self.y - (self.height / 2) and pos[1] < self.y + (self.height / 2):
                return True
        return False

    def isOver_2(self, pos):  # start 화면에서 single,pvp,help,setting을 위해서 y좌표 좁게 인식하도록

        if pos[0] > self.x - (self.width / 2) and pos[0] < self.x + (self.width / 2):
            # 243줄에서의 2을 4로 바꿔주면서 좁게 인식할수 있도록함. 더 좁게 인식하고 싶으면 숫자 늘려주기#
            if pos[1] > self.y - (self.height / 4) and pos[1] < self.y + (self.height / 4):
                return True
        return False
# 메뉴 버튼

# (self, board_width, board_height, x_rate, y_rate, width_rate, height_rate, img='')
# (self, board_width, board_height,   0.2,   0.2,     0.22,        0.2,      img='')


select_mode_button = button(board_width, board_height, 0.125, 0.4, 0.22, 0.2, select_mode_button_image)
setting_button = button(board_width, board_height, 0.375,0.4, 0.22, 0.2, setting_button_image)
quit_button = button(board_width, board_height, 0.625,0.4, 0.22, 0.2, quit_button_image)
score_board_button = button(board_width, board_height, 0.875, 0.4, 0.22, 0.2, score_board_button_image)

single_button = button(board_width, board_height, 0.35, 0.35, 0.22, 0.2, single_button_image)
pvp_button = button(board_width, board_height, 0.65,0.35, 0.22, 0.2, pvp_button_image)

easy_button = button(board_width, board_height, 0.25,0.35, 0.22, 0.2, easy_button_image)
normal_button = button(board_width, board_height, 0.5, 0.35, 0.22 , 0.2, normal_button_image)
hard_button = button(board_width, board_height, 0.75,0.35, 0.22, 0.2, hard_button_image)
pvp_button = button(board_width, board_height, 0.65,0.35, 0.22, 0.2, pvp_button_image)

resume_button = button(board_width, board_height, 0.5,0.23, 0.17, 0.2, resume_button_image)
menu_button2 = button(board_width, board_height, 0.5,0.43, 0.17, 0.2, menu_button_image)
help_button = button(board_width, board_height, 0.5,0.63, 0.17, 0.2, help_button_image)
training_help_button = button(board_width, board_height, 0.68,0.6, 0.17, 0.2, help_button_image)

pause_quit_button = button(board_width, board_height,0.5, 0.83, 0.17, 0.2, quit_button_image)
pause_setting_button = button(board_width, board_height, 0.5, 0.63, 0.17, 0.2, pause_setting_button_image)

leaderboard_icon = button(board_width, board_height,0.77, 0.85, 0.15, 0.2, leaderboard_vector)
mute_button = button(board_width, board_height, 0.5,0.20, 0.15, 0.2, mute_button_image)
default_button = button(board_width, board_height, 0.5,0.27, 0.15, 0.2, default_button_image)


restart_button = button(board_width, board_height, 0.5,0.23, 0.17, 0.2, restart_button_image)
back_button = button(board_width, board_height, 0.5,0.85, 0.1, 0.12, back_button_image)
back_button2 = button(board_width, board_height, 0.2,0.85, 0.1, 0.12, back_button_image)
ok_button = button(board_width, board_height, 0.5,0.83, 0.15, 0.2, ok_button_image)

# 멀티모드 게임오버화면 버튼
multi_menu_button = button(board_width, board_height,0.35, 0.8, 0.2, 0.2, menu_button_image)
multi_restart_button = button(board_width, board_height, 0.65, 0.8, 0.2, 0.2, restart_button_image)
# 트레이닝 게임오버 화면 버튼
training_restart_button = button(board_width, board_height, 0.35, 0.8, 0.2, 0.2, restart_button_image)
training_multi_start_button = button(board_width, board_height, 0.65, 0.8, 0.2, 0.2, pvp_button_image)
training_hard_start_button = button(board_width, board_height, 0.65, 0.8, 0.2, 0.2, hard_button_image)


effect_plus_button = button(board_width, board_height, 0.27, 0.73, 0.0625, 0.1111, plus_button_image)
effect_minus_button = button(board_width, board_height, 0.42, 0.73, 0.0625, 0.1111, minus_button_image)

sound_plus_button = button(board_width, board_height,0.27, 0.53, 0.0625, 0.1111, plus_button_image)
sound_minus_button = button(board_width, board_height, 0.42, 0.53, 0.0625, 0.1111, minus_button_image)


mute_check_button = button(board_width, board_height,0.2, 0.4, 0.0625, 0.1111, check_button_image)

background1_check_button = button(board_width, board_height, 0.5, 0.25, 0.1875, 0.1444, background1_image)  # hongkong
background2_check_button = button(board_width, board_height, 0.5, 0.45, 0.1875, 0.1444, clicked_background2_image)  # nyc (default background)
background3_check_button = button(board_width, board_height, 0.5, 0.65, 0.1875, 0.1444, background3_image)  # uk

size1_check_button = button(board_width, board_height, 0.3, 0.5, 0.1875, 0.1444, size1_image)
size2_check_button = button(board_width, board_height, 0.51, 0.5, 0.1875, 0.1444, size2_image)
size3_check_button = button(board_width, board_height, 0.7, 0.5, 0.1875, 0.1444, size3_image)

volume_icon = button(board_width, board_height, 0.3, 0.5, 0.12, 0.23, volume_vector)
screen_icon = button(board_width, board_height, 0.7, 0.5, 0.12, 0.23, screen_vector)
size_icon = button(board_width, board_height, 0.5, 0.5, 0.12, 0.23, size_vector)


#음소거 추가#
effect_sound_off_button = button(board_width, board_height, 0.55, 0.73, 0.08, 0.15, sound_off_button_image)
music_sound_off_button = button(board_width, board_height, 0.55, 0.53, 0.08, 0.15, sound_off_button_image)
effect_sound_on_button = button(board_width, board_height, 0.55, 0.73, 0.08, 0.15, sound_on_button_image)
music_sound_on_button = button(board_width, board_height, 0.55, 0.53, 0.08, 0.15, sound_on_button_image)

#BGM 선택 추가#
BGM1_sound_on_button = button(board_width, board_height, 0.67, 0.43, 0.08, 0.15, clicked_backgroundmusic_select_image)  # default bgm: BGM1
BGM2_sound_on_button = button(board_width, board_height, 0.67, 0.63, 0.08, 0.15, backgroundmusic_select_image)
BGM3_sound_on_button = button(board_width, board_height, 0.67, 0.83, 0.08, 0.15, backgroundmusic_select_image)

# 선택된 BGM
selected_bgm = "Tetris_Game/assets/sounds/BGM1.wav"


# 게임 중 버튼 생성하기위한 버튼객체 리스트 (버튼 전체)

button_list = [
    select_mode_button, setting_button, quit_button, score_board_button, single_button, easy_button, normal_button, hard_button, pvp_button,
    resume_button, menu_button2, help_button, pause_quit_button, pause_setting_button,
    leaderboard_icon, mute_button, default_button, restart_button, back_button, ok_button, effect_plus_button, effect_minus_button,  size1_check_button, size2_check_button, size3_check_button, 
    sound_plus_button, sound_minus_button, mute_check_button, background1_check_button, background2_check_button, background3_check_button,
    volume_icon, screen_icon, size_icon, effect_sound_off_button, music_sound_off_button, effect_sound_on_button, music_sound_on_button,
    BGM1_sound_on_button, BGM2_sound_on_button, BGM3_sound_on_button, multi_restart_button, multi_menu_button, back_button2, training_restart_button, training_multi_start_button, training_hard_start_button]


def set_volume():
    # set_volume의 argument는 0.0~1.0으로 이루어져야하기 때문에 소수로 만들어주기 위해 10으로 나눔#
    ui_variables.fall_sound.set_volume(effect_volume / 10)
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.break_sound.set_volume(effect_volume / 10)
    ui_variables.move_sound.set_volume(effect_volume / 10)
    ui_variables.drop_sound.set_volume(effect_volume / 10)
    ui_variables.single_sound.set_volume(effect_volume / 10)
    ui_variables.double_sound.set_volume(effect_volume / 10)
    ui_variables.triple_sound.set_volume(effect_volume / 10)
    ui_variables.tetris_sound.set_volume(effect_volume / 10)
    ui_variables.LevelUp_sound.set_volume(effect_volume / 10)
    ui_variables.GameOver_sound.set_volume(music_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    pygame.mixer.music.set_volume(music_volume / 10)


# 이미지 화면에 띄우기 (매개변수 x, y가 이미지의 정중앙 좌표)
def draw_image(window, img_path, x, y, width, height):
    x = x - (width / 2)  # 해당 이미지의 가운데 x좌표, 가운데 좌표이기 때문에 2로 나눔
    y = y - (height / 2)  # 해당 이미지의 가운데 y좌표, 가운데 좌표이기 때문에 2로 나눔
    image = pygame.image.load(img_path)
    image = pygame.transform.smoothscale(image.convert_alpha(), (width, height))
    window.blit(image, (x, y))

# Draw block


def draw_block(x, y, color):
    # 사각형 내부 색 color로 지정
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    # 사각형 테두리
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_block_image(x, y, image):
    # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_image(screen, image, x, y, block_size, block_size)

# Draw game screen
def draw_board(next1, next2, hold, score, level, goal):
    # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)
    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양
    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(
        str(level), 1, ui_variables.real_white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.real_white)
    text_fever = ui_variables.h5.render("NEXT FEVER", 1, ui_variables.real_white)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_goal, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8400)))
    screen.blit(goal_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))
    screen.blit(text_fever, (int(board_width * 0.12) + 
                sidebar_width, int(board_height * 0.8395)))
    screen.blit(next_fever_value, (int(board_width * 0.13) + 
                sidebar_width, int(board_height * 0.8823)))

    # Draw board
    # 테트리스 블록이 들어갈 공간? 그리기 ..맞나?
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])

def draw1_board(next1, next2, hold, score, level, goal):
    # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)
    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block_1[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block_1[grid_n2[i][j]])

    
    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양
    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block_1[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(
        str(level), 1, ui_variables.real_white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.real_white)
    text_fever = ui_variables.h5.render("NEXT FEVER", 1, ui_variables.real_white)
    next_fever_value = ui_variables.h4.render(str(next_fever), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_goal, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8400)))
    screen.blit(goal_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))
    screen.blit(text_fever, (int(board_width * 0.12) + 
                sidebar_width, int(board_height * 0.8395)))
    screen.blit(next_fever_value, (int(board_width * 0.13) + 
                sidebar_width, int(board_height * 0.8823)))            

    # Draw board
    # 테트리스 블록이 들어갈 공간? 그리기 ..맞나?
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            draw_block_image(dx, dy, ui_variables.t_block_1[matrix[x][y + 1]])



# hard mode draw board change
# 블록 뒤집기 코드~
def draw_hardboard_change(next1, next2, hold, score, level, goal):
  # 크기 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.5312)

    # screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.2375), board_height)  # 크기 비율 고정
    )

    # Draw 2 next minos
    grid_n1 = tetrimino.mino_map[next1 - 1][0]
    grid_n2 = tetrimino.mino_map[next2 - 1][0]

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx1 = int(board_width * 0.025) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로 길이에서 원하는 비율을 곱해줌
            dy1 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로 길이에서 원하는 비율을 곱해줌#
            if grid_n1[i][j] != 0:
                draw_block_image(dx1, dy1, ui_variables.t_block[grid_n1[i][j]])

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx2 = int(board_width * 0.145) + sidebar_width + \
                block_size * j  # 위치 비율 고정, 전체 board 가로길이에서 원하는 비율을 곱해줌#
            dy2 = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, 전체 board 세로길이에서 원하는 비율을 곱해줌#
            if grid_n2[i][j] != 0:
                draw_block_image(dx2, dy2, ui_variables.t_block[grid_n2[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # hold 존재X
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정
                dy = int(board_height * 0.1336) + block_size * i  # 위치 비율 고정
                if grid_h[i][j] != 0:  # 해당 부분에 블록이 존재하면
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 출력

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.real_white)
    score_value = ui_variables.h4.render(
        str(score), 1, ui_variables.real_white)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.real_white)
    level_value = ui_variables.h4.render(
        str(level), 1, ui_variables.real_white)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.real_white)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.real_white)

    # Place texts
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_score, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.5187)))
    screen.blit(score_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.5614)))
    screen.blit(text_level, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.6791)))
    screen.blit(level_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.7219)))
    screen.blit(text_goal, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.8400)))
    screen.blit(goal_value, (int(board_width * 0.055) +
                sidebar_width, int(board_height * 0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.25) + block_size * \
                x  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            # draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])
            draw_block_image(
                dx, dy, ui_variables.t_block[matrix[x][(height-1)-y+1]]) #<-- [y]값이 뒤집는 코드


def draw_1Pboard(next, hold, current_key):
    # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    sidebar_width = int(board_width * 0.31)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.1875),
             board_height)  # 크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  # (배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + \
                block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 그림

    # Draw texts
    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(combo_count), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h3.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h2.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h2.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(
            str(combo_count), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * \
                x  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(dx, dy, ui_variables.t_block[matrix[x][y + 1]])
            
def draw_1Pboard_change(next, hold, current_key):
    # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    sidebar_width = int(board_width * 0.31)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(sidebar_width, 0, int(board_width * 0.1875),
             board_height)  # 크기비율 고정, board 가로길이에 원하는 비율을 곱해줌#
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]  # (배열이라-1) 다음 블록의 원래 모양

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.045) + sidebar_width + \
                block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]  # (배열이라-1) 기본 모양

    if hold_mino != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치비율 고정, board 가로길이에 원하는 비율을 곱해줌#
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치비율 고정, board 세로길이에 원하는 비율을 곱해줌#
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])  # hold 블록 그림

    # Draw texts
    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(combo_count), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h3.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h3.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h3.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key:
            reverse_value = ui_variables.h2.render(
                "O", 1, ui_variables.real_white)
        elif not current_key:
            reverse_value = ui_variables.h2.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h3.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h2.render(
            str(combo_count), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board 가로길이, 세로길이에 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.05) + block_size * \
                x  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.055) + block_size * \
                y  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            draw_block_image(
                dx, dy, ui_variables.t_block[matrix[x][(height-1)-y+1]])


def draw_2Pboard(next, hold, current_key_2P):
    # 위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.82)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        # 크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + \
                block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])

    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(combo_count_2P), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h4.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h3.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h3.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(
            str(combo_count_2P), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate_2P), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x  # 위치비율 고정
            dy = int(board_height * 0.055) + block_size * y  # 위치비율 고정
            draw_block_image(dx, dy, ui_variables.t_block[matrix_2P[x][y + 1]])

def draw_2Pboard_change(next, hold, current_key_2P):
    # 위치 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌
    sidebar_width = int(board_width * 0.82)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        # 크기 비율 고정, , board의 가로길이에 원하는 비율을 곱해줌, Rect(x축, y축, 가로길이, 세로길이)#
        Rect(sidebar_width, 0, int(board_width * 0.1875), board_height)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(mino_matrix_y):  # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(mino_matrix_x):
            dx = int(board_width * 0.05) + sidebar_width + \
                block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
            dy = int(board_height * 0.3743) + block_size * \
                i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
            if grid_n[i][j] != 0:
                draw_block_image(dx, dy, ui_variables.t_block[grid_n[i][j]])

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino_2P != -1:  # 기본값이 -1. 즉 hold블록 존재할 떄
        for i in range(mino_matrix_y):
            for j in range(mino_matrix_x):
                dx = int(board_width * 0.045) + sidebar_width + \
                    block_size * j  # 위치 비율 고정, board의 가로길이에 원하는 비율을 곱해줌
                dy = int(board_height * 0.1336) + block_size * \
                    i  # 위치 비율 고정, board의 세로길이에 원하는 비율을 곱해줌
                if grid_h[i][j] != 0:
                    draw_block_image(
                        dx, dy, ui_variables.t_block[grid_h[i][j]])

    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래 코드의 숫자 1=안티에일리어싱 적용에 대한 코드
    if textsize == False:
        text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h5.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h5.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h4.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h4.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h4.render(
            str(combo_count_2P), 1, ui_variables.real_white)
    if textsize == True:
        text_hold = ui_variables.h4.render("HOLD", 1, ui_variables.real_white)
        text_next = ui_variables.h4.render("NEXT", 1, ui_variables.real_white)
        text_reverse = ui_variables.h4.render(
            "REVERSE", 1, ui_variables.real_white)
        if current_key_2P:
            reverse_value = ui_variables.h3.render(
                "O", 1, ui_variables.real_white)
        elif not current_key_2P:
            reverse_value = ui_variables.h3.render(
                "X", 1, ui_variables.real_white)
        text_combo = ui_variables.h4.render("COMBO", 1, ui_variables.real_white)
        combo_value = ui_variables.h3.render(
            str(combo_count_2P), 1, ui_variables.real_white)
    if debug:
        # speed를 알려주는 framerate(기본값 30. 빨라질 수록 숫자 작아짐)
        speed_value = ui_variables.h5.render(
            "SPEED : "+str(framerate_2P), 1, ui_variables.real_white)
        screen.blit(speed_value, (int(board_width * 0.045) + sidebar_width,
                    int(board_height * 0.015)))  # 각각 전체 board의 가로길이, 세로길이에 대해 원하는 비율을 곱해줌
    screen.blit(text_hold, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.0374)))
    screen.blit(text_next, (int(board_width * 0.045) +
                sidebar_width, int(board_height * 0.2780)))
    screen.blit(text_reverse, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.6791)))
    screen.blit(reverse_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.7219)))
    screen.blit(text_combo, (int(board_width*0.045) +
                sidebar_width, int(board_height*0.8395)))
    screen.blit(combo_value, (int(board_width*0.055) +
                sidebar_width, int(board_height*0.8823)))

    for x in range(width):
        for y in range(height):
            dx = int(board_width * 0.54) + block_size * x  # 위치비율 고정
            dy = int(board_height * 0.055) + block_size * y  # 위치비율 고정
            draw_block_image(
                dx, dy, ui_variables.t_block[matrix[x][(height-1)-y+1]])

#PvP board 생성
def draw_multiboard(next_1P, hold_1P, next_2P, hold_2P, current_key, current_key_2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, current_key)
    draw_2Pboard(next_2P, hold_2P, current_key_2P)
    
def draw_multiboard_1p_change(next_1P, hold_1P, next_2P, hold_2P, current_key, current_key_2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard_change(next_1P, hold_1P, current_key)
    draw_2Pboard(next_2P, hold_2P, current_key_2P)

def draw_multiboard_2p_change(next_1P, hold_1P, next_2P, hold_2P, current_key, current_key_2P):
    screen.fill(ui_variables.real_white)
    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
               0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
    draw_1Pboard(next_1P, hold_1P, current_key)
    draw_2Pboard_change(next_2P, hold_2P, current_key_2P)
    



# Draw a tetrimino
#테트리스 그리기
def draw_mino(x, y, mino, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    tx, ty = x, y
    # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
    while not is_bottom(tx, ty, mino, r, matrix):
        ty += 1  # 한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = 11  # 테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j]  # 해당 위치에 블록 만듦

#single 모드 블록 생성
def draw1_mino(x, y, mino_en, r, matrix):  # mino는 모양, r은 회전된 모양 중 하나
    grid = tetrimino.mino_map[mino_en - 1][r]  # grid : 출력할 테트리스

    tx, ty = x, y
    # 테트리스가 바닥에 존재하면 true -> not이니까 바닥에 없는 상태
    while not is_bottom(tx, ty, mino_en, r, matrix):
        ty += 1  # 한칸 밑으로 하강

    # Draw ghost
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[tx + j][ty + i] = 8  # 테트리스가 쌓일 위치에 8 이라는 ghost 만듦

    # Draw mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = grid[i][j]  # 해당 위치에 블록 만듦


# Erase a tetrimino
def erase_mino(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(board_y + 1):
        for i in range(board_x):
            if matrix[i][j] == 11:  # 테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  # 없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0  # 해당 위치에 블록 없애서 빈 곳으로 만들기

#single 모드
def erase1_mino(x, y, mino_en, r, matrix):
    grid = tetrimino.mino_map[mino_en - 1][r]

    # Erase ghost
    for j in range(board_y + 1):
        for i in range(board_x):
            if matrix[i][j] == 8:  # 테트리스 블록에서 해당 행렬위치에 ghost블록 존재하면
                matrix[i][j] = 0  # 없애서 빈 곳으로 만들기

    # Erase mino
    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                matrix[x + j][y + i] = 0  # 해당 위치에 블록 없애서 빈 곳으로 만들기


# Returns true if mino is at bottom
def is_bottom(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y:  # 바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 11:
                    return True

    return False

def is_bottom1(x, y, mino_en, r, matrix):
    grid = tetrimino.mino_map[mino_en - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (y + i + 1) > board_y:  # 바닥의 y좌표에 있음(바닥에 닿음)
                    return True
                # 그 블록위치에 0, 8 아님(즉 블록 존재 함)
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

#사이드 벽 충돌 코드?
# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  # 맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  # 그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_leftedge1(x, y, mino_en, r, matrix):
    grid = tetrimino.mino_map[mino_en - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j - 1) < 0:  # 맨 왼쪽에 위치함
                    return True
                elif matrix[x + j - 1][y + i] != 0:  # 그 위치의 왼쪽에 이미 무엇인가 존재함
                    return True

    return False

# Returns true if mino is at the right edge


def is_rightedge(x, y, mino, r, matrix):
    grid = tetrimino.mino_map[mino - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x:  # 맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:  # 그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False

def is_rightedge1(x, y, mino_en, r, matrix):
    grid = tetrimino.mino_map[mino_en - 1][r]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                if (x + j + 1) >= board_x:  # 맨 오른쪽에 위치
                    return True
                elif matrix[x + j + 1][y + i] != 0:  # 그 위치의 오른쪽에 이미 무엇인가 존재함
                    return True

    return False


def is_turnable_r(x, y, mino, r, matrix):
    if r != 3:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r + 1]  # 3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][0]  # 3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

def is_turnable_r1(x, y, mino_en, r, matrix):
    if r != 3:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino_en - 1][r + 1]  # 3이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino_en - 1][0]  # 3이면 0번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False
    return True

# Returns true if turning left is possible


def is_turnable_l(x, y, mino, r, matrix):
    if r != 0:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino - 1][r - 1]  # 0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino - 1][3]  # 0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

def is_turnable_l1(x, y, mino_en, r, matrix):
    if r != 0:  # 회전모양 총 0, 1, 2, 3번째 총 4가지 있음
        grid = tetrimino.mino_map[mino_en - 1][r - 1]  # 0이 아니면 그 다음 모양
    else:
        grid = tetrimino.mino_map[mino_en - 1][3]  # 0이면 3번째 모양으로

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            if grid[i][j] != 0:  # 테트리스 블록에서 해당 행렬위치에 블록 존재하면
                # 테트리스 matrix크기 벗어나면 못돌림
                if (x + j) < 0 or (x + j) >= board_x or (y + i) < 0 or (y + i) > board_y:
                    return False
                elif matrix[x + j][y + i] != 0:  # 해당 자리에 이미 블록이 있으면 못돌림
                    return False

    return True

# Returns true if new block is drawable


def is_stackable(mino, matrix):
    grid = tetrimino.mino_map[mino - 1][0]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

def is_stackable1(mino_en, matrix):
    grid = tetrimino.mino_map[mino_en - 1][0]  # grid : 출력할 테트리스

    for i in range(mino_matrix_y):
        for j in range(mino_matrix_x):
            
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True


#한줄 뿌시면 공격
def multi_reverse_key(rev, player):
    # 하드드롭-왼쪽회전, 소프트드롭-오른쪽회전, 오른쪽이동-왼쪽이동 방향키 전환
    keys_1P = {'hardDrop': K_e, 'softDrop': K_s, 'turnRight': K_w,
               'turnLeft': K_q, 'moveRight': K_d, 'moveLeft': K_a}
    keys_1P_reverse = {'hardDrop': K_q, 'softDrop': K_w, 'turnRight': K_s,
                       'turnLeft': K_e, 'moveRight': K_a, 'moveLeft': K_d}
    keys_2P = {'hardDrop': K_SPACE, 'softDrop': K_DOWN, 'turnRight': K_UP,
               'turnLeft': K_m, 'moveRight': K_RIGHT, 'moveLeft': K_LEFT}
    keys_2P_reverse = {'hardDrop': K_m, 'softDrop': K_UP, 'turnRight': K_DOWN,
                       'turnLeft': K_SPACE, 'moveRight': K_LEFT, 'moveLeft': K_RIGHT}

    if rev == False:
        if player == 1:
            return keys_1P
        elif player == 2:
            return keys_2P
    elif rev == True:
        if player == 1:
            return keys_1P_reverse
        elif player == 2:
            return keys_2P_reverse

def set_initial_values():
    global attack_point, attack_point_2P, combo_count, combo_count_2P, line_count, score, level, goal, next_fever, fever_score, fever_interval, max_score, fever, combo_fever, score_2P, level_2P, goal_2P, bottom_count, bottom_count_2P, hard_drop, hard_drop_2P, attack_point, attack_point_2P, dx, dy, dx_2P, dy_2P, rotation, rotation_2P, mino,mino_en, mino_2P, next_mino1,next_mino1_en, next_mino2,next_mino2_en, next_mino1_2P, hold, hold_2P, hold_mino, hold_mino_2P, framerate, framerate_2P, matrix, matrix_2P, Change_RATE, blink, start, pause, done, game_over, leader_board, setting, volume_setting, size_setting, screen_setting, pvp, help, gravity_mode, debug, d, e, b, u, g, start_ticks, textsize, CHANNELS, swidth, name_location, name, previous_time, current_time, pause_time, lines, leaders, leaders_hard, game_status, framerate_blockmove, framerate_2P_blockmove, game_speed, game_speed_2P, select_mode, single, normal, hard, hard_time_setting, winner, key1, key2, key_reverse, key_reverse_2P, current_key, current_key_2P, help_status, remaining_time

    framerate = 30  # Bigger -> Slower  기본 블록 하강 속도, 2도 할만 함, 0 또는 음수 이상이어야 함
    framerate_blockmove = framerate * 3  # 블록 이동 시 속도
    game_speed = framerate * 20  # 게임 기본 속도
    framerate_2P = 30  # 2P
    framerate_2P_blockmove = framerate_2P * 3  # 블록 이동 시 속도
    game_speed_2P = framerate_2P * 20  # 2P 게임 기본 속도

    help_status = False
    # Initial values
    blink = False
    start = False # easy mode
    pause = False
    done = False
    game_over = False
    leader_board = False
    setting = False
    volume_setting = False
    screen_setting = False
    size_setting = False
    single = False
    pvp = False
    hard = False  # 하드모드 변수 추가
    normal = False
    

    help = False
    select_mode = False
    gravity_mode = False  # 이 코드가 없으면 중력모드 게임을 했다가 Restart해서 일반모드로 갈때 중력모드로 게임이 진행됨#
    debug = False
    d = False
    e = False
    b = False
    u = False
    g = False
    hard_time_setting = False  # 하드모드 시작하였을 때 타임 세팅을 시작하여 경과 시간을 계산하기 위해 추가한 변수
    remaining_time = 60  # 하드모드 남은 시간
    winner = 0  # multi mode에서 1P가 이기면 1, 2P가 이기면 2 (기본값은 0)
    start_ticks = pygame.time.get_ticks()
    textsize = False
    
    # 게임 음악 속도 조절 관련 변수
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2

    fever_score = 500
    next_fever = 500
    fever_interval = 3
    max_score = 99999
    fever = 0

    combo_fever = 2

    line_count = 0
    score = 0
    level = 1
    goal = level * 5
    score_2P = 0
    level_2P = 1
    goal_2P = level_2P * 5
    bottom_count = 0
    bottom_count_2P = 0
    hard_drop = False
    hard_drop_2P = False
    attack_point = 0
    attack_point_2P = 0
    combo_count = 0
    combo_count_2P = 0
    key1 = {'hardDrop': K_e, 'softDrop': K_s, 'turnRight': K_w,
            'turnLeft': K_q, 'moveRight': K_d, 'moveLeft': K_a}
    key2 = {'hardDrop': K_SPACE, 'softDrop': K_DOWN, 'turnRight': K_UP,
            'turnLeft': K_m, 'moveRight': K_RIGHT, 'moveLeft': K_LEFT}
    key_reverse = False   # 상대가 몇 줄이든 줄(들)을 깼는지 체크 (조건 충족 체크)
    key_reverse_2P = False
    current_key = False    # 최근 키가 반전키였는지 정상키였는지 체크
    current_key_2P = False

    dx, dy = 3, 0  # Minos location status
    dx_2P, dy_2P = 3, 0
    rotation = 0  # Minos rotation status
    rotation_2P = 0
    mino = randint(1, 10)  # Current mino #테트리스 블록 7가지 중 하나
    mino_en = randint(1, 7)
    mino_2P = randint(1, 10)
    next_mino1 = randint(1, 10)  # Next mino1 # 다음 테트리스 블록 7가지 중 하나
    next_mino1_en = randint(1, 7)
    next_mino2 = randint(1, 10)  # Next mino2 # 다음 테트리스 블록 7가지 중 하나
    next_mino2_en = randint(1, 7)
    next_mino1_2P = randint(1, 10)
    hold = False  # Hold status
    hold_2P = False
    hold_mino = -1  # Holded mino #현재 hold하는 것 없는 상태
    hold_mino_2P = -1
    textsize = False

    name_location = 0
    name = [65, 65, 65]

    previous_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()

    # easy mode 스코어보드 leaders 배열에 저장
    with open('Tetris_Game/leaderboard.txt') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in open(
        'Tetris_Game/leaderboard.txt')]  # leaderboard.txt 한줄씩 읽어옴

    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

    # hard mode 스코어보드 leaders_hard 배열에 저장
    with open('Tetris_Game/leaderboard_hard.txt') as h:
        lines = h.readlines()
    lines = [line.rstrip('\n') for line in open(
        'Tetris_Game/leaderboard_hard.txt')]  # leaderboard.txt 한줄씩 읽어옴

    leaders_hard = {'AAA': 0, 'BBB': 0, 'CCC': 0}
    for i in lines:
        leaders_hard[i.split(' ')[0]] = int(i.split(' ')[1])
    leaders_hard = sorted(leaders_hard.items(),
                        key=operator.itemgetter(1), reverse=True)

    matrix = [[0 for y in range(height + 1)]
            for x in range(width)]  # Board matrix
    matrix_2P = [[0 for y in range(height + 1)]
                for x in range(width)]  # Board matrix

    pygame.mixer.init()
    ui_variables.click_sound.set_volume(effect_volume / 10)
    ui_variables.intro_sound.set_volume(music_volume / 10)
    ui_variables.break_sound.set_volume(
        effect_volume / 10)  # 소리 설정 부분도 set_volume 함수에 넣으면 됨

    game_status = ''
    pygame.mixer.music.load(selected_bgm)


set_initial_values()
pygame.time.set_timer(pygame.USEREVENT, 500)


###########################################################
# Loop Start
###########################################################

while not done:
    if board_width<=500:
        select_mode_button = button(board_width, board_height, 0.5, 0.125, 0.22, 0.2, select_mode_button_image)
        setting_button = button(board_width, board_height, 0.5,0.375, 0.22, 0.2, setting_button_image)
        quit_button = button(board_width, board_height, 0.5,0.625, 0.22, 0.2, quit_button_image)
        score_board_button = button(board_width, board_height, 0.5, 0.875, 0.22, 0.2, score_board_button_image)

        easy_button = button(board_width, board_height, 0.5,0.125, 0.22, 0.2, easy_button_image)
        normal_button = button(board_width, board_height, 0.5, 0.375, 0.22 , 0.2, normal_button_image)
        hard_button = button(board_width, board_height, 0.5,0.625, 0.22, 0.2, hard_button_image)
        
        single_button = button(board_width, board_height, 0.5, 0.25, 0.22, 0.2, single_button_image)
        pvp_button = button(board_width, board_height, 0.5,0.5, 0.22, 0.2, pvp_button_image)

        volume_icon = button(board_width, board_height, 0.5, 0.25, 0.06, 0.12, volume_vector)
        screen_icon = button(board_width, board_height, 0.5, 0.41, 0.06, 0.12, screen_vector)
        size_icon = button(board_width, board_height, 0.5, 0.6, 0.06, 0.12, size_vector)
    else:
        select_mode_button = button(board_width, board_height, 0.125, 0.4, 0.22, 0.2, select_mode_button_image)
        setting_button = button(board_width, board_height, 0.375,0.4, 0.22, 0.2, setting_button_image)
        quit_button = button(board_width, board_height, 0.625,0.4, 0.22, 0.2, quit_button_image)
        score_board_button = button(board_width, board_height, 0.875, 0.4, 0.22, 0.2, score_board_button_image)
        
        easy_button = button(board_width, board_height, 0.25,0.35, 0.22, 0.2, easy_button_image)
        normal_button = button(board_width, board_height, 0.5, 0.35, 0.22 , 0.2, normal_button_image)
        hard_button = button(board_width, board_height, 0.75,0.35, 0.22, 0.2, hard_button_image)

        single_button = button(board_width, board_height, 0.35, 0.35, 0.22, 0.2, single_button_image)
        pvp_button = button(board_width, board_height, 0.65,0.35, 0.22, 0.2, pvp_button_image)
        
        volume_icon = button(board_width, board_height, 0.3, 0.5, 0.12, 0.23, volume_vector)
        screen_icon = button(board_width, board_height, 0.7, 0.5, 0.12, 0.23, screen_vector)
        size_icon = button(board_width, board_height, 0.5, 0.5, 0.12, 0.23, size_vector)
    # 게임안에서 Pause 눌렀을 때 screen
    if pause:
        pygame.mixer.music.pause()
        
        if help_status == True:
            pause_surface = screen.convert_alpha()  # 투명 가능하도록
            pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
            pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

            draw_image(screen, help_board_image, board_width * 0.5, board_height * 0.5,
                       int(board_width * 0.8), int(board_height * 0.9))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            back_button2.draw(screen, (0, 0, 0))

        if help_status == False:
            draw_image(screen, pause_board_image, board_width * 0.5, board_height * 0.5,
                       int(board_height * 1), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
            resume_button.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색

            menu_button2.draw(screen, (0, 0, 0))
            help_button.draw(screen, (0, 0, 0))
            pause_quit_button.draw(screen, (0, 0, 0))

        pygame.display.update()

        for event in pygame.event.get(): #키보드, 마우스 입력값을 받음
            pos = pygame.mouse.get_pos() # 마우스의 포지션 x,y로 튜플로 반환
            if event.type == QUIT: 
                done = True

            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초


            # isOver() : 마우스의 위치가 버튼이미지 위에 있는지 확인  (pos[0]은 마우스 x좌표, pos[1]은 마우스 y좌표)
            elif event.type == pygame.MOUSEMOTION:    #마우스 움직일 때 발생함
                if back_button2.isOver(pos):
                    back_button2.image = clicked_back_button_image
                else:
                    back_button2.image = back_button_image
                pygame.display.update()
                if resume_button.isOver_2(pos):
                    resume_button.image = clicked_resume_button_image
                else:
                    resume_button.image = resume_button_image

                if menu_button2.isOver_2(pos):
                    menu_button2.image = clicked_menu_button_image
                else:
                    menu_button2.image = menu_button_image

                if help_button.isOver_2(pos):
                    help_button.image = clicked_help_button_image
                else:
                    help_button.image = help_button_image

                if pause_quit_button.isOver_2(pos):
                    pause_quit_button.image = clicked_quit_button_image
                else:
                    pause_quit_button.image = quit_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # help창 back버튼 클릭 시
                if back_button2.isOver(pos):
                    ui_variables.click_sound.play()
                    help_status = False
                    pause = True
                # pause창 quit 버튼 클릭 시
                if pause_quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True
                # pause창 help 버튼 클릭 시
                if help_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    help_status = True
                    #help = True
                    
                    #시작화면으로 나가는 버튼
                if menu_button2.isOver_2(pos):
                    ui_variables.click_sound.play()
                    pause = False
                    start = False
                    if pvp:
                        pvp = False
                    if hard:
                        hard = False
                    if normal:
                        normal = False
    

                if resume_button.isOver_2(pos):
                    pygame.mixer.music.unpause()
                    pause = False
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초
            
            # 계속 반복되는 코드 함수로 만들기~
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    F[i].change(board_width, board_height)
                pygame.display.update()

    # Game screen
    elif start:
        for event in pygame.event.get():
            attack_stack = 0
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino 5 * 10
                if board_height <= 450 and board_width <= 800:
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw1_board(next_mino1_en, next_mino2_en,
                           hold_mino, score, level, goal)
                #10*20
                elif board_height <= 675 and board_width <= 1200:
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                #15 * 30
                # elif 1600 900    
                
                
                # Erase a mino
                if not game_over:
                    erase1_mino(dx, dy, mino_en, rotation, matrix)

                # Move mino down
                if not is_bottom1(dx, dy, mino_en, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw1_mino(dx, dy, mino_en, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width *
                                   0.5, board_height * 0.5, board_width, board_height)
                        draw1_board(next_mino1_en, next_mino2_en,
                                hold_mino, score, level, goal)
                        pygame.display.update()
                        # 뭔 코드?
                        if is_stackable1(next_mino1_en, matrix):
                            mino_en = next_mino1_en
                            next_mino1_en = next_mino2_en
                            next_mino2_en = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_status = 'start'
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                combo_value = 0
                attack_stack = 0

                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        attack_stack += 1
                        k = j
                        combo_value += 1
                        
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]   # 남아있는 블록 한 줄씩 내리기(덮어쓰기)
                            k -= 1
                    
                while attack_stack >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix[i][j] = matrix[i][j + 1]

                            attack_stack -= 1
                    for i in range(10):
                        matrix[i][20] = 9
                    k = randint(0, 9)
                    matrix[k][20] = 0
                    attack_point += 1
                    attack_stack -= 1

                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < goal_achieve and level < max_level:
                    level += increase_level
                    goal += level * increase_goal
                    # blit(이미지, 위치)
                    screen.blit(ui_variables.LevelUp_vector,
                                (board_width * levelup_img_width, board_height * levelup_img_height))
                    pygame.display.update()
                    pygame.time.delay(img_upload_delay)  # 0.4초
                    if level <= max_level:
                        pygame.time.set_timer(pygame.USEREVENT, (500 - 50 * (level-increase_level)))
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, 100)
                
                # 점수 구간에 따른 피버타임 #fever_interval=3
                for i in range(1, max_score, fever_interval):
                    if score > i * fever_score and score < (i + 1) * fever_score:  # 500~1000,2000~2500.3500~4000
                        mino = randint(1, 1)
                        next_mino1_en = randint(1, 1)
                        next_mino2_en = randint(1, 1)
                        next_fever = (i + fever_interval) * fever_score
                        if erase_count == 1:
                            ui_variables.single_sound.play()
                            score += 100 * level
                        elif erase_count == 2:
                            ui_variables.double_sound.play()
                            score += 300 * level
                        elif erase_count == 3:
                            ui_variables.triple_sound.play()
                            score += 700 * level
                        elif erase_count == 4:
                            ui_variables.tetris_sound.play()
                            score += 2000 * level
                        # fever time시 이미지 깜빡거리게
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.fever_image,
                                                               (int(board_width * 0.3), int(board_height * 0.2))),
                                        (board_width * 0.01, board_height * 0.1))
                            blink = False
                        else:
                            blink = True
                

            elif event.type == KEYDOWN:
                erase1_mino(dx, dy, mino_en, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    ui_variables.drop_sound.play()
                    while not is_bottom1(dx, dy, mino_en, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino_en
                            mino_en = next_mino1_en
                            next_mino1_en = next_mino2_en
                            next_mino2_en = randint(1, 7)
                        else:
                            hold_mino, mino_en = mino_en, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r1(dx, dy - 1, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r1(dx + 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r1(dx - 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r1(dx, dy - 2, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r1(dx + 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r1(dx - 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l1(dx, dy - 1, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l1(dx + 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l1(dx - 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l1(dx, dy - 2, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l1(dx + 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l1(dx - 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()
        
    elif normal:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw1_mino(dx, dy, mino_en, rotation, matrix)
                draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                draw1_board(next_mino1_en, next_mino2_en,
                           hold_mino, score, level, goal)

                # Erase a mino
                if not game_over:
                    erase1_mino(dx, dy, mino_en, rotation, matrix)

                # Move mino down
                if not is_bottom1(dx, dy, mino_en, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw1_mino(dx, dy, mino_en, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width *
                                   0.5, board_height * 0.5, board_width, board_height)
                        draw1_board(next_mino1_en, next_mino2_en,
                                hold_mino, score, level, goal)
                        pygame.display.update()
                        # 뭔 코드?
                        if is_stackable1(next_mino1_en, matrix):
                            mino_en = next_mino1_en
                            next_mino1_en = next_mino2_en
                            next_mino2_en = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_status = 'start'
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < goal_achieve and level < max_level:
                    level += increase_level
                    goal += level * increase_goal
                    # blit(이미지, 위치)
                    screen.blit(ui_variables.LevelUp_vector,
                                (board_width * levelup_img_width, board_height * levelup_img_height))
                    pygame.display.update()
                    pygame.time.delay(img_upload_delay)  # 0.4초
                    framerate = int(framerate * increase_noraml_speed)

                # 점수 구간에 따른 피버타임 #fever_interval=3
                for i in range(1, max_score, fever_interval):
                    if score > i * fever_score and score < (i + 1) * fever_score:  # 500~1000,2000~2500.3500~4000
                        mino = randint(1, 1)
                        next_mino1_en = randint(1, 1)
                        next_mino2_en = randint(1, 1)
                        next_fever = (i + fever_interval) * fever_score
                        if erase_count == 1:
                            ui_variables.single_sound.play()
                            score += 100 * level
                        elif erase_count == 2:
                            ui_variables.double_sound.play()
                            score += 300 * level
                        elif erase_count == 3:
                            ui_variables.triple_sound.play()
                            score += 700 * level
                        elif erase_count == 4:
                            ui_variables.tetris_sound.play()
                            score += 2000 * level
                        # fever time시 이미지 깜빡거리게
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.fever_image,
                                                               (int(board_width * 0.3), int(board_height * 0.2))),
                                        (board_width * 0.01, board_height * 0.1))
                            blink = False
                        else:
                            blink = True    

            elif event.type == KEYDOWN:
                erase1_mino(dx, dy, mino_en, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom1(dx, dy, mino_en, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino_en
                            mino_en = next_mino1_en
                            next_mino1_en = next_mino2_en
                            next_mino2_en = randint(1, 7)
                        else:
                            hold_mino, mino_en = mino_en, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r1(dx, dy - 1, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r1(dx + 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r1(dx - 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r1(dx, dy - 2, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r1(dx + 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r1(dx - 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l1(dx, dy - 1, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l1(dx + 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l1(dx - 1, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l1(dx, dy - 2, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l1(dx + 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l1(dx - 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge1(dx, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw1_mino(dx, dy, mino_en, rotation, matrix)
                    draw1_board(next_mino1_en, next_mino2_en,
                            hold_mino, score, level, goal)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()

    elif hard:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            change = line_count // 3   # board_change 변수 --> 향후 상수 파일로 작성
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, game_speed)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                           0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                # draw_board(next_mino1, next_mino2,
                #            hold_mino, score, level, goal)
                if change % 2 == 1:
                    draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                else:
                    draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                    pygame.display.update()
                    
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation, matrix)
                        screen.fill(ui_variables.real_white)
                        draw_image(screen, gamebackground_image, board_width *
                                   0.5, board_height * 0.5, board_width, board_height)
                        
                        if change % 2 == 1:
                            draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                        else:
                            draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                            pygame.display.update()
                            
                        # 뭔 코드?
                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 10)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_status = 'start'
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        line_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    ui_variables.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    ui_variables.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    ui_variables.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    ui_variables.tetris_sound.play()
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < goal_achieve and level < max_level:
                    level += increase_level
                    goal += level * increase_goal
                    # blit(이미지, 위치)
                    screen.blit(ui_variables.LevelUp_vector,
                                (board_width * levelup_img_width, board_height * levelup_img_height))
                    pygame.display.update()
                    pygame.time.delay(img_upload_delay)  # 0.4초
                    framerate = int(framerate * increase_hard_speed)

                # 점수 구간에 따른 피버타임 #fever_interval=3
                for i in range(1, max_score, fever_interval):
                    if score > i * fever_score and score < (i + 1) * fever_score:  # 500~1000,2000~2500.3500~4000
                        mino = randint(1, 1)
                        next_mino1_en = randint(1, 1)
                        next_mino2_en = randint(1, 1)
                        next_fever = (i + fever_interval) * fever_score
                        if erase_count == 1:
                            ui_variables.single_sound.play()
                            score += 100 * level
                        elif erase_count == 2:
                            ui_variables.double_sound.play()
                            score += 300 * level
                        elif erase_count == 3:
                            ui_variables.triple_sound.play()
                            score += 700 * level
                        elif erase_count == 4:
                            ui_variables.tetris_sound.play()
                            score += 2000 * level
                        # fever time시 이미지 깜빡거리게
                        if blink:
                            screen.blit(pygame.transform.scale(ui_variables.fever_image,
                                                               (int(board_width * 0.3), int(board_height * 0.2))),
                                        (board_width * 0.01, board_height * 0.1))
                            blink = False
                        else:
                            blink = True

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                # Hold
                elif event.key == K_LSHIFT or event.key == K_c:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = next_mino2
                            next_mino2 = randint(1, 10)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                # Turn right
                elif event.key == K_UP or event.key == K_x:
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino_en, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                # Move left
                elif event.key == K_LEFT:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()
                # Move right
                elif event.key == K_RIGHT:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_board(next_mino1, next_mino2,
                            hold_mino, score, level, goal)
                    if change % 2 == 1:
                        draw_hardboard_change(next_mino1, next_mino2, hold_mino, score, level, goal)
                    else:
                        draw_board(next_mino1, next_mino2, hold_mino, score, level, goal)
                        pygame.display.update()

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()
        

    elif pvp:

        for event in pygame.event.get():
            change_1P = combo_count_2P // 3
            change_2P = combo_count // 3
            if event.type == QUIT: #창 종료
                done = True

            elif event.type == USEREVENT: #키보드,마우스 이벤트 
                pygame.time.set_timer(pygame.USEREVENT, game_speed)  # 기본 게임속도 600으로 초기 설정
                draw_mino(dx, dy, mino, rotation, matrix)
                draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                # Draw a mino
                if attack_point == 2:
                    if change_2P % 2 == 1:
                        draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                    else:
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                if attack_point_2P == 2:
                    if change_1P % 2 == 1:
                        draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                    else:
                        draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation, matrix)
                    erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                ### 1P ###
                # Move mino down
                if not is_bottom(dx, dy, mino, rotation, matrix):
                    dy += 1

                # Create new mino
                else:

                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        draw_mino(dx, dy, mino, rotation, matrix)
                        
                        if attack_point == 2:
                            if change_2P % 2 == 1:
                                draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                            else:
                                draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                        if is_stackable(next_mino1, matrix):
                            mino = next_mino1
                            next_mino1 = randint(1, 10)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                            score += 10 * level
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            winner = 2
                            game_status = 'pvp'
                            pvp = False
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                ### 2P ###
                # Move mino down
                if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                    dy_2P += 1

                # Create new mino
                else:

                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        draw_mino(dx_2P, dy_2P, mino_2P,
                                rotation_2P, matrix_2P)
                        if attack_point_2P == 2:
                            if change_1P % 2 == 1:
                                draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                            else:
                                draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                        if is_stackable(next_mino1_2P, matrix_2P):
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 10)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                            score_2P += 10 * level_2P
                        else:  # 더이상 쌓을 수 없으면 게임오버
                            winner = 1
                            game_status = 'pvp'
                            pvp = False
                            game_over = True
                            ui_variables.GameOver_sound.play()
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1


                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (1P)
                attack_stack=0
                attack_stack_2P=0
                for j in range(board_y + 1):
                    is_full = True  # 한 줄이 가득 찼는지 확인하기 위한 변수
                    for i in range(board_x):
                        if matrix[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        combo_count += 1
                        attack_stack+=1
                        if combo_count % 3 == 0:
                            attack_point = randint(1,2)
                            if attack_point == 1:
                                key_reverse_2P = True # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                            if attack_point == 2:
                                if change_2P % 2 == 1:
                                    draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                            hold_mino_2P, current_key, current_key_2P)
                                else:
                                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                            
                    
                        pygame.display.update()
                        pygame.time.delay(400)
                        ui_variables.break_sound.play()
                        k = j

                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                matrix[i][k] = matrix[i][k - 1]  # 한줄씩 밑으로 내림
                            k -= 1

                # 한 줄이 차면 그 위의 블럭들 한 줄씩 아래로 내리기. (2P)
                for j in range(board_y + 1):
                    is_full = True
                    for i in range(board_x):
                        if matrix_2P[i][j] == 0:  # 빈 곳인 경우
                            is_full = False  # 클리어 되지 못함
                    if is_full:
                        combo_count_2P += 1
                        attack_stack_2P+=1
                        if combo_count_2P % 3 == 0:
                            attack_point_2P = randint(1,2)
                            if attack_point_2P == 1:
                                key_reverse = True  # 상대방 키 반전조건 성립 (몇 줄을 깨든)
                            if attack_point_2P == 2:
                                if change_1P % 2 == 1:
                                    draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                                else:
                                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                        hold_mino_2P, current_key, current_key_2P)
                            
                        pygame.display.update()
                        pygame.time.delay(400)
                        ui_variables.break_sound.play()
                        k = j
                        while k > 0:  # y좌표가 matrix 안에 있는 동안
                            for i in range(board_x):  # 해당 줄의 x좌표들 모두
                                # 한줄씩 밑으로 내림
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1
                while attack_stack >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix_2P[i][j] = matrix_2P[i][j + 1]

                            attack_stack -= 1
                    for i in range(10):
                        matrix_2P[i][20] = 9
                    k = randint(0, 9)
                    matrix_2P[k][20] = 0
                    attack_point += 1

                while attack_stack_2P >= 2:
                    for j in range(20):
                        for i in range(10):
                            matrix[i][j] = matrix[i][j + 1]

                            attack_stack_2P -= 1
                    for i in range(10):
                        matrix[i][20] = 9
                    k = randint(0, 9)
                    matrix[k][20] = 0
                    attack_point_2P += 1

                if key_reverse:   # 키 반전 조건(상대가 몇 줄이든 깸)이 성립됐다면
                    # 방향키 반전 (최근 방향키가 어떤 것이었든 반대로)
                    current_key = not current_key
                    key1 = multi_reverse_key(current_key, 1)
                    key_reverse = False  # 다시 키 반전 조건은 False로 (default)
                if key_reverse_2P:
                    current_key_2P = not current_key_2P
                    key2 = multi_reverse_key(current_key_2P, 2)
                    key_reverse_2P = False

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation, matrix)
                erase_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)

                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    pause = True

                # Hold
                elif event.key == K_LSHIFT:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino1
                            next_mino1 = randint(1, 10)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                            
                elif event.key == K_RSHIFT:
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino1_2P
                            next_mino1_2P = randint(1, 10)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                    # dx, dy는 각각 좌표위치 이동에 해당하며, rotation은 mino.py의 테트리스 블록 회전에 해당함
                    # Hard drop
                # 왼쪽창#
                elif event.key == key1['hardDrop']:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation, matrix):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                elif event.key == key2['hardDrop']:  # 오른쪽창#
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, framerate_2P)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn right
                elif event.key == key1['turnRight']:  # 왼쪽창#
                    if is_turnable_r(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                elif event.key == key2['turnRight']:  # 오른쪽창#
                    if is_turnable_r(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Turn left
                elif event.key == key1['turnLeft']:
                    if is_turnable_l(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation -= 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation -= 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation -= 1
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                elif event.key == key2['turnLeft']:  # 오른쪽창#
                    if is_turnable_l(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        rotation_2P -= 1
                    # Kick
                    elif is_turnable_l(dx_2P, dy_2P - 1, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 1, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P, dy_2P - 2, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P + 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P -= 1
                    elif is_turnable_l(dx_2P - 2, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P -= 1
                    if rotation_2P == -1:
                        rotation_2P = 3
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left (1P)
                # key = pygame.key.get_pressed()
                elif event.key == key1['moveLeft']:
                    if not is_leftedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                # Move right (1P)
                elif event.key == key1['moveRight']:
                    if not is_rightedge(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Move left(2P)
                elif event.key == key2['moveLeft']:
                    if not is_leftedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P -= 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                # Move right(2P)
                elif event.key == key2['moveRight']:
                    if not is_rightedge(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dx_2P += 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

                # Soft drop (1P)
                elif event.key == key1['softDrop']:
                    if not is_bottom(dx, dy, mino, rotation, matrix):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_blockmove)
                        dy = dy + 1
                    draw_mino(dx, dy, mino, rotation, matrix)
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    if attack_point == 2:
                        if change_2P % 2 == 1:
                            draw_multiboard_2p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        
                # Soft drop (2P)
                elif event.key == key2['softDrop']:
                    if not is_bottom(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(
                            pygame.KEYUP, framerate_2P_blockmove)
                        dy_2P = dy_2P + 1
                    draw_mino(dx_2P, dy_2P, mino_2P, rotation_2P, matrix_2P)
                    draw_mino(dx, dy, mino, rotation, matrix)
                    if attack_point_2P == 2:
                        if change_1P % 2 == 1:
                            draw_multiboard_1p_change(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)
                        else:
                            draw_multiboard(next_mino1, hold_mino, next_mino1_2P,
                                    hold_mino_2P, current_key, current_key_2P)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                if not ((board_rate - 0.1) < (board_height / board_width) < (
                        board_rate + 0.05)):  # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        pygame.display.update()



    # new game over screen
    elif game_over:

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()

                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초

                if game_status == 'pvp':
                    # 기존 화면 약간 어둡게 처리
                    draw_image(screen, gamebackground_image, board_width * 0.5, board_height *
                            0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    draw_multiboard(next_mino1, hold_mino, next_mino1_2P, hold_mino_2P,
                                    current_key, current_key_2P)
                    pause_surface = screen.convert_alpha()  # 투명 가능하도록
                    pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
                    pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
                        board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
                    screen.blit(pause_surface, (0, 0))
                    #

                    draw_image(screen, multi_gameover_image, board_width * 0.5, board_height * 0.2,
                               int(board_height * 0.7), int(board_height * 0.2))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    if winner == 1:  # 1P가 이기면
                        draw_image(screen, multi_win_image, board_width * 0.2, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_image(screen, multi_lose_image, board_width * 0.8, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    elif winner == 2:  # 2P가 이기면
                        draw_image(screen, multi_win_image, board_width * 0.8, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                        draw_image(screen, multi_lose_image, board_width * 0.2, board_height * 0.5,
                                   int(board_height * 0.3), int(board_height * 0.25))  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

                    multi_menu_button.draw(screen, (0, 0, 0))
                    multi_restart_button.draw(screen, (0, 0, 0))

                elif game_status != 'pvp':
                    draw_image(screen, gameover_board_image, board_width * 0.5, board_height * 0.5,
                               int(board_height * 1), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
                    menu_button2.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
                    restart_button.draw(screen, (0, 0, 0))
                    ok_button.draw(screen, (0, 0, 0))

                    # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
                    name_1 = ui_variables.h1_b.render(
                        chr(name[0]), 1, ui_variables.white)
                    name_2 = ui_variables.h1_b.render(
                        chr(name[1]), 1, ui_variables.white)
                    name_3 = ui_variables.h1_b.render(
                        chr(name[2]), 1, ui_variables.white)

                    underbar_1 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)
                    underbar_2 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)
                    underbar_3 = ui_variables.h1_b.render(
                        "_", 1, ui_variables.white)

                    # blit(요소, 위치), 각각 전체 board의 가로길이, 세로길이에다가 원하는 비율을 곱해줌
                    screen.blit(name_1, (int(board_width * 0.434),
                                int(board_height * 0.55)))
                    screen.blit(name_2, (int(board_width * 0.494),
                                int(board_height * 0.55)))  # blit(요소, 위치)
                    screen.blit(name_3, (int(board_width * 0.545),
                                int(board_height * 0.55)))  # blit(요소, 위치)

                    if blink:
                        blink = False
                    else:
                        if name_location == 0:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_1, ((int(board_width * 0.437), int(board_height * 0.56))))
                        elif name_location == 1:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_2, ((int(board_width * 0.497), int(board_height * 0.56))))
                        elif name_location == 2:
                            # 위치 비율 고정
                            screen.blit(
                                underbar_3, ((int(board_width * 0.557), int(board_height * 0.56))))
                        blink = True

                pygame.display.update()

            elif event.type == KEYDOWN and game_status != 'pvp':  # 멀티모드 아닐 때만 스코어 저장

                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    if game_status == 'start':  # easy mode일 경우
                        outfile = open('leaderboard.txt', 'a')
                        outfile.write(
                            chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                        outfile.close()
                    elif game_status == 'hard':  # hard mode일 경우
                        outfile = open('leaderboard_hard.txt', 'a')
                        outfile.write(
                            chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                        outfile.close()

                    game_over = False
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초

                # name은 3글자로 name_locationd은 0~2, name[name_location]은 영어 아스키코드로 65~90.
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == pygame.MOUSEMOTION:
                if menu_button2.isOver_2(pos):
                    menu_button2.image = clicked_menu_button_image
                else:
                    menu_button2.image = menu_button_image

                if restart_button.isOver_2(pos):
                    restart_button.image = clicked_restart_button_image
                else:
                    restart_button.image = restart_button_image

                if ok_button.isOver_2(pos):
                    ok_button.image = clicked_ok_button_image
                else:
                    ok_button.image = ok_button_image

                # 멀티모드 게임오버 화면 버튼
                if multi_menu_button.isOver_2(pos):
                    multi_menu_button.image = clicked_menu_button_image
                else:
                    multi_menu_button.image = menu_button_image

                if multi_restart_button.isOver_2(pos):
                    multi_restart_button.image = clicked_restart_button_image
                else:
                    multi_restart_button.image = restart_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_status != 'pvp':
                    if ok_button.isOver(pos):
                        ui_variables.click_sound.play()
                        if game_status == 'start':  # easy mode 일 경우
                            outfile = open('leaderboard.txt', 'a')
                            outfile.write(
                                chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                            outfile.close()
                        elif game_status == 'hard':  # hard mode 일 경우
                            outfile = open('leaderboard_hard.txt', 'a')
                            outfile.write(
                                chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                            outfile.close()
                        game_over = False
                        pygame.time.set_timer(pygame.USEREVENT, 1)

                    if menu_button2.isOver(pos):
                        ui_variables.click_sound.play()
                        game_over = False

                    if restart_button.isOver_2(pos):
                        if game_status == 'start':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            start = True
                            pygame.mixer.music.play(-1)  # play(-1) = 노래 반복재생
                        if game_status == 'pvp':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            pvp = True
                            pygame.mixer.music.play(-1)
                        if game_status == 'hard':
                            set_initial_values()
                            ui_variables.intro_sound.stop()
                            hard = True
                            pygame.mixer.music.play(-1)
                        ui_variables.click_sound.play()
                        game_over = False
                        pause = False

                    if resume_button.isOver_2(pos):
                        pause = False
                        ui_variables.click_sound.play()
                        pygame.time.set_timer(pygame.USEREVENT, 1)  # 0.001초

                # 멀티모드 게임오버 화면 버튼
                if game_status == 'pvp':
                    if multi_menu_button.isOver_2(pos):
                        ui_variables.click_sound.play()
                        game_over = False
                    if multi_restart_button.isOver_2(pos):
                        set_initial_values()
                        pvp = True
                        pygame.mixer.music.play(-1)

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기비율 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif select_mode:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        single_button.draw(screen, (0, 0, 0))
        # easy_button.draw(screen, (0, 0, 0)) #easy mode
        # hard_button.draw(screen, (0, 0, 0)) #hard mode
        # normal_button.draw(screen, (0, 0, 0))
        pvp_button.draw(screen, (0, 0, 0)) #multi mode
        back_button.draw(screen, (0, 0, 0))
        

        pygame.display.update()  # select mode 화면으로 넘어가도록 전체 화면 업데이트

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
                
            # button 이미지 mouse over 시 색칠
            elif event.type == pygame.MOUSEMOTION:
                if single_button.isOver_2(pos):
                    single_button.image = clicked_single_button_image
                else:
                    single_button.image = single_button_image
                # if easy_button.isOver_2(pos):
                #     easy_button.image = clicked_easy_button_image
                # else:
                #     easy_button.image = easy_button_image

                if pvp_button.isOver_2(pos):
                    pvp_button.image = clicked_pvp_button_image
                else:
                    pvp_button.image = pvp_button_image

                # if hard_button.isOver_2(pos):
                #     hard_button.image = clicked_hard_button_image
                # else:
                #     hard_button.image = hard_button_image

                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                    
            # mouse click 시 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if single_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    single = True
                    initialize = True
                    select_mode = False

                # if easy_button.isOver_2(pos):
                #     ui_variables.click_sound.play()
                #     previous_time = pygame.time.get_ticks()
                #     ui_variables.intro_sound.stop()
                #     pygame.mixer.music.play(-1)
                #     start = True
                #     initialize = True
                #     select_mode = False
                if pvp_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    pvp = True
                    initialize = True
                    select_mode = False
                    
                # if hard_button.isOver_2(pos):
                #     ui_variables.click_sound.play()
                #     ui_variables.intro_sound.stop()
                #     pygame.mixer.music.play(-1)
                #     hard = True
                #     initialize = True
                #     select_mode = False
                    
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    select_mode = False
                    initialize = False
                    
            # 창 사이즈 조절
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)
    elif single:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        easy_button.draw(screen, (0, 0, 0)) #easy mode
        hard_button.draw(screen, (0, 0, 0)) #hard mode
        normal_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))
        

        pygame.display.update()  # select mode 화면으로 넘어가도록 전체 화면 업데이트
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
                
            # button 이미지 mouse over 시 색칠
            elif event.type == pygame.MOUSEMOTION:
                if easy_button.isOver_2(pos):
                    easy_button.image = clicked_easy_button_image
                else:
                    easy_button.image = easy_button_image
                
                if normal_button.isOver_2(pos):
                    normal_button.image = clicked_normal_button_image
                else:
                    normal_button.image = normal_button_image

                if hard_button.isOver_2(pos):
                    hard_button.image = clicked_hard_button_image
                else:
                    hard_button.image = hard_button_image

                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                    
            # mouse click 시 
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if easy_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    start = True
                    initialize = True
                    single = False
                
                
                if normal_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    normal = True
                    initialize = True
                    single = False
                    
                if hard_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.play(-1)
                    hard = True
                    initialize = True
                    single = False
                    
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    select_mode = True
                    initialize = False
                    single = False
                    
            # 창 사이즈 조절
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)
        
# score_board 셋팅
    elif leader_board:
        screen.fill(ui_variables.real_white)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, scoreboard_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)

        easy_mode_text = ui_variables.h2_b.render(
            "EASY MODE:", 1, ui_variables.yellow)
        hard_mode_text = ui_variables.h2_b.render(
            "HARD MODE:", 1, ui_variables.yellow)
        screen.blit(easy_mode_text, (board_width * 0.2, board_height * 0.2))
        screen.blit(hard_mode_text, (board_width * 0.55, board_height * 0.2))

        back_button.draw(screen, (0, 0, 0))

        # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        # easy mode
        leader_1 = ui_variables.h2_b.render(
            '1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.white)
        leader_2 = ui_variables.h2_b.render(
            '2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.white)
        leader_3 = ui_variables.h2_b.render(
            '3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.white)
        screen.blit(leader_1, (board_width * 0.2,
                    board_height * 0.35))  # 위치 비율 고정
        screen.blit(leader_2, (board_width * 0.2,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(leader_3, (board_width * 0.2,
                    board_height * 0.65))  # 위치 비율 고정

        # hard mode
        leader_1 = ui_variables.h2_b.render(
            '1st ' + leaders_hard[0][0] + ' ' + str(leaders_hard[0][1]), 1, ui_variables.white)
        leader_2 = ui_variables.h2_b.render(
            '2nd ' + leaders_hard[1][0] + ' ' + str(leaders_hard[1][1]), 1, ui_variables.white)
        leader_3 = ui_variables.h2_b.render(
            '3rd ' + leaders_hard[2][0] + ' ' + str(leaders_hard[2][1]), 1, ui_variables.white)
        screen.blit(leader_1, (board_width * 0.55,
                    board_height * 0.35))  # 위치 비율 고정
        screen.blit(leader_2, (board_width * 0.55,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(leader_3, (board_width * 0.55,
                    board_height * 0.65))  # 위치 비율 고정

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver_2(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    leader_board = False
            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)
    
#셋팅 페이지 
    elif screen_setting:
        screen.fill(ui_variables.pinkpurple)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        background1_check_button.draw(screen, (0, 0, 0))
        background2_check_button.draw(screen, (0, 0, 0))
        background3_check_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        Background1_text = ui_variables.h5.render(
            'HongKong', 1, ui_variables.white)
        Background2_text = ui_variables.h5.render(
            'NewYork', 1, ui_variables.white)
        Background3_text = ui_variables.h5.render(
            'London', 1, ui_variables.white)
        screen.blit(Background1_text, (board_width * 0.47,
                    board_height * 0.33))  # 위치 비율 고정
        screen.blit(Background2_text, (board_width * 0.47,
                    board_height * 0.52))  # 위치 비율 고정
        screen.blit(Background3_text, (board_width * 0.47,
                    board_height * 0.73))  # 위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = False
                if background1_check_button.isOver(pos):
                    gamebackground_image = 'Tetris_Game/assets/images/background_hongkong.png'
                    # 클릭한 이미지에만 체크 표시
                    background2_check_button.image = background2_image
                    background3_check_button.image = background3_image
                    background1_check_button.image = clicked_background1_image

                if background2_check_button.isOver(pos):
                    gamebackground_image = 'Tetris_Game/assets/images/background_nyc.png'
                    # 클릭한 이미지에만 체크 표시
                    background1_check_button.image = background1_image
                    background3_check_button.image = background3_image
                    background2_check_button.image = clicked_background2_image

                if background3_check_button.isOver(pos):
                    gamebackground_image = 'Tetris_Game/assets/images/background_uk.png'
                    # 클릭한 이미지에만 체크 표시
                    background1_check_button.image = background1_image
                    background2_check_button.image = background2_image
                    background3_check_button.image = clicked_background3_image
                pygame.display.update()

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif volume_setting:
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색#
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))  # 위치 비율 고정

        # draw_image(window, 이미지주소, x좌표, y좌표, 너비, 높이)
        draw_image(screen, setting_board_image, board_width * 0.5,
                   board_height * 0.5, int(board_height * 1.3), board_height)
        draw_image(screen, number_board, board_width * 0.35, board_height *
                   0.53, int(board_width * 0.09), int(board_height * 0.1444))
        draw_image(screen, number_board, board_width * 0.35, board_height *
                   0.73, int(board_width * 0.09), int(board_height * 0.1444))
        mute_button.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색#

        effect_plus_button.draw(screen, (0, 0, 0))
        effect_minus_button.draw(screen, (0, 0, 0))
        sound_plus_button.draw(screen, (0, 0, 0))
        sound_minus_button.draw(screen, (0, 0, 0))
        #음소거 추가#
        effect_sound_on_button.draw(screen, (0, 0, 0))
        music_sound_on_button.draw(screen, (0, 0, 0))

        # BGM 선택 버튼 3개
        BGM1_sound_on_button.draw(screen, (0, 0, 0))
        BGM2_sound_on_button.draw(screen, (0, 0, 0))
        BGM3_sound_on_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        # render("텍스트이름", 안티에일리어싱 적용, 색깔), 즉 아래의 코드에서 숫자 1=안티에일리어싱 적용에 관한 코드
        music_volume_text = ui_variables.h5.render(
            'Music Volume', 1, ui_variables.white)
        effect_volume_text = ui_variables.h5.render(
            'Effect Volume', 1, ui_variables.white)
        screen.blit(music_volume_text, (board_width *
                    0.3, board_height * 0.4))  # 위치 비율 고정
        screen.blit(effect_volume_text, (board_width *
                    0.3, board_height * 0.6))  # 위치 비율 고정

        music_volume_text = ui_variables.h5.render(
            'Music On/Off', 1, ui_variables.white)
        effect_volume_text = ui_variables.h5.render(
            'Effect On/Off', 1, ui_variables.white)
        screen.blit(music_volume_text, (board_width *
                    0.5, board_height * 0.4))  # 위치 비율 고정
        screen.blit(effect_volume_text, (board_width *
                    0.5, board_height * 0.6))  # 위치 비율 고정

        music_volume_size_text = ui_variables.h4.render(
            str(music_volume), 1, ui_variables.grey_1)
        effect_volume_size_text = ui_variables.h4.render(
            str(effect_volume), 1, ui_variables.grey_1)
        screen.blit(music_volume_size_text, (board_width *
                    0.33, board_height * 0.5))  # 위치 비율 고정
        screen.blit(effect_volume_size_text, (board_width *
                    0.33, board_height * 0.7))  # 위치 비율 고정

        BGM1_text = ui_variables.h5.render('BGM1', 1, ui_variables.white)
        BGM2_text = ui_variables.h5.render('BGM2', 1, ui_variables.white)
        BGM3_text = ui_variables.h5.render('BGM3', 1, ui_variables.white)

        screen.blit(BGM1_text, (board_width * 0.65,
                    board_height * 0.3))  # 위치 비율 고정
        screen.blit(BGM2_text, (board_width * 0.65,
                    board_height * 0.5))  # 위치 비율 고정
        screen.blit(BGM3_text, (board_width * 0.65,
                    board_height * 0.7))  # 위치 비율 고정

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정

                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image
                if effect_plus_button.isOver(pos):
                    effect_plus_button.image = clicked_plus_button_image
                else:
                    effect_plus_button.image = plus_button_image

                if effect_minus_button.isOver(pos):
                    effect_minus_button.image = clicked_minus_button_image
                else:
                    effect_minus_button.image = minus_button_image

                if sound_plus_button.isOver(pos):
                    sound_plus_button.image = clicked_plus_button_image
                else:
                    sound_plus_button.image = plus_button_image

                if sound_minus_button.isOver(pos):
                    sound_minus_button.image = clicked_minus_button_image
                else:
                    sound_minus_button.image = minus_button_image

                if mute_button.image == mute_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_mute_button_image
                    else:
                        mute_button.image = mute_button_image
                if mute_button.image == clicked_mute_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_mute_button_image
                    else:
                        mute_button.image = mute_button_image

                if mute_button.image == default_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_default_button_image
                    else:
                        mute_button.image = default_button_image
                if mute_button.image == clicked_default_button_image:
                    if mute_button.isOver(pos):
                        mute_button.image = clicked_default_button_image
                    else:
                        mute_button.image = default_button_image

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    pygame.mixer.music.stop()
                    ui_variables.intro_sound.play()
                    volume_setting = False
                if sound_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume >= 10:  # 음량 최대크기
                        music_volume = 10
                    else:
                        music_sound_on_button.image = sound_on_button_image
                        music_volume += 1
                if sound_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume <= 0:  # 음량 최소크기
                        music_volume = 0
                        music_sound_on_button.image = sound_off_button_image
                    else:
                        if music_volume == 1:
                            music_sound_on_button.image = sound_off_button_image
                            music_volume -= 1
                        else:
                            music_sound_on_button.image = sound_on_button_image
                            music_volume -= 1
                if effect_plus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume >= 10:  # 음량 최대크기
                        effect_volume = 10
                    else:
                        effect_sound_on_button.image = sound_on_button_image
                        effect_volume += 1
                if effect_minus_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume <= 0:  # 음량 최소크기
                        effect_volume = 0
                        effect_sound_on_button.image = sound_off_button_image
                    else:
                        if effect_volume == 1:
                            effect_sound_on_button.image = sound_off_button_image
                            effect_volume -= 1
                        else:
                            effect_sound_on_button.image = sound_on_button_image
                            effect_volume -= 1
                #BGM 선택 기능 추가#
                # BGM버튼을 누르면 인트로음악은 멈추고 해당 BGM재생됨 (Back버튼을 눌러 뒤로가기 전까지 계속 재생)
                if BGM1_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("Tetris_Game/assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM2_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = backgroundmusic_select_image
                    BGM1_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "Tetris_Game/assets/sounds/BGM1.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()
                if BGM2_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("Tetris_Game/assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM1_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = backgroundmusic_select_image
                    BGM2_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "Tetris_Game/assets/sounds/BGM2.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()
                if BGM3_sound_on_button.isOver(pos):
                    #ui_variables.intro_sound.("Tetris_Game/assets/sounds/BGM2.wav")#
                    # 클릭한 버튼만 체크 표시되도록
                    BGM1_sound_on_button.image = backgroundmusic_select_image
                    BGM2_sound_on_button.image = backgroundmusic_select_image
                    BGM3_sound_on_button.image = clicked_backgroundmusic_select_image
                    ui_variables.intro_sound.stop()
                    pygame.mixer.music.stop()
                    selected_bgm = "Tetris_Game/assets/sounds/BGM3.wav"
                    pygame.mixer.music.load(selected_bgm)
                    pygame.mixer.music.play()

                #음소거 추가#
                if music_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if music_volume == 0:
                        music_volume = 5  # 중간 음량으로
                        music_sound_on_button.image = sound_on_button_image
                    else:
                        music_volume = 0
                        music_sound_off_button.draw(
                            screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
                        music_sound_on_button.image = sound_off_button_image
                if effect_sound_on_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if effect_volume == 0:
                        effect_volume = 5  # 중간 음량으로
                        effect_sound_on_button.image = sound_on_button_image
                    else:
                        effect_volume = 0
                        effect_sound_off_button.draw(screen, (0, 0, 0))
                        effect_sound_on_button.image = sound_off_button_image
                if mute_button.isOver(pos):
                    ui_variables.click_sound.play()
                    if (effect_volume == 0) and (music_volume == 0):
                        music_volume = 5  # 중간 음량으로
                        effect_volume = 5  # 중간 음량으로
                        mute_button.image = mute_button_image
                    else:
                        music_volume = 0  # 최소 음량으로
                        effect_volume = 0  # 최소 음량으로
                        # default_button.draw(screen, (0, 0, 0))
                        mute_button.image = default_button_image

                set_volume()

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    elif size_setting:
        screen.fill(ui_variables.pinkpurple)
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause),
                         [0, 0, int(board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)

        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5, int(board_height * 1.3),
                   board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)
        size1_check_button.draw(screen, (0, 0, 0))
        size2_check_button.draw(screen, (0, 0, 0))
        size3_check_button.draw(screen, (0, 0, 0))
        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    size_setting = False
                    
                if size1_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 800
                    board_height = 450
                    block_size = int(board_height * 0.045)  # 블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = False

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

                if size2_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1200
                    board_height = 675
                    block_size = int(board_height * 0.045)  # 블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)

                    pygame.display.update()

                if size3_check_button.isOver(pos):
                    ui_variables.click_sound.play()
                    board_width = 1600
                    board_height = 900
                    block_size = int(board_height * 0.045)  # 블록 크기 비율 고정
                    screen = pygame.display.set_mode((board_width, board_height), pygame.RESIZABLE)
                    textsize = True

                    for i in range(len(button_list)):
                        button_list[i].change(board_width, board_height)
                    pygame.display.update()

    elif setting:
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))
        # 배경 약간 어둡게
        leaderboard_icon.draw(screen, (0, 0, 0))
        pause_surface = screen.convert_alpha()  # 투명 가능하도록
        pause_surface.fill((0, 0, 0, 0))  # 투명한 검정색으로 덮기
        pygame.draw.rect(pause_surface, (ui_variables.black_pause), [0, 0, int(
            board_width), int(board_height)])  # (screen, 색깔, 위치 x, y좌표, 너비, 높이)
        screen.blit(pause_surface, (0, 0))

        draw_image(screen, setting_board_image, board_width * 0.5, board_height * 0.5,
                   int(board_height * 1.3), board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        screen_icon.draw(screen, (0, 0, 0))  # rgb(0,0,0) = 검정색
        volume_icon.draw(screen, (0, 0, 0))
        size_icon.draw(screen, (0, 0, 0))

        back_button.draw(screen, (0, 0, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)  # 0.3초로 설정
                pygame.display.update()

            elif event.type == pygame.MOUSEMOTION:
                if back_button.isOver(pos):
                    back_button.image = clicked_back_button_image
                else:
                    back_button.image = back_button_image

                if volume_icon.isOver(pos):
                    volume_icon.image = clicked_volume_vector
                else:
                    volume_icon.image = volume_vector

                if screen_icon.isOver(pos):
                    screen_icon.image = clicked_screen_vector
                else:
                    screen_icon.image = screen_vector
                
                if size_icon.isOver(pos):
                    size_icon.image = clicked_size_vector
                else:
                    size_icon.image = size_vector

                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = False

                if volume_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    volume_setting = True

                if screen_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    screen_setting = True

                if size_icon.isOver(pos):
                    ui_variables.click_sound.play()
                    size_setting = True    

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate-0.1) < (board_height/board_width) < (board_rate+0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width*board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

    # Start screen
    else:
        # 초기화
        if initialize:
            set_initial_values()
        initialize = False

        # 인트로 사운드 플레이
        ui_variables.intro_sound.play()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True

            elif event.type == pygame.MOUSEMOTION:
                if select_mode_button.isOver_2(pos):
                    select_mode_button.image = clicked_select_mode_button_image
                else:
                    select_mode_button.image = select_mode_button_image

                if quit_button.isOver_2(pos):
                    quit_button.image = clicked_quit_button_image
                else:
                    quit_button.image = quit_button_image

                if setting_button.isOver_2(pos):
                    setting_button.image = clicked_setting_button_image
                else:
                    setting_button.image = setting_button_image

                if score_board_button.isOver_2(pos):
                    score_board_button.image = clicked_score_board_button_image
                else:
                    score_board_button.image = score_board_button_image

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if select_mode_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    previous_time = pygame.time.get_ticks()
                    select_mode = True
                    initialize = True
                    # #pygame.mixer.music.play(-1) #play(-1) = 노래 반복재생
                    # #ui_variables.intro_sound.stop()
                if setting_button.isOver(pos):
                    ui_variables.click_sound.play()
                    setting = True
                if score_board_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    leader_board = True
                if quit_button.isOver_2(pos):
                    ui_variables.click_sound.play()
                    done = True

            elif event.type == VIDEORESIZE:
                board_width = event.w
                board_height = event.h
                if board_width < min_width or board_height < min_height:  # 최소 너비 또는 높이를 설정하려는 경우
                    board_width = min_width
                    board_height = min_height
                    pygame.display.set_caption("TETRIS(s)")
                # 높이 또는 너비가 비율의 일정수준 이상을 넘어서게 되면
                if not ((board_rate - 0.1) < (board_height / board_width) < (board_rate + 0.05)):
                    # 너비를 적정 비율로 바꿔줌
                    board_width = int(board_height / board_rate)
                    # 높이를 적정 비율로 바꿔줌
                    board_height = int(board_width * board_rate)
                if board_width >= mid_width:  # 화면 사이즈가 큰 경우
                    textsize = True  # 큰 글자크기 사용
                if board_width < mid_width:  # 화면 사이즈가 작은 경우
                    textsize = False  # 작은 글자크기 사용

                block_size = int(board_height * 0.045)  # 블록 크기 고정
                screen = pygame.display.set_mode(
                    (board_width, board_height), pygame.RESIZABLE)

                for i in range(len(button_list)):
                    button_list[i].change(board_width, board_height)

        # 메인화면 배경
        draw_image(screen, background_image, board_width * 0.5, board_height *
                0.5, board_width, board_height)  # (window, 이미지주소, x좌표, y좌표, 너비, 높이)

        # 버튼그리기
        select_mode_button.draw(screen, (0, 0, 0))
        setting_button.draw(screen, (0, 0, 0))
        score_board_button.draw(screen, (0, 0, 0))
        quit_button.draw(screen, (0, 0, 0))

        if not start:
            pygame.display.update()
            clock.tick(60)

pygame.quit()
