function [formattedpcs] = formatpcs(pcs)

formattedpcs={}

for i =1:size(pcs,1)
    
  colors=double(pcs{i}.Color);

  
  
  size(pcs)
      
  size(colors)
      
  formattedpcs{end+1} =horzcat(pcs{i}.Location,colors)
  
end

end