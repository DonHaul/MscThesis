function [newspocs] = untitled2(pcs,threshold)


newpcs={};

i=1;

for i=1:size(pcs,2)
pts=pcs{i}.Location;

K= find(pts(:,3)<threshold);


pts=pts(K,:);
color=pcs{i}.Color(K,:);
newspocs{i}=pointCloud(pts,'Color',color);


end

