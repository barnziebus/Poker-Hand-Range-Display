import pygame as py

class ComboCell:
    def __init__(
            self,
            position,
            size,
            border_width,
            bg_col_suited,
            bg_col_unsuited,
            bg_col_pairs,
            fill_percentage_1, fill_percentage_1_col,
            fill_percentage_2, fill_percentage_2_col,
            selected_col,
            highlighted_col,
            text,
            text_col,
            selected_text_col,
            text_font,
            text_size,
    ):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.size = size
        self.w = size[0]
        self.h = size[1]
        self.border_w = border_width

        self.bg_col = [0,0,0]
        self.bg_col_suited = bg_col_suited
        self.bg_col_unsuited = bg_col_unsuited
        self.bg_col_pairs = bg_col_pairs

        self.fill_pct_1 = fill_percentage_1
        self.fill_pct_2 = fill_percentage_2
        self.fill_pct_1_col = fill_percentage_1_col
        self.fill_pct_2_col = fill_percentage_2_col
        self.selc_col = selected_col # greyed out when selected (fold col)
        self.highl_col = highlighted_col

        self.selected = False
        self.selected_state = 0 #0 = unselected; 1 = fill 1; 2 = fill2
        self.selected_for_range = False

        self.text = text
        self.text_col = text_col
        self.selexted_text_col = selected_text_col
        self.text_font = py.font.SysFont(text_font, text_size)

    def DrawCell(self, screen):
        self.SetCellCol()
        ## Draw the cell: starting with the highlighted border, then bg col, then fill 1 and fill 2
        # Draw the cell border when the cell is selected
        if self.selected:
            py.draw.rect(
                surface=screen,
                color=self.highl_col,
                rect=[self.x - self.border_w, self.y - self.border_w, self.w + self.border_w * 2, self.h + self.border_w * 2]
            )
        if self.selected_state == 1:
            py.draw.circle(
                surface=screen,
                color=self.fill_pct_1_col,
                center=[self.x + self.w / 3, self.y - (self.border_w + 4)],
                radius=4
            )
        if self.selected_state == 2:
            py.draw.circle(
                surface=screen,
                color=self.fill_pct_2_col,
                center=[self.x + ((self.w / 3) * 2), self.y - (self.border_w + 4)],
                radius=4
            )
        # Draw the cell background
        py.draw.rect(
            surface=screen,
            color=self.bg_col,
            rect=[self.position, self.size]
        )
        # Draw the background if selected and has some percentage indicator within
        if self.selected_for_range or self.fill_pct_1 > 0 or self.fill_pct_2 > 0:
            py.draw.rect(
                surface=screen,
                color=self.selc_col,
                rect=[self.x, self.y, self.w, self.h]
            )
        # Draw the first percentage filled section of the cell
        py.draw.rect(
            surface=screen,
            color=self.fill_pct_1_col,
            rect=[self.x, self.y, self.w * self.fill_pct_1, self.h]
        )
        py.draw.rect(
            surface=screen,
            color=self.fill_pct_2_col,
            rect=[self.x, self.y, self.w * self.fill_pct_2, self.h]
        )
        ## Draw Text
        # create text surface and set the col dependant on selection
        if self.fill_pct_1 > 0 or self.fill_pct_2 > 0 or self.selected_for_range:
            text_surface = self.text_font.render(self.text, True, self.selexted_text_col)
        else:
            text_surface = self.text_font.render(self.text, True, self.text_col)
        # get the center position
        text_rect = text_surface.get_rect(center=(self.x+(self.w/2),self.y+(self.h/2)))
        # render the text surface to the center positions
        screen.blit(text_surface, text_rect)

    def SelectCell(self):
        # highlight cell on mouse over (click comes from event loop)
        mouse_position = py.mouse.get_pos()
        if self.x <= mouse_position[0] <= self.x + self.w and self.y <= mouse_position[1] <= self.y + self.h:
            self.selected_state += 1
            if self.selected_state > 2:
                self.selected_state = 0

            if self.selected_state == 0:
                self.selected = False
            else:
                self.selected = True

    def SelectCellForRange(self):
        mouse_position = py.mouse.get_pos()
        if self.x <= mouse_position[0] <= self.x + self.w and self.y <= mouse_position[1] <= self.y + self.h:
            if self.selected_for_range:
                self.selected_for_range = False
            else:
                self.selected_for_range = True

    def DeselectCell(self):
        self.selected = False
        self.selected_for_range = False
        self.selected_state = 0

    def IncPercentage(self, scrolling):
        if scrolling:
            inc_speed = 0.04
        elif not scrolling:
            inc_speed = 0.001
        if self.selected_state == 1:
            self.fill_pct_1 += inc_speed
            if self.fill_pct_1 >= 1:
                self.fill_pct_1 = 1

        elif self.selected_state == 2:
            self.fill_pct_2 += inc_speed
            if self.fill_pct_2 >= 1:
                self.fill_pct_2 = 1

    def DecPercentage(self, scrolling):
        if scrolling:
            inc_speed = 0.04
        elif not scrolling:
            inc_speed = 0.001
        if self.selected_state == 1:
            self.fill_pct_1 -= inc_speed
            if self.fill_pct_1 <= 0:
                self.fill_pct_1 = 0

        elif self.selected_state == 2:
            self.fill_pct_2 -= inc_speed
            if self.fill_pct_2 <= 0:
                self.fill_pct_2 = 0

    def SetCellCol(self):
        if self.x == self.y:
            self.bg_col = self.bg_col_pairs
        if self.x > self.y:
            self.bg_col = self.bg_col_suited
        if self.x < self.y:
            self.bg_col = self.bg_col_unsuited

    def ActiveCell(self):
        if self.fill_pct_1 > 0 or self.fill_pct_2 > 0:
            return True
        else:
            return False

    def CountCombos(self):
        if self.ActiveCell():
            if self.text[-1] == 's':
                return 4
            elif self.text[-1] == 'o':
                return 12
            else:
                return 6
        else:
            return 0