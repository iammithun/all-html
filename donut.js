const theta_spacing = 0.07;
const phi_spacing = 0.02;

const R1 = 1;
const R2 = 2;
const K2 = 5;

// Set screen dimensions
const screen_width = 80;  // example screen width
const screen_height = 40;  // example screen height

const K1 = screen_width * K2 * 3 / (8 * (R1 + R2));

function render_frame(A, B) {
    const cosA = Math.cos(A);
    const sinA = Math.sin(A);
    const cosB = Math.cos(B);
    const sinB = Math.sin(B);

    const output = Array.from(Array(screen_height), () => Array(screen_width).fill(' '));
    const zbuffer = Array.from(Array(screen_height), () => Array(screen_width).fill(0));

    for (let theta = 0; theta < 2 * Math.PI; theta += theta_spacing) {
        const costheta = Math.cos(theta);
        const sintheta = Math.sin(theta);

        for (let phi = 0; phi < 2 * Math.PI; phi += phi_spacing) {
            const cosphi = Math.cos(phi);
            const sinphi = Math.sin(phi);

            const circlex = R2 + R1 * costheta;
            const circley = R1 * sintheta;

            const x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB;
            const y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB;
            const z = K2 + cosA * circlex * sinphi + circley * sinA;
            const ooz = 1 / z;

            const xp = Math.floor(screen_width / 2 + K1 * ooz * x);
            const yp = Math.floor(screen_height / 2 - K1 * ooz * y);

            const L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi);

            if (L > 0) {
                if (0 <= xp && xp < screen_width && 0 <= yp && yp < screen_height && ooz > zbuffer[yp][xp]) {
                    zbuffer[yp][xp] = ooz;
                    const luminance_index = Math.floor(L * 8);
                    const bounded_index = Math.max(0, Math.min(luminance_index, 11));  // Ensure index is in the range 0-11
                    const luminance_chars = ".,-~:;=!*#$@";
                    output[yp][xp] = luminance_chars[bounded_index];
                }
            }
        }
    }

    console.clear();
    for (let j = 0; j < screen_height; j++) {
        console.log(output[j].join(''));
    }
}

// Example usage: Rotate the torus over time
let A = 0;
let B = 0;
setInterval(() => {
    render_frame(A, B);
    A += 0.04;
    B += 0.02;
}, 30);
