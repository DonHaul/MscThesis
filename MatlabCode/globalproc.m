close all
clear all
load("..\Logs\2019-07-31_19_56_31_weasel\poses.mat")

%%
load("./pcs-31-Jul-20191.mat")
%%

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

%pcs = cleanPCnans(pcs)
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

modelz=[]
%convert to vertices struct
for k=1:max(size(V))
   models = cell2mat( V(k) );
   
   modelz(k).vertices = double(models')
    
end

MaxSteps = 50;
tic
[R, t, s, Centroid, corr, registeredModel] = globalProcrustes(modelz, MaxSteps);
toc

addpath('GlobalProcrustesICP')
%%

% Plot model before-after registration
figure(1); clf;
visModel(modelz);
figure(2); clf;
visModel(registeredModel);
%%
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

%% convert merged H to the cell output
Rcell={}
tcell={}

for i=1:length(pcs)
   Rcell{i}=mergedH(1:3,1:3,i)
   tcell{i}=mergedH(1:3,4,i)
end

%%


 figure
 
 
%  
  mergeshow(tranfpc)
  tranf1pc = tranformpcs(tranfpc,Rcell,tcell)
  mergeshow(tranf1pc)
%      
    
    