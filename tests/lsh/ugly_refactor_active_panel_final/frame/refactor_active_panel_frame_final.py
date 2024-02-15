from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from common.utility import get_project_root
from opengl_battle_field_card.card import Card
from opengl_rectangle_lightning_border.lightning_border import LightningBorder
from opengl_shape.rectangle import Rectangle


class PickingCardLightningBorderWithActivePanelFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.unit_card_list = []
        self.active_panel_rectangle = None
        self.selected_object = None
        self.prev_selected_object = None
        self.drag_start = None

        self.lightning_border = LightningBorder()

        print("Picking Action LightningBorder2")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        first_unit = Card(local_translation=(100, 100))
        first_unit.init_card(6)

        self.unit_card_list.append(first_unit)

        second_unit = Card(local_translation=(400, 400))
        second_unit.init_card(8)

        self.unit_card_list.append(second_unit)

        self.bind("<B1-Motion>", self.on_canvas_drag)
        self.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.bind("<Button-1>", self.on_canvas_left_click)
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-3>", self.on_canvas_right_click)

    def initgl(self):
        print("Initializing OpenGL")

        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        for unit_card in self.unit_card_list:
            tool_card = unit_card.get_tool_card()
            tool_card.set_visible(not tool_card.get_visible())

            pickable_unit_card = unit_card.get_pickable_card_base()
            attached_shape_list = pickable_unit_card.get_attached_shapes()
            print(f"attached shape: {attached_shape_list}")

            for attached_shape in attached_shape_list:
                print(f"attached shape: {attached_shape.vertices}")

            equipped_mark = attached_shape_list[1]
            current_status = equipped_mark.get_visible()
            print(f"current visible status: {current_status}")
            equipped_mark.set_visible(not equipped_mark.get_visible())

        self.redraw()

    def set_projection_matrix(self):
        glViewport(0, 0, self.winfo_reqwidth(), self.winfo_reqheight())
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winfo_reqwidth(), 0, self.winfo_reqheight())
        glMatrixMode(GL_MODELVIEW)

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for unit_card in self.unit_card_list:
            attached_tool_card = unit_card.get_tool_card()
            attached_tool_card.draw()

            pickable_unit_card_base = unit_card.get_pickable_card_base()
            pickable_unit_card_base.draw()

            attached_shape_list = pickable_unit_card_base.get_attached_shapes()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        if self.selected_object:
            pickable_unit_card_base = self.selected_object.get_pickable_card_base()

            self.lightning_border.set_padding(50)
            self.lightning_border.update_shape(pickable_unit_card_base)
            self.lightning_border.draw_lightning_border()

        if self.active_panel_rectangle:
            self.active_panel_rectangle.draw()

        self.tkSwapBuffers()

    def on_canvas_drag(self, event):
        x, y = event.x, event.y
        y = self.winfo_reqheight() - y

        if self.selected_object and self.drag_start:
            print(f"selected_object: {self.selected_object}")
            pickable_unit = self.selected_object.get_pickable_card_base()
            print(f"pickable_unit: {pickable_unit}")

            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            print(f"dx = {dx}, dy = {dy}")
            print(f"drag_start: {self.drag_start}")
            dy *= -1

            print(f"pickable local translation: {pickable_unit.get_local_translation()}")

            for vx, vy in pickable_unit.vertices:
                print(f"vx = {vx}, vy = {vy}")

            new_vertices = [
                (vx + dx, vy + dy) for vx, vy in pickable_unit.vertices
            ]
            pickable_unit.update_vertices(new_vertices)

            tool_card = self.selected_object.get_tool_card()
            new_tool_card_vertices = [
                (vx + dx, vy + dy) for vx, vy in tool_card.vertices
            ]
            tool_card.update_vertices(new_tool_card_vertices)

            for attached_shape in pickable_unit.get_attached_shapes():
                new_attached_shape_vertices = [
                    (vx + dx, vy + dy) for vx, vy in attached_shape.vertices
                ]
                attached_shape.update_vertices(new_attached_shape_vertices)

            self.drag_start = (x, y)
            self.redraw()

    def on_canvas_release(self, event):
        self.drag_start = None

    def on_canvas_left_click(self, event):
        try:
            x, y = event.x, event.y
            y = self.winfo_reqheight() - y

            for unit_card in self.unit_card_list:
                if isinstance(unit_card, Card):
                    unit_card.selected = False

            self.selected_object = None

            for unit_card in reversed(self.unit_card_list):
                print("find selected Pickable Rectangle")
                pickable_unit_card_base = unit_card.get_pickable_card_base()

                if pickable_unit_card_base.is_point_inside((x, y)):
                    print(f"pickable_unit_card_base.is_point_inside(x, y) pass")
                    unit_card.selected = not unit_card.selected
                    self.selected_object = unit_card
                    self.drag_start = (x, y)
                    print(f"Selected PickableRectangle at ({x}, {y})")
                    print(f"vertices: {pickable_unit_card_base.vertices[0][0]}, "
                          f"{pickable_unit_card_base.vertices[0][1]}, "
                          f"{pickable_unit_card_base.vertices[2][0]}, "
                          f"{pickable_unit_card_base.vertices[2][1]}")

                    if self.selected_object != self.prev_selected_object:
                        self.active_panel_rectangle = None
                        self.prev_selected_object = self.selected_object

                    break

            self.redraw()

        except Exception as e:
            print(f"Exception in on_canvas_click: {e}")

    def on_canvas_right_click(self, event):
        x, y = event.x, event.y

        if self.selected_object:
            print("check on_canvas_right_click")
            convert_y = self.winfo_reqheight() - y
            pickable_unit_card_base = self.selected_object.get_pickable_card_base()
            if pickable_unit_card_base.is_point_inside((x, convert_y)):
                print("Right click inside the selected card area")
                new_rectangle = self.create_opengl_rectangle((x, y))
                print(f"New rectangle: {new_rectangle}")
                self.active_panel_rectangle = new_rectangle

        self.redraw()

    def create_opengl_rectangle(self, start_point):
        rectangle_size = 50
        rectangle_color = (1.0, 0.0, 0.0, 1.0)

        end_point = (start_point[0] + rectangle_size, start_point[1] + rectangle_size)

        new_rectangle = Rectangle(rectangle_color, [
            (start_point[0], start_point[1]),
            (end_point[0], start_point[1]),
            (end_point[0], end_point[1]),
            (start_point[0], end_point[1])
        ])
        new_rectangle.created_by_right_click = True
        return new_rectangle
