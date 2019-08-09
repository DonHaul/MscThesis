close all

load("..\Logs\2019-07-31_19_56_31_weasel\poses.mat")
load("./pcs-31-Jul-20191.mat")


auxpcs = pcs
pcs={auxpcs{1},auxpcs{4},auxpcs{2},auxpcs{3}}

%assign initial pcs
Rcell = {}
tcell = {}
count=1

for i=1:4
   


  %virginpcs{end+1}=ptCloud
   
  %Rcell{end+1}= eye(3) %generatenoiseR(0.1)
  %tcell{end+1}=[0 0 0 ]'
  Rcell{end+1}=squeeze(R(count,:,:))
  tcell{end+1}=t(count,:)'
  
  count=count+1
  
end


pcs = croppc(pcs,1.3);

tranfpc = tranformpcs(pcs,Rcell,tcell);

i=2
j=3

%mergeshow({tranfpc{i}})
%mergeshow({tranfpc{j}})
%mergeshow({tranfpc{i},tranfpc{j}})
%figure

%tranfpc = {tranfpc{i},tranfpc{j}}
%pcs = {pcs{i},pcs{j}}

V= formatpcs(tranfpc')'



%pcs={pcs{3},pcs{3},pcs{3},pcs{3}}

M = max(size(pcs))
tcell=tcell'
Rcell=Rcell'
pcs=pcs'

Rcellz = {eye(3),eye(3),eye(3),eye(3)}'
tcellz = {[0,0,0]',[0,0,0]',[0,0,0]',[0,0,0]'}'




 


% %%% optionally work with less points, donwnsample the point-sets by a factor df >1
df=2; % df=1 means no downsampling
[V,I] = cellfun(@(V) deal(V(1:df:end,1:3)',double(V(1:df:end,4:6))/255),V,'uniformoutput',false);



addpath('JRMPC_v0.9.4')



%Xin=pcs{1}

% initialize centers, the median cardinality can also be used as K but 
% it will dramatically increase the computational complexity without 
%  substantial gain in performance. Higher K can be combined with point-set
%  downsampling to avoid high complexity
%K = 10000;
K = 17000%ceil(0.5*median(cellfun(@(V) size(V,2),V))); 

% sample the unit sphere, by randomly selecting azimuth / elevation angles.
az = 2*pi*rand(1,K);
el = 2*pi*rand(1,K);

% (unit) polar to cartesian conversion.
Xin = [cos(az).*cos(el); sin(el); sin(az).*cos(el)];
Xin = Xin*0.8% make them have the same order with points (it helps the convergence)


% choose the middle pointset instead to initialize the cluster centers
Xin = V{1}(:,unique(round(linspace(1,size(V{1},2),K))));

% Number of Iterations.
maxNumIter = 30;
 

% call jrmpc to do the actual compuation, 
fprintf('Joint registration...(it takes a few minutes with full sets).\n');
[R,t,X,S,a] = jrmpc(V,Xin,'maxNumIter',maxNumIter,'gamma',0.4,'R',Rcellz,'t',tcellz);

% apply transformation to each view V{j} as R{j}*V{j}+t{j}*ones(1,Nj). Then
% segment each TV{j} into an 1 x Nj cell array with 3 x 1 vectors. This allows
% calling plot3 with the corresponding color for each point
TV = cellfun(@(V,R,t) bsxfun(@plus,R*V,t),V,R,t,'uniformoutput',false);

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
 figure
 
 
%  
  mergeshow(tranfpc)
  tranf1pc = tranformpcs(tranfpc,R,t)
  mergeshow(tranf1pc)
%      
    
    