import math
import numpy as np

theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5

# Set screen dimensions
screen_width = 80  # example screen width
screen_height = 40  # example screen height

K1 = screen_width * K2 * 3 / (8 * (R1 + R2))

def render_frame(A, B):
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    output = np.full((screen_height, screen_width), ' ')
    zbuffer = np.zeros((screen_height, screen_width))

    for theta in np.arange(0, 2 * math.pi, theta_spacing):
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        for phi in np.arange(0, 2 * math.pi, phi_spacing):
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            if L > 0:
                if 0 <= xp < screen_width and 0 <= yp < screen_height and ooz > zbuffer[yp, xp]:
                    zbuffer[yp, xp] = ooz
                    luminance_index = int(L * 8)
                    luminance_index = max(0, min(luminance_index, 11))  # Ensure index is in the range 0-11
                    output[yp, xp] = ".,-~:;=!*#$@"[luminance_index]

    print("\x1b[H", end='')
    for row in output:
        print("".join(row))

# Example usage: Rotate the torus over time
import time
A = 0
B = 0
while True:
    render_frame(A, B)
    A += 0.04
    B += 0.02
    time.sleep(0.03)
