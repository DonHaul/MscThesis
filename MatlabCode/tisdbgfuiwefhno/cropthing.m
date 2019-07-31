
fullpath='.\Logs\2019-07-25_16_26_25_pigeon'
path= strcat(fullpath ,'\PCs\PC_8\')

posepath =  strcat(fullpath,'\poses.mat')
load(posepath)


%% for everycmera
pcs = {}
Rcell = {}
tcell = {}

count=1

virginpcs={}

count=1
for str = camnames'
    
   pcpath= strcat(path,str','.pcd')
   ptCloud = pcread(pcpath )
  
   virginpcs{count}=ptCloud
  %figure
   %pcshow(ptCloud)
    %figure
   %pcshow(ptCloud)
  if size(ptCloud.Color,1)==0
      colors=zeros(size(ptCloud.Location));
      disp('ho')
  else
      disp('hey')
      colors=double(ptCloud.Color);
  end
  
  count=count+1
  
end


%%




