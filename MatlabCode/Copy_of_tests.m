
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
  
  
  
  
  mergedpc=virginpcs{1};

for i=2:5
    mergedpc = pcmerge(mergedpc,virginpcs{i},0.001);
end

pcshow(mergedpc)

    
 %%
  
  
  
  
  
  size(pcs)
      
  size(colors)
      
  pcs{end+1} =horzcat(ptCloud.Location,colors)


  
  Rcell{end+1}=squeeze(R(count,:,:))
  tcell{end+1}=t(count,:)'
  
  
  count=count+1
end


M = 5
tcell=tcell'
Rcell=Rcell'
pcs=pcs'
%% 

V=pcs


% %%% optionally work with less points, donwnsample the point-sets by a factor df >1
df=2; % df=1 means no downsampling
[V,I] = cellfun(@(V) deal(V(1:df:end,1:3)',double(V(1:df:end,4:6))/255),V,'uniformoutput',false);



addpath('JRMPC_v0.9.4')



%Xin=pcs{1}

% initialize centers, the median cardinality can also be used as K but 
% it will dramatically increase the computational complexity without 
%  substantial gain in performance. Higher K can be combined with point-set
%  downsampling to avoid high complexity
K = 10000;
%K = ceil(0.5*median(cellfun(@(V) size(V,2),V))); 

% sample the unit sphere, by randomly selecting azimuth / elevation angles.
az = 2*pi*rand(1,K);
el = 2*pi*rand(1,K);

% (unit) polar to cartesian conversion.
Xin = [cos(az).*cos(el); sin(el); sin(az).*cos(el)];
Xin = Xin*1% make them have the same order with points (it helps the convergence)


% choose the middle pointset instead to initialize the cluster centers
% Xin = V{5}(:,unique(round(linspace(1,size(V{5},2),K))));

% Number of Iterations.
maxNumIter = 2;
 

% call jrmpc to do the actual compuation, 
fprintf('Joint registration...(it takes a few minutes with full sets).\n');
[R,t,X,S,a] = jrmpc(V,Xin,'maxNumIter',maxNumIter,'gamma',0.2, 'epsilon', 1e-5,'R',Rcell,'t',tcell);

% apply transformation to each view V{j} as R{j}*V{j}+t{j}*ones(1,Nj). Then
% segment each TV{j} into an 1 x Nj cell array with 3 x 1 vectors. This allows
% calling plot3 with the corresponding color for each point
TV = cellfun(@(V,R,t) bsxfun(@plus,R*V,t),V,R,t,'uniformoutput',false);
%%
% visualize the final result of the registration.
fprintf('ploting...(it takes some time with full sets).\n');

figure(1)
hold on
title(sprintf('Final registration of %d TOF images',M),'fontweight','bold','fontsize',12)

%scatter3(TV{1}(1,:),TV{1}(2,:),TV{1}(3,:),7,I{1},'filled')

cellfun(@(TV,I) scatter3(TV(1,:),TV(2,:),TV(3,:),7,I,'filled'),TV(1:M),I(1:M));

set(1,'position',get(1,'position')+[-260 0 0 0]);

view([0 -70])
hold off

% use S and a to detect and remove unreliable points
[TVrefined,~,~,Irefined] = removePointsAndCenters(TV,X,S,a,I);

% visualize with color the finals with outliers removed
figure(2)
hold on
title('Registration after removing points classified on clusters with high variance','fontweight','bold','fontsize',12)

cellfun(@(TVref,Iref) scatter3(TVref(1,:),TVref(2,:),TVref(3,:),7,Iref,'filled'),TVrefined,Irefined);

set(2,'position',get(1,'position')+[+580 0 0 0]);

view([0 -70])
hold off

%%
transformedpcs={}

for i =1:5
    pts = virginpcs{i}.Location;
    color = virginpcs{i}.Color; 

    pts = R{i} * pts'+t{i};
    
    transformedpcs{i} = pointCloud(pts','Color',color);

    pcshow(transformedpcs{i});
end


%%
mergedpc=transformedpcs{1};

for i=2:5
    mergedpc = pcmerge(mergedpc,transformedpcs{i},0.001);
end

pcshow(mergedpc)

    
    
    