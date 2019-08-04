function [transformedpcs] = tranformpcs(pcs,R,t)

transformedpcs={};

for i =1:max(size(pcs))

    pts = pcs{i}.Location;
    color = pcs{i}.Color; 

    pts = R{i} * pts'+t{i};
    disp("spps")
    transformedpcs{i} = pointCloud(pts','Color',color);


end


end