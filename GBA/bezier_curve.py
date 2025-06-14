import math
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class BezierCurve:
    def __init__(self, x_points, y_points):
        self.x_points = x_points
        self.y_points = y_points
        if len(self.x_points) == len(self.y_points):
            self.n = len(x_points) - 1
        self.t_values = np.linspace(0, 1, 100)

    def binomial(self, n, i):
        """
        Calculate the binomial coefficient C(n, i).
        
        Parameters:
        - n (int): Total number of items.
        - i (int): Number of items to choose.
        
        Returns:
        - int: Binomial coefficient C(n, i).
        """
        return math.factorial(n) / (math.factorial(i) * math.factorial(n - i))

    def calculate_bezier(self, t):
        """
        Calculate the Bezier curve value at parameter t.
        
        Parameters:
        - t (float): Parameter value between 0 and 1.
        
        Returns:
        - tuple: Tuple containing x and y coordinates of the Bezier curve for that t.
        """
        result_x, result_y = 0, 0
        for i in range(self.n + 1):
            coefficient = self.binomial(self.n, i) * (1 - t) ** (self.n - i) * t ** i
            result_x += self.x_points[i] * coefficient
            result_y += self.y_points[i] * coefficient
        return result_x, result_y

    def get_cardinal_coordinates(self):
        """
        Generate the cardinal coordinates of the Bezier curve values.
        
        Parameters:
        
        Returns:
        - list: List of tuples containing Bezier curve coordinates for each t in t_values.
        """
        bezier_values = [self.calculate_bezier(t) for t in self.t_values]
        bezier_values_x, bezier_values_y = list(zip(*bezier_values))
        x_interp = sorted([x ** 1.5 for x in np.linspace(0, 1, 100)])
        y_interp = np.interp(x_interp, bezier_values_x, bezier_values_y)
        return x_interp, y_interp


if __name__ == '__main__':

        # Example usage:
        n = 5
        x_points = [0, 0.2, 0.4, 0.8, 1]
        y_points = [0, -0.2, -0.15, -0.05, 0]

        bezier_curve = BezierCurve(x_points, y_points)
        bezier_coordinates = bezier_curve.get_cardinal_coordinates()

        # Plot lines between control points
        plt.plot(x_points, y_points, color='gray', linestyle='--', label='Control Lines')

        # Plot points (x, y)
        plt.scatter(x_points, y_points, color='red', label='Control Points')

        # Plot the generated spline
        plt.plot(bezier_coordinates[0], bezier_coordinates[1], color='blue', label='Bezier Curve')

        # Set aspect ratio to equal
        plt.axis('equal')

        plt.title('Bezier Curve with Control Points and Lines')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)
        plt.show()

