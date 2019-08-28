import numpy as np
import scipy.io



mat = scipy.io.loadmat('globalIcpOut.mat')


print(mat['R'][0,:].shape)



%creates all H
for k=1:length(R)-1

for i=1:length(pcs)
    H(1:4,1:4,k,i)=eye(4);
    H(1:3,1:3,k,i)=R{i,k};
    H(1:3,4,k,i)=t{i,k};
end
end
%%
%merges all H
% last index is pc index
mergedH = repmat(eye(4),1,1,4)

for k=1:length(R)-1

for i=1:length(pcs)
    mergedH(:,:,i)= H(:,:,k,i) * mergedH(:,:,i)
end
end
