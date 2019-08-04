function [R] = generatenoiseR(noise)
    %generate noise
    a = rand(3,1)*noise

    %make it have 0 mean
    b =ones(3,1)*(noise/2)
    angle=a-b

    %convert to radians
    degtorad(angle)
    

    %x angle rotation matrix
    Rx = [1,0,0;0,cos(angle(1)),-sin(angle(1));0,sin(angle(1)),cos(angle(1))]
    %y angle rotation matrix
    Ry = [cos(angle(2)),0,sin(angle(2));0,1,0;-sin(angle(2)),0,cos(angle(2))]
    %z angle rotation matrix
    Rz = [cos(angle(3)),-sin(angle(3)),0;sin(angle(3)),cos(angle(3)),0;0,0,1] 

    %mount the final rotation
    R = Rx*Ry*Rz

    end