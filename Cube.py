import math, time, sys, shutil

def main():
    sys.stdout.write('\x1b[?25l')
    
    R = [i * 0.04 for i in range(-25, 26)]
    points = [(v, x, y, c) for v, c in [(-1,'.'), (1,'~')] for x in R for y in R] + \
             [(x, v, y, c) for v, c in [(-1,'@'), (1,'+')] for x in R for y in R] + \
             [(x, y, v, c) for v, c in [(-1,'$'), (1,';')] for x in R for y in R]

    A = B = C = offset = 0.0
    W, H = shutil.get_terminal_size((80, 24))
    cx, cy, vx, vy = W / 2, H / 2, 2.0, 1.0 
    mx, my = 28, 14                         

    sys.stdout.write('\x1b[2J\x1b[3J\x1b[H') 
    sys.stdout.flush()
    
    try:
        while True:
            curr_size = shutil.get_terminal_size((80, 24))
            if curr_size.columns != W or curr_size.lines != H:
                W, H = curr_size.columns, curr_size.lines
                sys.stdout.write('\x1b[2J\x1b[3J\x1b[H') 
                sys.stdout.flush() 

            b, zb = [' '] * (W * H), [-9999.0] * (W * H) 

            try:
                cx += vx; cy += vy
                if cx <= mx or cx >= W - mx: vx, cx = -vx, max(mx, min(cx, W - mx))
                if cy <= my or cy >= H - my: vy, cy = -vy, max(my, min(cy, H - my))

                sA, cA, sB, cB = math.sin(A), math.cos(A), math.sin(B), math.cos(B)
                sC, cC = math.sin(C), math.cos(C)
                
                xx, xy, xz = cB*cC, sA*sB*cC - cA*sC, cA*sB*cC + sA*sC
                yx, yy, yz = cB*sC, sA*sB*sC + cA*cC, cA*sB*sC - sA*cC
                zx, zy, zz = -sB,   sA*cB,            cA*cB

                for px, py, pz, c in points:
                    z3 = max(px*zx + py*zy + pz*zz + 5, 0.01) 
                    oz = 1.0 / z3
                    
                    xp = int(cx + (px*xx + py*xy + pz*xz) * oz * 48) 
                    yp = int(cy + (px*yx + py*yy + pz*yz) * oz * 24) 
                    
                    if 0 <= xp < W and 0 <= yp < H:
                        idx = xp + yp * W
                        if oz > zb[idx]:
                            zb[idx], b[idx] = oz, c

            except Exception:
                cx, cy = W / 2.0, H / 2.0
                A = B = C = 0.0
                sys.stdout.write('\x1b[2J') 
                continue 

            sys.stdout.write('\x1b[H') 
            screen = []
            for i in range(H):
                row, base_hue = [], i * 0.05 + offset
                for j in range(W):
                    c = b[j + i * W]
                    if c != ' ':
                        h = base_hue + j * 0.1
                        r = int(math.sin(h)*127+128)
                        g = int(math.sin(h+2.094)*127+128)
                        b_col = int(math.sin(h+4.188)*127+128)
                        row.append(f"\x1b[38;2;{r};{g};{b_col}m{c}\x1b[0m")
                    else:
                        row.append(' ')
                screen.append(''.join(row))

            sys.stdout.write('\n'.join(screen))
            sys.stdout.flush()

            A, B, C = A + 0.03, B + 0.04, C + 0.01
            offset -= 0.15
            time.sleep(0.03)

    except KeyboardInterrupt:
        sys.stdout.write('\x1b[0m\x1b[?25h\nAnimation stopped.\n')

if __name__ == '__main__':
    main()