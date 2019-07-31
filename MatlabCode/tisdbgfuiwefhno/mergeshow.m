function [mergedpc] = mergeshow(virginpcs)
mergedpc=virginpcs{1};

for i=2:size(virginpcs,2)
    mergedpc = pcmerge(mergedpc,virginpcs{i},0.001);
end

figure
pcshow(mergedpc)


end
