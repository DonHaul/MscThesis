



%assign initial pcs
Rcell = {}
tcell = {}
count=1

for i=1:4
   


  %virginpcs{end+1}=ptCloud
   
  Rcell{end+1}= generatenoiseR(0.1)
  tcell{end+1}=[0 0 0 ]'
  
  
  count=count+1
  
end
%%
%pcs = virgincopy
%%
pcs = {pcs{1},pcs{1},pcs{1},pcs{1}}
%%
mergeshow(pcs)
%%
tranfpc = tranformpcs(pcs,Rcell,tcell)
%%
mergeshow(tranfpc)
%%


V= formatpcs(tranfpc')'

%%

%pcs={pcs{3},pcs{3},pcs{3},pcs{3}}

M = max(size(pcs))
tcell=tcell'
Rcell=Rcell'
pcs=pcs'

Rcellz = {eye(3),eye(3),eye(3),eye(3)}'
tcellz = {[0,0,0]',[0,0,0]',[0,0,0]',[0,0,0]'}'



V= formatpcs(pcs)'

 


% %%% optionally work with less points, donwnsample the point-sets by a factor df >1
df=2; % df=1 means no downsampling
[V,I] = cellfun(@(V) deal(V(1:df:end,1:3)',double(V(1:df:end,4:6))/255),V,'uniformoutput',false);


%%
addpath('JRMPC_v0.9.4')



%Xin=pcs{1}

% initialize centers, the median cardinality can also be used as K but 
% it will dramatically increase the computational complexity without 
%  substantial gain in performance. Higher K can be combined with point-set
%  downsampling to avoid high complexity
%K = 10000;
K = ceil(0.5*median(cellfun(@(V) size(V,2),V))); 

% sample the unit sphere, by randomly selecting azimuth / elevation angles.
az = 2*pi*rand(1,K);
el = 2*pi*rand(1,K);

% (unit) polar to cartesian conversion.
Xin = [cos(az).*cos(el); sin(el); sin(az).*cos(el)];
Xin = Xin% make them have the same order with points (it helps the convergence)


% choose the middle pointset instead to initialize the cluster centers
Xin = V{2}(:,unique(round(linspace(1,size(V{2},2),K))));

% Number of Iterations.
maxNumIter = 30;
 

% call jrmpc to do the actual compuation, 
fprintf('Joint registration...(it takes a few minutes with full sets).\n');
[R,t,X,S,a] = jrmpc(V,Xin,'maxNumIter',maxNumIter,'gamma',0.1,'R',Rcellz,'t',tcellz);

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
%%
% visualize with color the finals with outliers removed
figure(2)
hold on
title('Registration after removing points classified on clusters with high variance','fontweight','bold','fontsize',12)

cellfun(@(TVref,Iref) scatter3(TVref(1,:),TVref(2,:),TVref(3,:),7,Iref,'filled'),TVrefined,Irefined);

set(2,'position',get(1,'position')+[+580 0 0 0]);

view([0 -70])
hold off

%%
 mergeshow(tranfpc)
 %%
 figure
 
 
%  
  
  tranf1pc = tranformpcs(pcs,R,t)
  mergeshow(tranf1pc)
%      
    
    