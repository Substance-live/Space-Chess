import pygame
import copy
import sys

pygame.init()


# Методы
def draw_field():
    for row in range(COUNT_TITLE):
        for column in range(COUNT_TITLE):
            if (row + column // 1) % 2 == 0:
                color = COLOR_TITLE_SECOND
            else:
                color = COLOR_TITLE_FIRST

            field_list[row][column].fill(color)
            field_list[row][column].set_alpha(ALPHA_PARAMETR)
            screen.blit(field_list[row][column], (
                LEFT_MARGIN + MARGIN + row * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + column * SIZE_TITLE, SIZE_TITLE,
                SIZE_TITLE))

            if (p1_skill_2_on and data_model[column][row] in (3, 4)) or (
                    p2_skill_2_on and data_model[column][row] in (10, 11)):
                screen.blit(stars[counter_3], (
                    LEFT_MARGIN + MARGIN + row * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + column * SIZE_TITLE,
                    SIZE_TITLE,
                    SIZE_TITLE))


def draw_models(data_model):
    if counter_tick != None:
        data = data_animation_kill
    elif counter_tick_flash != None:
        data = data_animation_swap
    else:
        data = data_model

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != 0:
                screen.blit(models[data[i][j]],
                            (LEFT_MARGIN + MARGIN + j * SIZE_TITLE, 2 * MARGIN + UPPER_MARGIN + i * SIZE_TITLE))


def select_title(pos):
    global selected_title
    x, y = pos
    if not (LEFT_MARGIN + MARGIN < x < SIZE[0] - RIGHT_MARGIN - MARGIN or y < UPPER_MARGIN + MARGIN):
        return None
    x, y = x - MARGIN - LEFT_MARGIN, y - 2 * MARGIN - UPPER_MARGIN
    row, column = x // SIZE_TITLE, y // SIZE_TITLE
    if (column + row) % 2 == 0:
        color_title = COLOR_SELECT_WHITE
    else:
        color_title = COLOR_SELECT_BLACK
    print(row, column)
    if data_model[column][row] == 0:
        return None
    else:
        if side_turn == 1 and data_model[column][row] in BLUE_LIST:
            return row, column, color_title
        elif side_turn == -1 and data_model[column][row] in RED_LIST:
            return row, column, color_title
        else:
            return None


def paint_tile():
    global field_list
    row, column, color_title = selected_title
    field_list[row][column].fill(color_title)
    screen.blit(field_list[row][column], (
        LEFT_MARGIN + MARGIN + row * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + column * SIZE_TITLE, SIZE_TITLE,
        SIZE_TITLE))


def paint_cicrles():
    row, column, color = selected_title

    for i in ret_places(row, column, data_model[column][row]):
        row, column = i
        if data_model[column][row] != 0:
            field_list[row][column].fill(COLOR_ENEMY_TITLE)
            screen.blit(field_list[row][column], (
                LEFT_MARGIN + MARGIN + row * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + column * SIZE_TITLE, SIZE_TITLE,
                SIZE_TITLE))
        else:
            screen.blit(circle_model, (
                LEFT_MARGIN + MARGIN + row * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + column * SIZE_TITLE, SIZE_TITLE,
                SIZE_TITLE))


def ret_places(row, column, type):
    ret = []
    if type in (4, None):  # Проверка красной мыши (пешки)
        if counter_turns_skill_2 == 0 or not (p1_skill_2_on):
            turns_list = (-1, 1)
        else:
            turns_list = (-2, -1, 1, 2)

        for i in turns_list:
            if 0 <= column + i < COUNT_TITLE and data_model[column + i][row] == 0:
                ret.append([row, column + i])

        if (row, column) in not_started_RED and data_model[column - 2][row] == 0 and data_model[column - 1][row] == 0:
            ret.append([row, column - 2])
        for i in range(-1, 2, 2):  # Создание списка с числами -1;1
            if 0 <= row + i <= COUNT_TITLE - 1 and 0 <= column - 1 <= COUNT_TITLE - 1 and data_model[column - 1][row + i] in BLUE_LIST:
                ret.append([row + i, column - 1])

    elif type in (11, None):  # Проверка синей мыши (пешки)
        if counter_turns_skill_2 == 0 or not (p2_skill_2_on):
            turns_list = (-1, 1)
        else:
            turns_list = (-2, -1, 1, 2)

        for i in turns_list:
            if 0 <= column + i < COUNT_TITLE and data_model[column + i][row] == 0:
                ret.append([row, column + i])
        if (row, column) in not_started_BLUE and data_model[column + 2][row] == 0 and data_model[column + 1][row] == 0:
            ret.append([row, column + 2])
        for i in range(-1, 2, 2):  # Создание списка с числами -1;1
            if 0 <= row + i <= COUNT_TITLE - 1 and 0 <= column + 1 <= COUNT_TITLE - 1 and data_model[column + 1][row + i] in RED_LIST:
                ret.append([row + i, column + 1])

    if type in (2, 9, None):  # Проверка диагональных прыжков на 1
        for i in range(-2, 3, 4):
            for j in range(-2, 3, 4):
                if 0 <= column + i <= COUNT_TITLE - 1 and 0 <= row + j <= COUNT_TITLE - 1:
                    if data_model[column + i][row + j] == 0:
                        ret.append([row + j, column + i])
                    else:
                        if (type in RED_LIST and data_model[column + i][row + j] in BLUE_LIST) or \
                                (type in BLUE_LIST and data_model[column + i][row + j] in RED_LIST):
                            ret.append([row + j, column + i])

    if type in (6, 13, 3, 10, None):  # Проверка диагонали на 1 шаг
        if counter_turns_skill_2 != 0 and ((type in RED_LIST and p1_skill_2_on) or (
                type in BLUE_LIST and p2_skill_2_on)) and type != 6 and type != 13:
            turns_list = (-2, -1, 1, 2)
        else:
            turns_list = (-1, 1)
        for i in turns_list:
            for j in turns_list:
                if 0 <= column + i <= COUNT_TITLE - 1 and 0 <= row + j <= COUNT_TITLE - 1:
                    if data_model[column + i][row + j] == 0:
                        ret.append([row + j, column + i])
                    elif abs(i) == 1 and abs(j) == 1:
                        if (type in RED_LIST and data_model[column + i][row + j] in BLUE_LIST) or \
                                (type in BLUE_LIST and data_model[column + i][row + j] in RED_LIST):
                            ret.append([row + j, column + i])

    if type in (2, 9, 3, 10, None):  # Проверка ортоганали на 1 шаг
        if counter_turns_skill_2 != 0 and ((type in RED_LIST and p1_skill_2_on) or (
                type in BLUE_LIST and p2_skill_2_on)) and type != 2 and type != 9:
            turns_list = (-2, -1, 1, 2)
        else:
            turns_list = (-1, 1)

        for i in turns_list:  # Шаг по x
            if 0 <= i + column <= COUNT_TITLE - 1:
                if data_model[column + i][row] == 0:
                    ret.append([row, column + i])
                elif abs(i) == 1 and abs(j) == 1:
                    if (type in RED_LIST and data_model[column + i][row] in BLUE_LIST) or \
                            (type in BLUE_LIST and data_model[column + i][row] in RED_LIST):
                        ret.append([row, column + i])

        for i in turns_list:  # Шаг по y
            if 0 <= i + row <= COUNT_TITLE - 1:
                if data_model[column][row + i] == 0:
                    ret.append([row + i, column])
                elif abs(i) == 1 and abs(j) == 1:
                    if (type in RED_LIST and data_model[column][row + i] in BLUE_LIST) or \
                            (type in BLUE_LIST and data_model[column][row + i] in RED_LIST):
                        ret.append([row + i, column])

    if type in (1, 8, 7, 14, None):  # Проверка Г-образного хода
        for i in range(-2, 3, 4):
            for j in range(-1, 2, 2):
                if 0 <= column + i <= COUNT_TITLE - 1 and 0 <= row + j <= COUNT_TITLE - 1:  # Проверка вертикальной оси
                    if data_model[column + i][row + j] == 0:
                        ret.append([row + j, column + i])
                    else:
                        if (data_model[column + i][row + j] in BLUE_LIST and not (type in BLUE_LIST)) or (
                                data_model[column + i][row + j] in RED_LIST and not (type in RED_LIST)):
                            ret.append([row + j, column + i])

                if 0 <= column + j <= COUNT_TITLE - 1 and 0 <= row + i <= COUNT_TITLE - 1:  # Проверка горизонтальной оси
                    if data_model[column + j][row + i] == 0:
                        ret.append([row + i, column + j])
                    else:
                        if (data_model[column + j][row + i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                                data_model[column + j][row + i] in RED_LIST and not (type in RED_LIST)):
                            ret.append([row + i, column + j])

    if type in (5, 12, None):  # 1-ый змеиный ход
        for mode1 in (-1, 1):
            for mode2 in (-1, 1):
                condition = True
                step = 1
                while condition:  # движение
                    for i in (-1, 0, 1, 0):
                        if 0 <= column + step * mode1 <= COUNT_TITLE - 1 and 0 <= row + i * mode2 <= COUNT_TITLE - 1:
                            if data_model[column + step * mode1][row + i * mode2] == 0:
                                ret.append([row + i * mode2, column + step * mode1])
                            else:
                                if (data_model[column + step * mode1][row + i * mode2] in BLUE_LIST and not (
                                        type in BLUE_LIST)) or (
                                        data_model[column + step * mode1][row + i * mode2] in RED_LIST and not (
                                        type in RED_LIST)):
                                    ret.append([row + i * mode2, column + step * mode1])
                                condition = False
                                break
                        else:
                            condition = False
                            break
                        step += 1

    if type in (5, 12, None):  # 2-ой змеиный ход
        for mode1 in (-1, 1):
            for mode2 in (-1, 1):
                condition = True
                i = 1
                while condition:  # движение
                    for step in (-1, 0, 1, 0):
                        if 0 <= column + step * mode1 <= COUNT_TITLE - 1 and 0 <= row + i * mode2 <= COUNT_TITLE - 1:
                            if data_model[column + step * mode1][row + i * mode2] == 0:
                                ret.append([row + i * mode2, column + step * mode1])
                            else:
                                if (data_model[column + step * mode1][row + i * mode2] in BLUE_LIST and not (
                                        type in BLUE_LIST)) or (
                                        data_model[column + step * mode1][row + i * mode2] in RED_LIST and not (
                                        type in RED_LIST)):
                                    ret.append([row + i * mode2, column + step * mode1])
                                condition = False
                                break
                        else:
                            condition = False
                            break
                        i += 1

    if type in (7, 14, 6, 13, None):  # Проверка ортоганального хода
        if type in (6, 13, None):
            skip = True
        else:
            skip = False

        for i in range(1, row + 1):  # Проверка влево
            if data_model[column][row - i] == 0:
                ret.append([row - i, column])
            elif not (skip):
                if (data_model[column][row - i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column][row - i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row - i, column])
                break

        for i in range(1, COUNT_TITLE - row):  # Проверка вправо
            if data_model[column][row + i] == 0:
                ret.append([row + i, column])
            elif not (skip):
                if (data_model[column][row + i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column][row + i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row + i, column])
                break

        for i in range(1, column + 1):  # Проверка вверх
            if data_model[column - i][row] == 0:
                ret.append([row, column - i])
            elif not (skip):
                if (data_model[column - i][row] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column - i][row] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row, column - i])
                break

        for i in range(1, COUNT_TITLE - column):  # Проверка вниз
            if data_model[column + i][row] == 0:
                ret.append([row, column + i])
            elif not (skip):
                if (data_model[column + i][row] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column + i][row] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row, column + i])
                break

    if type in (1, 8, 6, 13, None):  # Проверка диагонального хода
        if type in (6, 13, None):
            skip = True
        else:
            skip = False

        minLenght = max(row, column)  # Кратчайший путь до доски для этого маршрута
        for i in range(1, COUNT_TITLE - minLenght):  # Проверка Вправо-вниз
            if data_model[column + i][row + i] == 0:
                ret.append([row + i, column + i])
            elif not (skip):
                if (data_model[column + i][row + i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column + i][row + i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row + i, column + i])
                break

        minLenght = min(row, column)  # Кратчайший путь до доски для этого маршрута
        for i in range(1, minLenght + 1):  # Проверка Влево-вверх
            if data_model[column - i][row - i] == 0:
                ret.append([row - i, column - i])
            elif not (skip):
                if (data_model[column - i][row - i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column - i][row - i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row - i, column - i])
                break

        minLenght = max(COUNT_TITLE - row - 1, column)  # # Кратчайший путь до доски для этого маршрута
        for i in range(1, COUNT_TITLE - minLenght):  # Проверка Влево-вниз
            if data_model[column + i][row - i] == 0:
                ret.append([row - i, column + i])
            elif not (skip):
                if (data_model[column + i][row - i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column + i][row - i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row - i, column + i])

                break

        minLenght = max(COUNT_TITLE - column - 1, row)  # # Кратчайший путь до доски для этого маршрута
        for i in range(1, COUNT_TITLE - minLenght):  # Проверка Вправо-вверх
            if data_model[column - i][row + i] == 0:
                ret.append([row + i, column - i])
            elif not (skip):
                if (data_model[column - i][row + i] in BLUE_LIST and not (type in BLUE_LIST)) or (
                        data_model[column - i][row + i] in RED_LIST and not (type in RED_LIST)):
                    ret.append([row + i, column - i])
                break
    return ret


def move_model(pos):
    global data_model, selected_title, side_turn, p1_skill_selected, p2_skill_selected, last_data, last_data_2, target_pos_skill_4, data_animation_kill, end_game, mana1, mana2, pos_animation_kill, last_moved

    data_model_copy = copy.deepcopy(data_model)

    rowSelect, columnSelect = (pos[0] - MARGIN - RIGHT_MARGIN) // SIZE_TITLE, (
            pos[1] - 2 * MARGIN - UPPER_MARGIN) // SIZE_TITLE
    ret = ret_places(selected_title[0], selected_title[1], data_model[selected_title[1]][selected_title[0]])

    if target_pos_skill_4 != None and ([rowSelect, columnSelect]) in ret:
        if selected_title[0] == target_pos_skill_4[0] and selected_title[1] == target_pos_skill_4[1]:
            target_pos_skill_4 = [rowSelect, columnSelect]
        elif rowSelect == target_pos_skill_4[0] and columnSelect == target_pos_skill_4[1]:
            target_pos_skill_4 = None

    if ([rowSelect, columnSelect]) in ret and data_model[columnSelect][rowSelect] == 0:

        if (rowSelect, columnSelect) in not_started_RED:  # Удаление красной мыши (пешки) из списка с неходившими
            not_started_RED.remove((rowSelect, columnSelect))
        elif (rowSelect, columnSelect) in not_started_BLUE:  # Удаление синей мыши (пешки) из списка с неходившими
            not_started_BLUE.remove((rowSelect, columnSelect))

        data_model[columnSelect][rowSelect], data_model[selected_title[1]][selected_title[0]] = \
            data_model[selected_title[1]][selected_title[0]], data_model[columnSelect][rowSelect]

        last_moved = True
    elif ([rowSelect, columnSelect]) in ret and data_model[columnSelect][rowSelect] != 0:

        data_animation_kill = copy.deepcopy(data_model)
        data_animation_kill[columnSelect][rowSelect] = 0
        pos_animation_kill = (selected_title[0], selected_title[1])

        if data_model[columnSelect][rowSelect] in (3, 10):
            end_game = True
            manacost = COST_KING
        elif data_model[columnSelect][rowSelect] in (1, 8):
            manacost = COST_DRAGON
        elif data_model[columnSelect][rowSelect] in (6, 13):
            manacost = COST_SCOUT
        elif data_model[columnSelect][rowSelect] in (4, 11):
            manacost = COST_COMMON
        elif data_model[columnSelect][rowSelect] in (5, 12):
            manacost = COST_SNAKE
        elif data_model[columnSelect][rowSelect] in (2, 9):
            manacost = COST_JUMPER
        elif data_model[columnSelect][rowSelect] in (7, 14):
            manacost = COST_WOLF

        if side_turn == -1:  # Синего убили
            mana2 += manacost
        else:
            mana1 += manacost
        last_moved = True

        data_model[columnSelect][rowSelect], data_model[selected_title[1]][selected_title[0]] = \
            data_model[selected_title[1]][selected_title[0]], 0

        start_boom((LEFT_MARGIN + MARGIN + rowSelect * SIZE_TITLE - 50 + SIZE_TITLE // 2,
                    MARGIN + columnSelect * SIZE_TITLE - 50 + SIZE_TITLE // 2), side_turn * -1)

    else:
        selected_title = None
        return
    selected_title = None
    side_turn *= -1
    last_data_2 = copy.deepcopy(last_data)
    last_data = copy.deepcopy(data_model_copy)
    p1_skill_selected = False
    p2_skill_selected = False


def draw_timer(type):
    string = calc_time_number(type)
    if type == 0:
        text = font_timer.render(string, False, COLOR_LIST_P1[1])
        screen.blit(text, (LEFT_MARGIN // 2 - text.get_size()[0] // 2, POS_TIMER1[1]))
    else:
        text = font_timer.render(string, False, COLOR_LIST_P2[1])
        screen.blit(text, (1620 - LEFT_MARGIN // 2 - text.get_size()[0] // 2, POS_TIMER1[1]))


def calc_time_number(type):
    if type == 0:
        min = clock1 // 60
        second = clock1 % 60
    else:
        min = clock2 // 60
        second = clock2 % 60

    if min < 10:
        total_min = "0" + str(min)
    else:
        total_min = str(min)

    if second < 10:
        total_second = "0" + str(second)
    else:
        total_second = str(second)
    return total_min + ":" + total_second


def draw_manaShard(type):
    if type == 0:
        x_shard1 = font_name.render('x', False, COLOR_LIST_P1[2])
        number_mana1 = font_name.render(f'{mana1}', False, COLOR_LIST_P1[2])
        x_shard2 = font_name.render('x', False, COLOR_LIST_P1[2])
        number_mana2 = font_name.render(f'{mana2}', False, COLOR_LIST_P1[2])

        screen.blit(number_mana1, (POS_SHARD1[0] - 20 - number_mana1.get_size()[0], POS_SHARD1[1] + 8))
        screen.blit(x_shard1, POS_SHARD1)
        screen.blit(COLOR_LIST_P1[4], (POS_SHARD1[0] + SPACE_SHARD_X + x_shard1.get_size()[0], POS_SHARD1[1]))
    else:
        x_shard1 = font_name.render('x', False, COLOR_LIST_P2[2])
        number_mana1 = font_name.render(f'{mana1}', False, COLOR_LIST_P2[2])
        x_shard2 = font_name.render('x', False, COLOR_LIST_P2[2])
        number_mana2 = font_name.render(f'{mana2}', False, COLOR_LIST_P2[2])
        screen.blit(number_mana2, (1620 - 30 - POS_SHARD1[0] - 20 - number_mana2.get_size()[0], POS_SHARD1[1] + 8))
        screen.blit(x_shard2, (1620 - 30 - POS_SHARD1[0], POS_SHARD1[1]))
        screen.blit(COLOR_LIST_P2[4],
                    (1620 - 30 - POS_SHARD1[0] + SPACE_SHARD_X + x_shard1.get_size()[0], POS_SHARD1[1]))


def draw_skill(type, num, manacost, name, description):
    if type == 0:
        POS_SKILL = POS_SKILL1
        COLOR = COLOR_LIST_P1
    else:
        POS_SKILL = (SIZE[0] - 180 - POS_SKILL1[0], POS_SKILL1[1])
        COLOR = COLOR_LIST_P2

    screen.blit(skills[0], POS_SKILL)
    screen.blit(skills[num], (POS_SKILL[0] + 56, POS_SKILL[1] + 12))
    if manacost < 10:
        manacost = f" {manacost}"
    else:
        manacost = str(manacost)

    d1 = font_mana.render(manacost, False, COLOR[2])
    d2 = font_skill_name.render(name, False, COLOR[3])
    if description == "":
        d3 = font_discription.render(description, False, COLOR[3])
    else:
        d3 = description

    screen.blit(d1, (POS_SKILL[0] + 5, POS_SKILL[1] + 2))
    screen.blit(d2, (POS_SKILL[0] + 90 - d2.get_size()[0] // 2, POS_SKILL[1] + 90))
    screen.blit(d3, (POS_SKILL[0] + 10, POS_SKILL[1] + 130))
    screen.blit(COLOR[5], (POS_SKILL[0] - 75, POS_SKILL[1] + 60))  # Стрелочки


def choose_side_turn(type):  # -1/1 = red/blue
    global COLOR_LIST_P1, COLOR_LIST_P2
    if type == -1:
        COLOR_LIST_P1 = (COLOR_TEAM1, COLOR_TIMER, COLOR_MANA_SHARD, COLOR_BG, shard, arrows)
        COLOR_LIST_P2 = [COLOR_NOTCLICK for i in range(len(COLOR_LIST_P1) - 2)]
        COLOR_LIST_P2.append(shard_black)
        COLOR_LIST_P2.append(arrows_black)
    else:
        COLOR_LIST_P2 = (COLOR_TEAM2, COLOR_TIMER, COLOR_MANA_SHARD, COLOR_BG, shard, arrows)
        COLOR_LIST_P1 = [COLOR_NOTCLICK for i in range(len(COLOR_LIST_P2) - 2)]
        COLOR_LIST_P1.append(shard_black)
        COLOR_LIST_P1.append(arrows_black)


def draw_skill_1(side_turn):
    if side_turn == -1:
        player_list = RED_LIST
    else:
        player_list = BLUE_LIST

    row, column = title_to_swap_selected
    draw_list = [(row, column)]

    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            if 0 <= column + i <= COUNT_TITLE - 1 and 0 <= row + j <= COUNT_TITLE - 1:
                if data_model[column + i][row + j] in player_list and data_model[column + i][row + j] != \
                        data_model[column][row]:
                    draw_list.append([row + j, column + i])

    for i in range(-1, 2, 2):  # Шаг по x
        if 0 <= i + column <= COUNT_TITLE - 1:
            if data_model[column + i][row] in player_list and data_model[column + i][row] != data_model[column][row]:
                draw_list.append([row, column + i])

    for i in range(-1, 2, 2):  # Шаг по y
        if 0 <= i + row <= COUNT_TITLE - 1:
            if data_model[column][row + i] in player_list and data_model[column][row + i] != data_model[column][row]:
                draw_list.append([row + i, column])

    for i in draw_list:
        field_list[i[0]][i[1]].fill(COLOR_BG)
        screen.blit(field_list[i[0]][i[1]], (
            LEFT_MARGIN + MARGIN + i[0] * SIZE_TITLE, UPPER_MARGIN + 2 * MARGIN + i[1] * SIZE_TITLE, SIZE_TITLE,
            SIZE_TITLE))


def run_skill_1(pos, player):
    global title_to_swap_selected, data_model, side_turn, p1_skill_selected, p2_skill_selected, last_data, last_data_2, target_pos_skill_4, data_animation_swap, mana1, mana2

    data_model_copy = copy.deepcopy(data_model)

    if player == 1:
        team_list = RED_LIST
    else:
        team_list = BLUE_LIST

    x, y = pos
    if not (LEFT_MARGIN + MARGIN < x < SIZE[0] - RIGHT_MARGIN - MARGIN or y < UPPER_MARGIN + MARGIN):
        return None
    x, y = x - MARGIN - LEFT_MARGIN, y - 2 * MARGIN - UPPER_MARGIN
    row, column = x // SIZE_TITLE, y // SIZE_TITLE

    if not (data_model[column][row] in team_list):
        return

    if title_to_swap_selected == None:
        print("тайл выбран")
        title_to_swap_selected = (row, column)

    else:
        difference1 = title_to_swap_selected[0] - row
        difference2 = title_to_swap_selected[1] - column
        difference1 = abs(difference1)
        difference2 = abs(difference2)
        if difference1 < 2 and difference2 < 2 and difference1 + difference2 != 0 and data_model[column][row] != \
                data_model[title_to_swap_selected[1]][title_to_swap_selected[0]]:
            print("swap")

            if target_pos_skill_4 != None:  # Взаимодействие с скиллом 4
                if target_pos_skill_4[0] == row and target_pos_skill_4[1] == column:
                    target_pos_skill_4[0], target_pos_skill_4[1] = title_to_swap_selected[0], title_to_swap_selected[1]
                elif target_pos_skill_4[0] == title_to_swap_selected[0] and target_pos_skill_4[1] == \
                        title_to_swap_selected[1]:
                    target_pos_skill_4 = [row, column]

            data_model[column][row], data_model[title_to_swap_selected[1]][title_to_swap_selected[0]] = \
                data_model[title_to_swap_selected[1]][title_to_swap_selected[0]], data_model[column][row]

            data_animation_swap = copy.deepcopy(data_model)
            data_animation_swap[column][row], data_animation_swap[title_to_swap_selected[1]][
                title_to_swap_selected[0]] = 0, 0

            start_flash((LEFT_MARGIN + MARGIN + row * SIZE_TITLE - 50 + SIZE_TITLE // 2,
                         MARGIN + column * SIZE_TITLE - 50 + SIZE_TITLE // 2), \
                        (LEFT_MARGIN + MARGIN + title_to_swap_selected[0] * SIZE_TITLE - 50 + SIZE_TITLE // 2,
                         MARGIN + title_to_swap_selected[1] * SIZE_TITLE - 50 + SIZE_TITLE // 2))

            title_to_swap_selected = None
            side_turn *= -1
            last_data_2 = copy.deepcopy(last_data)
            last_data = copy.deepcopy(data_model_copy)
            p1_skill_selected = False
            p2_skill_selected = False

            if side_turn == 1:
                mana1 -= skill_list[p1_skill_draw][1]
            else:
                mana2 -= skill_list[p2_skill_draw][1]

        else:
            print("тайл сброшен")
            title_to_swap_selected = None


def run_skill_3(pos):
    global data_model, skill_3_selected, turn_in_spell_3, p1_skill_selected, p2_skill_selected, last_data, last_data_2, mana1, mana2

    x, y = pos

    if skill_3_selected and LEFT_MARGIN + MARGIN < x < SIZE[0] - RIGHT_MARGIN - MARGIN and MARGIN < y < SIZE[
        1] - MARGIN:
        data_model = last_data_2

        last_data = None
        last_data_2 = None

        if side_turn == -1:
            mana1 -= skill_list[p1_skill_draw][1]
        else:
            mana2 -= skill_list[p2_skill_draw][1]

        skill_3_selected = False
        turn_in_spell_3 = counter_turn
        p1_skill_selected = False
        p2_skill_selected = False
    else:
        skill_3_selected = True


def run_skill_4(pos, player):
    global skill_4_selected, p1_skill_selected, p2_skill_selected, target_pos_skill_4, start_pos_skill_4, counter_turns_skill_4, side_turn, mana1, mana2

    x, y = pos

    if player == -1:
        team_list = RED_LIST
    else:
        team_list = BLUE_LIST

    if skill_4_selected and (LEFT_MARGIN + MARGIN < x < SIZE[0] - MARGIN - RIGHT_MARGIN) and (
            MARGIN * 2 < y < SIZE[1] - MARGIN):

        x, y = x - MARGIN - LEFT_MARGIN, y - 2 * MARGIN - UPPER_MARGIN
        row, column = x // SIZE_TITLE, y // SIZE_TITLE

        if not (data_model[column][row] in team_list):
            skill_4_selected = False

            if player == -1:  # red
                p1_skill_selected = False

            else:  # blue
                p2_skill_selected = False
            return

        if side_turn == -1:
            mana1 -= skill_list[p1_skill_draw][1]
        else:
            mana2 -= skill_list[p2_skill_draw][1]

        start_pos_skill_4 = (row, column)
        target_pos_skill_4 = [row, column]
        counter_turns_skill_4 = 6
        skill_4_selected = False
        p1_skill_selected = False
        p2_skill_selected = False
        side_turn *= -1

    else:
        if skill_4_selected:
            skill_4_selected = False

            if player == -1:  # red
                p1_skill_selected = False

            else:  # blue
                p2_skill_selected = False
        else:
            skill_4_selected = True


def run_skill_2(pos, player):
    global skill_2_selected, p1_skill_selected, p2_skill_selected, counter_turns_skill_2, p1_skill_2_on, p2_skill_2_on, mana1, mana2
    x, y = pos

    print("yup")
    if skill_2_selected and (LEFT_MARGIN + MARGIN < x < SIZE[0] - MARGIN - RIGHT_MARGIN) and (
            MARGIN * 2 < y < SIZE[1] - MARGIN):

        x, y = x - MARGIN - LEFT_MARGIN, y - 2 * MARGIN - UPPER_MARGIN
        row, column = x // SIZE_TITLE, y // SIZE_TITLE
        counter_turns_skill_2 = 6

        if side_turn == -1:
            mana1 -= skill_list[p1_skill_draw][1]
        else:
            mana2 -= skill_list[p2_skill_draw][1]

        if player == -1:
            p1_skill_2_on = True
        else:
            p2_skill_2_on = True
        skill_2_selected = False
        p1_skill_selected = False
        p2_skill_selected = False


    else:
        if skill_2_selected:
            skill_2_selected = False

            if player == -1:  # red
                p1_skill_selected = False

            else:  # blue
                p2_skill_selected = False
        else:
            skill_2_selected = True


def run_skill_5(pos, player):
    global skill_5_selected, p1_skill_selected, p2_skill_selected, counter_turns_skill_5, mana1, mana2
    x, y = pos
    if skill_5_selected and (LEFT_MARGIN + MARGIN < x < SIZE[0] - MARGIN - RIGHT_MARGIN) and (
            MARGIN * 2 < y < SIZE[1] - MARGIN):

        if player == -1:
            models.pop(3)
            models.insert(3, pygame.image.load("image/models/king+_red.png"))
        else:
            models.pop(10)
            models.insert(10, pygame.image.load("image/models/king+_blue.png"))

        if side_turn == -1:
            mana1 -= skill_list[p1_skill_draw][1]
        else:
            mana2 -= skill_list[p2_skill_draw][1]

        print("spell")
        counter_turns_skill_5 = 6

        skill_5_selected = False
        p1_skill_selected = False
        p2_skill_selected = False


    else:
        if skill_5_selected:
            skill_5_selected = False

            if player == -1:  # red
                p1_skill_selected = False

            else:  # blue
                p2_skill_selected = False
        else:
            skill_5_selected = True


def start_boom(pos, player):
    global boom_pos_1, boom_pos_2, counter_tick

    if player == -1:
        boom_lst = boom_red
        boom_pos_1 = pos
    else:
        boom_lst = boom_blue
        boom_pos_2 = pos

    counter_tick = 0


def start_flash(pos1, pos2):
    global flash_pos_1, flash_pos_2, counter_tick_flash
    flash_pos_1 = pos1
    flash_pos_2 = pos2
    counter_tick_flash = 0


def end_screen(player):  # Экран концовки
    player *= -1
    if player == -1:
        player = "Красный игрок"
    else:
        player = "Синий игрок"
    print("win:", player)
    sys.exit()


# Настройки окна
COUNT_TITLE = 9
SIZE_TITLE = 100
MARGIN = 0  # Было 10
UPPER_MARGIN = 0
LEFT_MARGIN = 350
RIGHT_MARGIN = 350

POS_TIMER1 = (65, 150)
POS_NAME1 = (12, 20)
POS_SHARD1 = (165, 820)
POS_SKILL1 = (90, 570)

POS_TIMER2 = (1555, 150)
POS_SHARD2 = (1455, 820)

SPACE_SHARD_X = 10
ALPHA_PARAMETR = 100  # Прозрачно игрового поля

# Рассчёт размеров окна
SIZE = (LEFT_MARGIN + 2 * MARGIN + SIZE_TITLE * COUNT_TITLE + RIGHT_MARGIN,
        3 * MARGIN + SIZE_TITLE * COUNT_TITLE + UPPER_MARGIN)

# Загатовки палитры цветов
COLOR_ENEMY_TITLE = (255, 50, 50)
COLOR_TEST = (255, 122, 0)
COLOR_SELECT_WHITE = (0, 204, 0)
COLOR_SELECT_BLACK = (0, 102, 0)
COLOR_BG = (82, 183, 200)
COLOR_UPPER_MARGIN = (115, 115, 115)
COLOR_TITLE_FIRST = (39, 86, 68)
COLOR_TITLE_SECOND = (200, 200, 200)
COLOR_MANA_SHARD = (102, 108, 189)
COLOR_TIMER = (102, 255, 51)
COLOR_TEAM1 = (255, 0, 0)
COLOR_TEAM2 = (0, 0, 255)
COLOR_NOTCLICK = (140, 140, 140)
COLOR_BUFF = (255, 228, 160)

COLOR_LIST_P1 = None
COLOR_LIST_P2 = None

# Создание массива с тайлами поля
field_list = [[pygame.Surface((SIZE_TITLE, SIZE_TITLE)) for i in range(COUNT_TITLE)] for i in range(COUNT_TITLE)]

# Прозрачная поверхность для скиллов
off_skill = pygame.Surface((185, 229))
off_skill.fill((0, 0, 0))
off_skill.set_alpha(100)

# Прозрачная поверхность для скиллов
bg_skills = pygame.Surface((COUNT_TITLE * SIZE_TITLE + MARGIN, COUNT_TITLE * SIZE_TITLE + MARGIN))
bg_skills.fill(COLOR_BG)
bg_skills.set_alpha(25)

# Прозрачная поверхность выбранного
selected_skill = pygame.Surface((185, 229))
selected_skill.fill(COLOR_BG)
selected_skill.set_alpha(100)

# Координаты стрелок
arrows_pos_left_1 = (POS_SKILL1[0] - 75 + 7, POS_SKILL1[1] + 60 + 13)  # Левая стрелка 1
arrows_pos_right_1 = (POS_SKILL1[0] - 75 + 7 + 222 + 48, POS_SKILL1[1] + 60 + 13)  # Левая стрелка 2
arrows_pos_left_2 = (SIZE[0] - 180 - POS_SKILL1[0] - 75 + 7, POS_SKILL1[1] + 60 + 13)  # Правая стрелка 1
arrows_pos_right_2 = (SIZE[0] - 180 - POS_SKILL1[0] - 75 + 7 + 222 + 48, POS_SKILL1[1] + 60 + 13)  # Правая стрелка 2
SIZE_ARROWS = (48, 51)

# Настройка окна
screen = pygame.display.set_mode(SIZE)
# screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
pygame.display.set_caption("Chess")

# Размеры шрифтов
timer_size = 100
name_size = 60

# Настройка шрифта
courier = pygame.font.SysFont("courier", 36)
font_timer = pygame.font.Font('fonty.ttf', timer_size)
font_name = pygame.font.SysFont('arial', name_size)
font_mana = pygame.font.SysFont('arial', 35)
font_skill_name = pygame.font.SysFont('arial', 22)
font_discription = pygame.font.SysFont('arial', 25)

# Загрузка картинок
circle_model = pygame.image.load("image/circle.png")

name_models = [
    "spec2_red.png",  # 1-Красный дракон (слон + конь) +5
    "scout_red.png",  # 2-Красная рыба (конь++) +2
    "king_red.png",  # 3-Красный король
    "common_red.png",  # 4-Красная мышь (пешка) +1
    "huge_red.png",  # 5-Красная змея (ладья++) +3
    "jumper_red.png",  # 6-Красный паук (Scout) 0
    "spec1_red.png",  # 7-Красный волк (ладья + конь) +5
    "spec2_blue.png",  # 8-Синий дракон (слон + конь) +5
    "scout_blue.png",  # 9-Синяя рыба (конь++) +1
    "king_blue.png",  # 10-Синий король
    "common_blue.png",  # 11-Синяя мышь (пешка) +1
    "huge_blue.png",  # 12-Синяя змея (ладья++) +3
    "jumper_blue.png",  # 13-Синий паук (Scout) 0
    "spec1_blue.png",  # 14-Синий волк (ладья + конь) +5
]
models = [pygame.image.load("image/models/" + i) for i in name_models]
models.insert(0, "EMPTY")

# Цифровая модель поля
data_model = [

    [12, 13, 9, 14, 10, 8, 9, 13, 12],
    [11, 11, 11, 11, 11, 11, 11, 11, 11],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4],
    [5, 6, 2, 1, 3, 7, 2, 6, 5],

]

# Список тайлов с мышами (пешок) которые не ходили
not_started_RED = [(i, COUNT_TITLE - 2) for i in range(COUNT_TITLE)]
not_started_BLUE = [(i, 1) for i in range(COUNT_TITLE)]

# Выбранная ячейка
selected_title = None

# Чья сторона ходит
side_turn = -1  # -1-red, 1-blue

# Список номеров фигур белых и черных
BLUE_LIST = (8, 9, 10, 11, 12, 13, 14)
RED_LIST = (1, 2, 3, 4, 5, 6, 7)

# Счётчик фпс
FPS = 30
timer = pygame.time.Clock()

# Циферблат
timer_counter1 = 0
clock1 = 2100
timer_counter2 = 0
clock2 = 2100

# Скиллы
skills = [pygame.image.load(f"image/skills/skill{i}.png") for i in range(1, 6)]
skills.insert(0, pygame.image.load(f"image/skills/maket.png"))
arrows = pygame.image.load(f"image/skills/swap_skill.png")
arrows_black = pygame.image.load(f"image/skills/swap_skill_black.png")
discript1 = pygame.image.load(f"image/skills/test.png")

# Скилл 1 Рокировка
title_to_swap_selected = None

# Скилл 3 Назад во времени
skill_3_selected = False

# Скилл 2 Перегрузка
skill_2_selected = False
counter_turns_skill_2 = 0
p1_skill_2_on = False
p2_skill_2_on = False

# Скилл 4
skill_4_selected = False
counter_turns_skill_4 = 0
target_pos_skill_4 = None
start_pos_skill_4 = None

# Скилл 5
skill_5_selected = False
counter_turns_skill_5 = 0

# Какой скилл сейчас отрисовавается из списка
p1_skill_draw = 1
p2_skill_draw = 5

# Выбрал ли пользователь скилл
p1_skill_selected = False
p2_skill_selected = False

skill_list = [
    ["EMPTY"],
    [1, 2, "Рокировка", pygame.image.load("image/skills/test.png")],
    [2, 10, "Перегрузка", pygame.image.load("image/skills/test1.png")],
    [3, 15, "Назад во времени", pygame.image.load("image/skills/test2.png")],
    [4, 50, "Возвращение", pygame.image.load("image/skills/test3.png")],
    [5, 99, "Последний шанс", pygame.image.load("image/skills/test4.png")],
]

# Кристалл маны
mana1 = 252
mana2 = 102

# Переменные экономики
ROUND_GROW_MANA = 1  # Рост маны за ход
MAX_INCOME = 5  # Макс кол-во получаемой доп маны
PERIOD_INCOME = 10  # За каждые n доп мана

# Цена потери юнитов
COST_DRAGON = 5  # 1, 8
COST_SCOUT = 0  # 6, 13
COST_KING = 0  # 3, 10
COST_COMMON = 1  # 4, 11
COST_SNAKE = 3  # 5, 12
COST_JUMPER = 2  # 2, 9
COST_WOLF = 5  # 7, 14

shard = pygame.image.load('image/skills/shard_mana.png')
shard_black = pygame.image.load('image/skills/shard_mana_black.png')

# Анимация скиллов
ashes = [pygame.image.load(f'animation/ashes/{i}.png') for i in range(90)]
counter_2 = 0
ashes_pos = (-100, -100)
pos_animation_kill = None

stars = [pygame.image.load(f'animation/stars/{i}.png') for i in range(12)]
counter_3 = 0
stars_pos = (-100, -100)

boom_red = [pygame.image.load(f'animation/boom_red/{i}.png') for i in range(12)]
counter_boom_1 = 0
boom_pos_1 = (-500, -500)

boom_blue = [pygame.image.load(f'animation/boom_blue/{i}.png') for i in range(12)]
counter_boom_2 = 0
boom_pos_2 = (-500, -500)

flash = [pygame.image.load(f'animation/flash/{i}.png') for i in range(17)]
counter_flash = 0
flash_pos_1 = (-500, -500)
flash_pos_2 = (-500, -500)

# Настройка заднего фона
COUNT_ANIMATION_BG = 40
name_models_list = [f"{i}.png" for i in range(COUNT_ANIMATION_BG)]
bg_cadr = [pygame.image.load("image/bg/" + i) for i in name_models_list]
counter = 0

# Текущий ход
last_side_turn = side_turn
last_data = None
last_data_2 = None
data_animation_kill = None
data_animation_swap = None
turn_in_spell_3 = None
counter_turn = 0
counter_tick = None
counter_tick_flash = None

end_game = False
last_moved = False

# Цикл игры
while True:
    # Проверка взаимодействий с окном
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] < MARGIN * 2 or event.pos[1] > SIZE[
                1] - MARGIN or counter_tick != None or counter_tick_flash != None:  # Баг с нажатием под поле
                break
            if event.button == pygame.BUTTON_LEFT:
                if side_turn == -1 and not (p1_skill_selected):  # Перелистываение скиллов хода красных
                    if POS_SKILL1[0] <= event.pos[0] <= POS_SKILL1[0] + 185 and \
                            POS_SKILL1[1] <= event.pos[1] <= POS_SKILL1[1] + 229 and selected_title == None and mana1 >= \
                            skill_list[p1_skill_draw][1]:  # Скилл красного игрока
                        p1_skill_selected = True
                    elif arrows_pos_left_1[0] <= event.pos[0] <= arrows_pos_left_1[0] + SIZE_ARROWS[0] and \
                            arrows_pos_left_1[1] <= event.pos[1] <= arrows_pos_left_1[1] + SIZE_ARROWS[1]:  # Левая стрелка
                        p1_skill_draw -= 1 if p1_skill_draw != 1 else -4
                    elif arrows_pos_right_1[0] <= event.pos[0] <= arrows_pos_right_1[0] + SIZE_ARROWS[0] and \
                            arrows_pos_right_1[1] <= event.pos[1] <= arrows_pos_right_1[1] + SIZE_ARROWS[1]:  # Правая стрелка
                        p1_skill_draw += 1 if p1_skill_draw != 5 else -4
                elif side_turn == 1 and not (p2_skill_selected):  # Перелистываение скиллов хода синих
                    if SIZE[0] - 180 - POS_SKILL1[0] <= event.pos[0] <= SIZE[0] - 180 - POS_SKILL1[0] + 185 and \
                            POS_SKILL1[1] <= event.pos[1] <= POS_SKILL1[1] + 229 and selected_title == None and mana2 >= \
                            skill_list[p2_skill_draw][1]:  # Скилл синего игрока
                        p2_skill_selected = True
                    elif arrows_pos_left_2[0] <= event.pos[0] <= arrows_pos_left_2[0] + SIZE_ARROWS[0] and \
                            arrows_pos_left_2[1] <= event.pos[1] <= arrows_pos_left_2[1] + SIZE_ARROWS[1]:  # Левая стрелка
                        p2_skill_draw -= 1 if p2_skill_draw != 1 else -4
                    elif arrows_pos_right_2[0] <= event.pos[0] <= arrows_pos_right_2[0] + SIZE_ARROWS[0] and \
                            arrows_pos_right_2[1] <= event.pos[1] <= arrows_pos_right_2[1] + SIZE_ARROWS[1]:  # Правая стрелка
                        p2_skill_draw += 1 if p2_skill_draw != 5 else -4

                # Выбор фигуры на доске
                if not (p1_skill_selected or p2_skill_selected):
                    selected_title = select_title(event.pos)
                    print(selected_title)

                if ((p1_skill_selected and p1_skill_draw == 3) or (p2_skill_selected and p2_skill_draw == 3)) and (
                        last_data != None and last_data_2 != None):  # Скилл 4
                    run_skill_3(event.pos)

                # Скиллы 1 игрока
                if p1_skill_selected:
                    if p1_skill_draw == 1:  # Запуск метода скилла 1
                        run_skill_1(event.pos, 1)
                    elif p1_skill_draw == 4:  # Запуск метода скилла 4
                        if target_pos_skill_4 != None:
                            p1_skill_selected = False
                        else:
                            run_skill_4(event.pos, side_turn)
                    elif p1_skill_draw == 2:  # Запуск метода скилла 2
                        run_skill_2(event.pos, side_turn)
                    elif p1_skill_draw == 5:  # Запуск метода скилла 5
                        run_skill_5(event.pos, side_turn)

                # Скиллы 2 игрока
                if p2_skill_selected:
                    if p2_skill_draw == 1:  # Запуск метода скилла 1
                        run_skill_1(event.pos, 2)
                    elif p2_skill_draw == 4:  # Запуск метода скилла 4
                        if target_pos_skill_4 != None:
                            p1_skill_selected = False
                        else:
                            run_skill_4(event.pos, side_turn)
                    elif p2_skill_draw == 2:  # Запуск метода скилла 2
                        run_skill_2(event.pos, side_turn)
                    elif p2_skill_draw == 5:  # Запуск метода скилла 5
                        run_skill_5(event.pos, side_turn)

            if event.button == pygame.BUTTON_RIGHT:
                title_to_swap_selected = None
                p1_skill_selected = False
                p2_skill_selected = False
                skill_2_selected = False
                skill_3_selected = False
                skill_4_selected = False
                skill_5_selected = False
                if selected_title != None:
                    move_model(event.pos)
    # Отрисовка объектов
    if target_pos_skill_4 != None:  # Рассчёт места пылинок
        if counter_tick != None:
            pos_list = pos_animation_kill
        elif counter_tick_flash != None:
            pos_list = (-100, -100)
        else:
            pos_list = target_pos_skill_4
        ashes_pos = (LEFT_MARGIN + MARGIN + pos_list[0] * SIZE_TITLE, 2 * MARGIN + pos_list[1] * SIZE_TITLE)
    else:
        ashes_pos = (-100, -100)

    screen.blit(bg_cadr[counter], (0, 0))

    counter += 1
    if counter == 40:
        counter = 0  # Фон

    counter_2 += 1
    if counter_2 == 90:  # Анимация зелёных пылинок
        counter_2 = 0

    counter_3 += 1
    if counter_3 == 12:  # Анимация зелёных пылинок
        counter_3 = 0

    if counter_tick != None and counter_tick % 3 == 0:
        counter_boom_1 += 1
    if counter_boom_1 == 12:  # Анимация красного взрыва
        counter_boom_1 = 0

    if counter_tick != None and counter_tick % 3 == 0:
        counter_boom_2 += 1
    if counter_boom_2 == 12:  # Анимация синего взрыва
        counter_boom_2 = 0

    if counter_tick_flash != None and counter_tick_flash % 2 == 0:
        counter_flash += 1  # Анимация вспышки
    if counter_flash == 17:
        counter_flash = 0

    if skill_3_selected or skill_2_selected or skill_5_selected:
        screen.blit(bg_skills, (LEFT_MARGIN + MARGIN - MARGIN // 2, UPPER_MARGIN + 2 * MARGIN - MARGIN // 2))

    draw_field()  # Клетки поля

    if selected_title != None:  # Закрасить выбранную фигуру
        paint_tile()
        paint_cicrles()

    if title_to_swap_selected != None:  # Подсвечивание фигуры для свапа
        draw_skill_1(side_turn)

    draw_models(data_model)  # Отрисовка фигур

    choose_side_turn(side_turn)  # Отрисовка цветов ходящего

    draw_timer(0)  # Отрисовка циферблата 1
    draw_timer(1)  # Отрисовка циферблата 2

    if p2_skill_selected:
        screen.blit(selected_skill, (SIZE[0] - 180 - POS_SKILL1[0], POS_SKILL1[1]))
    if p1_skill_selected:
        screen.blit(selected_skill, POS_SKILL1)

    # Имя игрока
    text_name1 = font_name.render("Красный флот", False, COLOR_LIST_P1[0])
    text_name2 = font_name.render("Синий флот", False, COLOR_LIST_P2[0])
    screen.blit(text_name1, (LEFT_MARGIN // 2 - text_name1.get_size()[0] // 2, 20))  # Отрисовка имени игрока 1
    screen.blit(text_name2, (1620 - LEFT_MARGIN // 2 - text_name2.get_size()[0] // 2, 20))  # Отрисовка имени игрока 2

    draw_manaShard(0)  # Отрисовка запаса маны
    draw_manaShard(1)  # Отрисовка запаса маны

    draw_skill(0, skill_list[p1_skill_draw][0], skill_list[p1_skill_draw][1], skill_list[p1_skill_draw][2],
               skill_list[p1_skill_draw][3])  # Отрисовка скилла # type, skill, manacost, name, desript
    draw_skill(1, skill_list[p2_skill_draw][0], skill_list[p2_skill_draw][1], skill_list[p2_skill_draw][2],
               skill_list[p2_skill_draw][3])  # Отрисовка скилла # type, skill, manacost, name, desript

    if side_turn == -1:  # Отрисовка затемнения скиллов не ходящего
        screen.blit(off_skill, (SIZE[0] - 180 - POS_SKILL1[0], POS_SKILL1[1]))
    else:
        screen.blit(off_skill, POS_SKILL1)

    # Рассчёт циферблата 1
    timer_counter1 += 1
    if timer_counter1 % FPS == 0:
        if side_turn == -1:
            clock1 -= 1
            if clock1 == 0:
                end_game = True
        timer_counter1 = 0

    # Рассчёт циферблата 2
    timer_counter2 += 1
    if timer_counter2 % FPS == 0:
        if side_turn == 1:
            clock2 -= 1
            if clock2 == 0:
                print(side_turn)
                end_game = True
        timer_counter2 = 0

    if side_turn != last_side_turn:
        last_side_turn = side_turn
        counter_turn += 1
        if side_turn == 1 and last_moved:
            mana1 += mana1 // PERIOD_INCOME if mana1 // PERIOD_INCOME <= MAX_INCOME else MAX_INCOME
            mana1 += ROUND_GROW_MANA
        elif side_turn == -1 and last_moved:
            mana2 += mana2 // PERIOD_INCOME if mana2 // PERIOD_INCOME <= MAX_INCOME else MAX_INCOME
            mana2 += ROUND_GROW_MANA

        last_moved = False

        if counter_turns_skill_4 != 0 and target_pos_skill_4 != None:
            counter_turns_skill_4 -= 1
            if counter_turns_skill_4 == 0:
                if data_model[start_pos_skill_4[1]][start_pos_skill_4[0]] == 0:
                    data_model[start_pos_skill_4[1]][start_pos_skill_4[0]], data_model[target_pos_skill_4[1]][
                        target_pos_skill_4[0]] = \
                        data_model[target_pos_skill_4[1]][target_pos_skill_4[0]], data_model[start_pos_skill_4[1]][
                            start_pos_skill_4[0]]
                else:
                    if data_model[start_pos_skill_4[1]][start_pos_skill_4[0]] in RED_LIST:
                        parametr = -1
                    else:
                        parametr = 1

                    data_animation_kill = copy.deepcopy(data_model)
                    data_animation_kill[start_pos_skill_4[1]][start_pos_skill_4[0]] = 0
                    pos_animation_kill = (target_pos_skill_4[0], target_pos_skill_4[1])

                    data_model[start_pos_skill_4[1]][start_pos_skill_4[0]], data_model[target_pos_skill_4[1]][
                        target_pos_skill_4[0]] = \
                        data_model[target_pos_skill_4[1]][target_pos_skill_4[0]], 0
                    start_boom((LEFT_MARGIN + MARGIN + start_pos_skill_4[0] * SIZE_TITLE - 50 + SIZE_TITLE // 2,
                                MARGIN + start_pos_skill_4[1] * SIZE_TITLE - 50 + SIZE_TITLE // 2), parametr)
                target_pos_skill_4 = None

        if counter_turns_skill_2 != 0:
            print(counter_turns_skill_2, "ходов с ускорением")
            counter_turns_skill_2 -= 1
            if counter_turns_skill_2 == 0:
                p1_skill_2_on = False
                p2_skill_2_on = False

        if counter_turns_skill_5 != 0:
            print(counter_turns_skill_5, "---===---")
            counter_turns_skill_5 -= 1
            if counter_turns_skill_5 == 0:
                models.pop(3)
                models.insert(3, pygame.image.load("image/models/king_red.png"))
                models.pop(10)
                models.insert(10, pygame.image.load("image/models/king_blue.png"))

        print(counter_turn, "ХОД НОМЕР")

    screen.blit(boom_red[counter_boom_1], boom_pos_1)
    screen.blit(boom_blue[counter_boom_2], boom_pos_2)
    screen.blit(flash[counter_flash], flash_pos_1)
    screen.blit(flash[counter_flash], flash_pos_2)
    screen.blit(ashes[counter_2], ashes_pos)
    screen.blit(stars[counter_3], stars_pos)

    if counter_tick != None:
        counter_tick += 1
        if counter_tick == 33:
            counter_tick = None
            counter_boom_1 = 0
            counter_boom_2 = 0
            boom_pos_1 = (-500, -500)
            boom_pos_2 = (-500, -500)

    if counter_tick_flash != None:
        counter_tick_flash += 1
        if counter_tick_flash == 33:
            counter_tick_flash = None
            counter_flash = 0
            flash_pos_1 = (-500, -500)
            flash_pos_2 = (-500, -500)

    if end_game and counter_tick_flash == None and counter_tick == None:
        end_screen(side_turn)

    # Обновление дисплея
    pygame.display.flip()
    timer.tick(FPS)
