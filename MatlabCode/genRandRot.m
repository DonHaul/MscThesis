function [R] = genRandRot()

angles = rand(3)*360-180

angle=angles(1)
Rx = [1 0 0; 0 cos(angle) -sin(angle); 0 sin(angle) cos(angle)]
angle=angles(2)
Ry = [cos(angle) 0 sin(angle); 0 1 0; -sin(angle) 0 cos(angle)]
angle=angles(3)
Rz = [cos(angle) -sin(angle) 0; sin(angle) cos(angle) 0; 0 0 1]

R=Rx*Ry*Rz


end