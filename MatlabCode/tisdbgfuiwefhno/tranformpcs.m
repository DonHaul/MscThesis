function [transformedpcs] = tranformpcs(pcs,R,t)

transformedpcs={}

for i =1:size(pcs,2)
    pts = pcs{i}.Location;
    color = pcs{i}.Color; 

    pts = R{i} * pts'+t{i};
    
    transformedpcs{i} = pointCloud(pts','Color',color);


end


end