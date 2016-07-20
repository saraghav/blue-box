function derivative = dcursor_points(p1, p2)

dy = p2.Position(2) - p1.Position(2);
dx = p2.Position(1) - p1.Position(1);

derivative = dy/dx;