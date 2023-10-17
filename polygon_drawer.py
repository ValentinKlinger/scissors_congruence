import tkinter as tk
from math import sqrt
from polygon_triangulation import *


class PolygonDrawer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=600, bg="ivory")
        self.canvas.pack()
        self.points_pgn1 = []
        self.points_pgn2 = []
        self.drawing_pgn1 = True
        self.drawing_pgn2 = False

        self.canvas.create_polygon(0, 0, outline="blue", width=3, fill="", tag="pgn1")
        self.canvas.create_polygon(0, 0, outline="red", width=3, fill="", tag="pgn2")

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Motion>", self.show_live_polygon)

    def animation(self):
        triangulation_pgn1 = triangulate_polygon(self.points_pgn1)
        triangulation_pgn2 = triangulate_polygon(self.points_pgn2)
        # print(triangulation_pgn1)
        # print(triangulation_pgn2)
        for triangle in triangulation_pgn1:
            self.canvas.create_polygon(triangle, outline="black", width=1, fill="")
        for triangle in triangulation_pgn2:
            self.canvas.create_polygon(triangle, outline="black", width=1, fill="")

    def show_live_polygon(self, event):
        """
        Show the live polygone with current coordinates and mouse's position.
        """

        if self.drawing_pgn1:
            x, y = event.x, event.y
            if len(self.points_pgn1) > 1:
                polygon_points = self.points_pgn1 + [(x, y)]
                self.canvas.coords(
                    "pgn1", [coord for point in polygon_points for coord in point]
                )
        elif self.drawing_pgn2:
            x, y = event.x, event.y
            if len(self.points_pgn2) > 1:
                polygon_points = self.points_pgn2 + [(x, y)]
                self.canvas.coords(
                    "pgn2", [coord for point in polygon_points for coord in point]
                )
        else:
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Motion>")
            self.animation()

    def add_point(self, event):
        """
        Add a new point to the list of points when user left click.
        """
        if self.drawing_pgn1:
            x, y = event.x, event.y

            if (
                len(self.points_pgn1) != 0
                and sqrt(
                    (x - self.points_pgn1[0][0]) ** 2
                    + (y - self.points_pgn1[0][1]) ** 2
                )
                < 20
            ):  # if the user has finished drawing the polygon
                self.drawing_pgn1 = False
                self.drawing_pgn2 = True
                yellow_circle = self.canvas.find_withtag("yellow_circle")
                self.canvas.delete(yellow_circle)
                self.canvas.coords(
                    "pgn1", [coord for point in self.points_pgn1 for coord in point]
                )

            else:
                self.points_pgn1.append((x, y))
                if len(self.points_pgn1) == 1:  # If it's the first point.
                    self.canvas.create_oval(
                        self.points_pgn1[0][0] - 20,
                        self.points_pgn1[0][1] - 20,
                        self.points_pgn1[0][0] + 20,
                        self.points_pgn1[0][1] + 20,
                        fill="#F6FF66",
                        width=0,
                        tag="yellow_circle",
                    )
                    self.canvas.tag_lower("yellow_circle")

        elif self.drawing_pgn2:
            x, y = event.x, event.y

            if (
                len(self.points_pgn2) != 0
                and sqrt(
                    (x - self.points_pgn2[0][0]) ** 2
                    + (y - self.points_pgn2[0][1]) ** 2
                )
                < 20
            ):  # if the user has finished drawing the polygon
                self.drawing_pgn2 = False
                yellow_circle = self.canvas.find_withtag("yellow_circle")
                self.canvas.delete(yellow_circle)
                self.canvas.coords(
                    "pgn2", [coord for point in self.points_pgn2 for coord in point]
                )

            else:
                self.points_pgn2.append((x, y))
                if len(self.points_pgn2) == 1:  # If it's the first point.
                    self.canvas.create_oval(
                        self.points_pgn2[0][0] - 20,
                        self.points_pgn2[0][1] - 20,
                        self.points_pgn2[0][0] + 20,
                        self.points_pgn2[0][1] + 20,
                        fill="#F6FF66",
                        width=0,
                        tag="yellow_circle",
                    )
                    self.canvas.tag_lower("yellow_circle")


def main():
    root = tk.Tk()
    root.title("Polygon Drawer")
    app = PolygonDrawer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
