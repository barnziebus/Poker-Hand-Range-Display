import pygame as py
import Combo_Cell


py.init()
py.font.init()

SCREEN_SIZE = 750, 800
SCREEN = py.display.set_mode(SCREEN_SIZE)

combo_list = []
TOTAL_COMBOS = 1326

CELL_SIZE = [50,50]
BORDER_WIDTH = 2
BACKGROUND_COL_SUITED = [245, 175, 122]
BACKGROUND_COL_UNSUITED = [180, 225, 250]
BACKGROUND_COL_PAIRS = [255, 248, 107]
fill_percentage_1 = 0
FILL_PERCENTAGE_1_COL = [181, 16, 16]
fill_percentage_2 = 0
FILL_PERCENTAGE_2_COL = [22, 16, 181]
RANGE_SELECTED_COL = [92, 92, 92]
HIGHLIGHTED_COL = [121, 255, 43]
TEXT_COL = [0,0,0]
TEXT_FONT = 'bahnschrift'
TEXT_SIZE = 22

TEXT_LIST = [
    ['AA', 'AKo', 'AQo', 'AJo', 'ATo', 'A9o', 'A8o', 'A7o', 'A6o', 'A5o', 'A4o', 'A3o', 'A2o',],
    ['AKs', 'KK', 'KQo', 'KJo', 'KTo', 'K9o', 'K8o', 'K7o', 'K6o', 'K5o', 'K4o', 'K3o', 'K2o',],
    ['AQs', 'KQs', 'QQ', 'QJo', 'QTo', 'Q9o', 'Q8o', 'Q7o', 'Q6o', 'Q5o', 'Q4o', 'Q3o', 'Q2o',],
    ['AJs', 'KJs', 'QJs', 'JJ', 'JTo', 'J9o', 'J8o', 'J7o', 'J6o', 'J5o', 'J4o', 'J3o', 'J2o',],
    ['ATs', 'KTs', 'QTs', 'JTs', 'TT', 'T9o', 'T8o', 'T7o', 'T6o', 'T5o', 'T4o', 'T3o', 'T2o',],
    ['A9s', 'K9s', 'Q9s', 'J9s', 'T9s', '99', '98o', '97o', '96o', '95o', '94o', '93o', '92o',],
    ['A8s', 'K8s', 'Q8s', 'J8s', 'T8s', '98s', '88', '87o', '86o', '85o', '84o', '83o', '82o',],
    ['A7s', 'K7s', 'Q7s', 'J7s', 'T7s', '97s', '87s', '77', '76o', '75o', '74o', '73o', '72o',],
    ['A6s', 'K6s', 'Q6s', 'J6s', 'T6s', '96s', '86s', '76s', '66', '65o', '64o', '63o', '62o',],
    ['A5s', 'K5s', 'Q5s', 'J5s', 'T5s', '95s', '85s', '75s', '65s', '55', '54o', '53o', '52o',],
    ['A4s', 'K4s', 'Q4s', 'J4s', 'T4s', '94s', '84s', '74s', '64s', '54s', '44', '43o', '42o',],
    ['A3s', 'K3s', 'Q3s', 'J3s', 'T3s', '93s', '83s', '73s', '63s', '53s', '43s', '33', '32o',],
    ['A2s', 'K2s', 'Q2s', 'J2s', 'T2s', '92s', '82s', '72s', '62s', '52s', '42s', '32s', '22',],
]


# Instance each cell in the grid
for x in range(13):
    inner_list = []
    for y in range(13):
        inner_list.append(Combo_Cell.ComboCell(
            position=[x * 55 + 20, y * 55 + 20],
            size=CELL_SIZE,
            border_width=BORDER_WIDTH,
            bg_col_suited=BACKGROUND_COL_SUITED,
            bg_col_unsuited=BACKGROUND_COL_UNSUITED,
            bg_col_pairs=BACKGROUND_COL_PAIRS,
            fill_percentage_1=fill_percentage_1,
            fill_percentage_1_col=FILL_PERCENTAGE_1_COL,
            fill_percentage_2=fill_percentage_2,
            fill_percentage_2_col=FILL_PERCENTAGE_2_COL,
            selected_col=RANGE_SELECTED_COL,
            highlighted_col=HIGHLIGHTED_COL,
            text=TEXT_LIST[x][y],
            text_col=TEXT_COL,
            selected_text_col=[255,255,255],
            text_font=TEXT_FONT,
            text_size=TEXT_SIZE
                    )
        )
    combo_list.append(inner_list)

combo_count = 0



print(combo_count)

running = True
while running:
    ## User Inputs and call-out actions
    # mouse actions
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONUP:
            if event.button == 1:
                for combo in combo_list:
                    for i in combo:
                        i.SelectCell()
            if event.button == 3:
                for combo in combo_list:
                    for i in combo:
                        i.SelectCellForRange()
        if event.type == py.MOUSEBUTTONDOWN:
            if event.button == 4:
                for combo in combo_list:
                    for i in combo:
                        i.IncPercentage(scrolling=True)
            if event.button == 5:
                for combo in combo_list:
                    for i in combo:
                        i.DecPercentage(scrolling=True)
    # key actions
    pressed_keys = py.key.get_pressed()
    if pressed_keys[py.K_RIGHT]:
        for combo in combo_list:
            for i in combo:
                i.IncPercentage(scrolling=False)
    if pressed_keys[py.K_LEFT]:
        for combo in combo_list:
            for i in combo:
                i.DecPercentage(scrolling=False)
    if pressed_keys[py.K_ESCAPE]:
        for combo in combo_list:
            for i in combo:
                i.DeselectCell()

    ## Program Logic
    # count combos of selected hands
    combo_count = 0
    for combo in combo_list:
        for i in combo:
            combo_count += i.CountCombos()

    ## Draw to screen
    # set background
    SCREEN.fill([255, 255, 255])
    # draw the cells to screen by calling the draw methods of each instance
    for combo in combo_list:
        for i in combo:
            i.DrawCell(SCREEN)
    # draw the number of combos text to screen
    text_font = py.font.SysFont(TEXT_FONT, TEXT_SIZE)
    text_surface = text_font.render(f'Combinations: {combo_count} of {TOTAL_COMBOS} hands. ({round(combo_count/TOTAL_COMBOS,3)*100}% of hands)', True, TEXT_COL)
    SCREEN.blit(text_surface, [50,750])

    py.display.update()

py.quit()