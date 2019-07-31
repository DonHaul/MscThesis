function [cleanpcs] = cleanPCnans(virginpcs)



n = max(size(virginpcs))



cleanpcs={}
j=1
for j=1:n
    
    
k = find(~isnan(virginpcs{j}.Location(:,1)));

pcxyz=virginpcs{j}.Location(k,:);
pcrgb=virginpcs{j}.Color(k,:);

    
   cleanpcs{j}=pointCloud(pcxyz,'Color',pcrgb); 
end


end