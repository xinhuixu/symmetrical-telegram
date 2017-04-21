from display import *
from matrix import *
from math import *
from V import *

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(points, x0, y0, z0)
    add_point(points, x1, y1, z1)
    add_point(points, x2, y2, z2)

def draw_polygons( matrix, screen, color ):
    if len(matrix) % 3 != 0:
        if len(matrix) < 3:
            print "NEED AT LEAST 3 POINTS TO DRAW POLYGONS"
        else:
            print "bad matrix length: not divisible by 3"
        return
    
    def draw_a_polygon(p0, p1, p2):
        draw_line(p0[0], p0[1],
                  p1[0], p1[1], screen, color)
        draw_line(p1[0], p1[1],
                  p2[0], p2[1], screen, color)
        draw_line(p2[0], p2[1],
                  p0[0], p0[1], screen, color)
        
    point = 0
    view_v = [0, 0, 1]
    
    while point < len(matrix) - 1:
        p0 = matrix[point]
        p1 = matrix[point+1]
        p2 = matrix[point+2]

        surf_norm = cross_prod( v_minus(p1, p0), v_minus(p2, p0) )
        if dot_prod(surf_norm, view_v) < 0:
            draw_a_polygon(p0, p1, p2)
        '''
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        draw_line( int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   int(matrix[point+2][0]),
                   int(matrix[point+2][1]),
                   screen, color)    
        draw_line(  int(matrix[point+2][0]),
                   int(matrix[point+2][1]),
                   int(matrix[point][0]),
                   int(matrix[point][1]),
                   screen, color)
        '''
        point+= 3
    

def add_box( points, x, y, z, w, h, d ):
    def add_f(x0,y0,z0,x1,y1,z1,x2,y2,z2,x3,y3,z3):
        add_polygon(points, x0,y0,z0,  x1,y1,z1,  x2,y2,z2)
        add_polygon(points, x0,y0,z0,  x2,y2,z2,  x3,y3,z3)
    add_f(x  ,y  ,z  ,  x+w,y  ,z  ,  x+w,y+h,z  ,  x  ,y+h,z  )#F
    add_f(x  ,y  ,z+d,  x  ,y  ,z  ,  x  ,y+h,z  ,  x  ,y+h,z+d)#L
    add_f(x+w,y  ,z+d,  x  ,y  ,z+d,  x  ,y+h,z+d,  x+w,y+h,z+d)#B
    add_f(x+w,y  ,z  ,  x+w,y  ,z+d,  x+w,y+h,z+d,  x+w,y+h,z  )#R
    add_f(x  ,y  ,z+d,  x+w,y  ,z+d,  x+w,y  ,z  ,  x  ,y  ,z  )#U
    add_f(x  ,y+h,z+d  ,x  ,y+h,z  ,  x+w,y+h,z  ,  x+w,y+h,z+d)#D
    '''
    x1 = x + width
    y1 = y - height
    z1 = z - depth
    #FRONT
    add_polygon(points, x, y, z, x, y1, z, x1, y1, z)
    add_polygon(points, x, y, z, x1, y1, z, x1, y, z)
    #BACK
    add_polygon(points, x, y, z1, x, y1, z1, x1, y1, z1)
    add_polygon(points, x, y, z1, x1, y1, z1, x1, y, z1)
    #LEFT
    add_polygon(points, x, y, z1, x, y1, z1, x, y1, z)
    add_polygon(points, x, y, z1, x, y1, z, x, y, z)
    #RIGHT
    add_polygon(points, x1, y, z, x1, y1, z, x1, y1, z1)
    add_polygon(points, x1, y1, z1, x1, y, z1, x1, y, z)
    #TOP
    add_polygon(points, x, y, z1, x, y, z, x1, y, z)
    add_polygon(points, x, y, z1, x1, y, z, x1, y, z1)
    #BOTTOM
    add_polygon(points, x, y1, z1, x, y1, z, x1, y1, z)
    add_polygon(points, x, y1, z1, x1, y1, z, x1, y1, z1)
    '''
def add_sphere( edges, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps

    num_steps+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            index = lat * num_steps + longt
            sphere = len(points)
            p0 = points[index] #top point
            p1 = points[(index+num_steps)%sphere] #point below top point
            p2 = points[(index+num_steps+1)%sphere] #point right to p1
            p3 = points[(index+1)%sphere] #point right to p0

            add_polygon(edges, p0[0], p0[1], p0[2],
                        p1[0], p1[1], p1[2],
                        p2[0], p2[1], p2[2])
            add_polygon(edges, p2[0], p2[1], p2[2],
                        p3[0], p3[1], p3[2],
                        p0[0], p0[1], p0[2])

def generate_sphere( cx, cy, cz, r, step ):
    points = [] #step=0.01 #num_step=100
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps #i create 101 points in a "ring"
            
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop+1):
            circ = step * circle

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points
        
def add_torus( edges, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)
    num_steps = int(1/step+0.1)
    
    lat_start = 0
    lat_stop = num_steps
    longt_start = 0
    longt_stop = num_steps
    
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):
            index = lat * num_steps + longt

            sphere = len(points)
            p0 = points[index]
            p1 = points[(index+1)%sphere]
            p2 = points[(index+num_steps)%sphere] 
            p3 = points[(index+num_steps+1)%sphere] 


            add_polygon(edges, p1[0], p1[1], p1[2],
                        p2[0], p2[1], p2[2],
                        p0[0], p0[1], p0[2])
            add_polygon(edges, p2[0], p2[1], p2[2],
                        p1[0], p1[1], p1[2],
                        p3[0], p3[1], p3[2])

def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    num_steps = int(1/step+0.1)
    
    rot_start = 0
    rot_stop = num_steps
    circ_start = 0
    circ_stop = num_steps

    print num_steps
    
    for rotation in range(rot_start, rot_stop):
        rot = step * rotation
        for circle in range(circ_start, circ_stop):
            circ = step * circle

            x = math.cos(2*math.pi*rot) * (r0 * math.cos(2*math.pi*circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi*rot) * (r0 * math.cos(2*math.pi*circ) + r1) + cz;

            points.append([x, y, z])
    return points

def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    t = step

    while t <= 1.00001:
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        t+= step

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    t = step
    while t <= 1.00001:
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]
                
        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)
    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
