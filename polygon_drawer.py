import tkinter as tk
import math
from math import sqrt
from polygon_triangulation import *


class PolygonDrawer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1200, height=600, bg="ivory")
        self.canvas.pack()
        self.label = tk.Label(root, text="")
        self.label.pack()
        self.points_pgn1 = []
        self.points_pgn2 = []
        self.drawing_pgn1 = True
        self.drawing_pgn2 = False
        self.is_animation = False

        self.canvas.create_polygon(0, 0, outline="blue", width=3, fill="", tag="pgn1")
        self.canvas.create_polygon(0, 0, outline="red", width=3, fill="", tag="pgn2")

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Motion>", self.show_live_polygon)

    def animation(self):
        def area_calculation(triangles):
            area = 0
            for triangle in triangles:
                area += 0.5 * (
                    triangle[0][0] * (triangle[1][1] - triangle[2][1])
                    + triangle[1][0] * (triangle[2][1] - triangle[0][1])
                    + triangle[2][0] * (triangle[0][1] - triangle[1][1])
                )
            return abs(area)

        def enlargement(polygon, coef):
            new_polygon = []
            point_0 = polygon[0]
            for point in polygon:
                vec_x = point[0] - point_0[0]
                vec_y = point[1] - point_0[1]
                new_polygon.append(
                    (point_0[0] + vec_x * coef, point_0[1] + vec_y * coef)
                )
            return new_polygon

        def move_triangle():
            self.canvas.move("pgn2_triangle0", 0, 5)  # Move the triangle 5 pixels down
            self.canvas.update()  # Update the canvas to show the new position
            if (
                self.canvas.coords("pgn2_triangle0")[3] < self.canvas.winfo_height()
            ):  # Check if the triangle has reached the center
                self.canvas.after(
                    20, move_triangle
                )  # Schedule the next animation frame after 20 milliseconds

        # Plasticizing the poligones in the upper corners.
        x_min_pgn1 = min(self.points_pgn1)[0]
        y_min_pgn1 = min(self.points_pgn1, key=lambda point: point[1])[1]

        self.points_pgn1 = [
            (x_point + 30 - x_min_pgn1, y_point + 30 - y_min_pgn1)
            for x_point, y_point in self.points_pgn1
        ]
        self.canvas.coords(
            "pgn1", [coord for point in self.points_pgn1 for coord in point]
        )

        x_max_pgn2 = max(self.points_pgn2)[0]
        y_min_pgn2 = min(self.points_pgn2, key=lambda point: point[1])[1]

        self.points_pgn2 = [
            (
                x_point + self.canvas.winfo_width() - 30 - x_max_pgn2,
                y_point + 30 - y_min_pgn2,
            )
            for x_point, y_point in self.points_pgn2
        ]
        self.canvas.coords(
            "pgn2", [coord for point in self.points_pgn2 for coord in point]
        )

        triangulation_pgn1 = triangulate_polygon(self.points_pgn1)
        triangulation_pgn2 = triangulate_polygon(self.points_pgn2)
        # print(triangulation_pgn1)
        # print(triangulation_pgn2)

        A_pgn1 = area_calculation(triangulation_pgn1)
        A_pgn2 = area_calculation(triangulation_pgn2)
        # print(A_pgn1, A_pgn2)
        if A_pgn1 < A_pgn2:
            # print("points pgn2 :", self.points_pgn2)
            coef_enlargement = sqrt(A_pgn1 / A_pgn2)
            self.points_pgn2 = enlargement(self.points_pgn2, coef_enlargement)
            x_max_pgn2 = max(self.points_pgn2)[0]
            y_min_pgn2 = min(self.points_pgn2, key=lambda point: point[1])[1]

            self.points_pgn2 = [
                (
                    x_point + self.canvas.winfo_width() - 30 - x_max_pgn2,
                    y_point + 30 - y_min_pgn2,
                )
                for x_point, y_point in self.points_pgn2
            ]
            self.canvas.coords(
                "pgn2", [coord for point in self.points_pgn2 for coord in point]
            )
            # print("points new pgn 2 :", self.points_pgn2)
            triangulation_pgn2 = triangulate_polygon(self.points_pgn2)
        elif A_pgn1 > A_pgn2:
            # print("points pgn 1 :", self.points_pgn1)
            coef_enlargement = sqrt(A_pgn2 / A_pgn1)
            self.points_pgn1 = enlargement(self.points_pgn1, coef_enlargement)

            x_min_pgn1 = min(self.points_pgn1)[0]
            y_min_pgn1 = min(self.points_pgn1, key=lambda point: point[1])[1]

            self.points_pgn1 = [
                (x_point + 30 - x_min_pgn1, y_point + 30 - y_min_pgn1)
                for x_point, y_point in self.points_pgn1
            ]

            self.canvas.coords(
                "pgn1", [coord for point in self.points_pgn1 for coord in point]
            )
            # print("points new pgn 1 :", self.points_pgn1)

            triangulation_pgn1 = triangulate_polygon(self.points_pgn1)

        self.canvas.itemconfigure("pgn1", width=1)
        self.canvas.itemconfigure("pgn2", width=1)

        for triangle_idx in range(len(triangulation_pgn1)):
            self.canvas.create_polygon(
                triangulation_pgn1[triangle_idx],
                outline="white",
                width=1,
                fill="blue",
                tag=f"pgn1_triangle{triangle_idx}",
            )
        for triangle_idx in range(len(triangulation_pgn2)):
            self.canvas.create_polygon(
                triangulation_pgn2[triangle_idx],
                outline="white",
                width=1,
                fill="red",
                tag=f"pgn2_triangle{triangle_idx}",
            )

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
        elif self.is_animation is False:
            self.canvas.unbind("<Button-1>")
            # self.canvas.unbind("<Motion>")
            self.is_animation = True
            self.animation()
        x, y = event.x, event.y
        self.label.config(text=f"X: {x}, Y: {y}")

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
