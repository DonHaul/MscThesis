close all

fullpath='./lgs/2019-07-31_19:56:31_weasel'

posepath =  strcat(fullpath,'/poses.mat')
load(posepath)


% for everycmera




virginpcs={}

camnames=strtrim(string(camnames))

%%
load('pcs-31-Jul-20192.mat')

pcsaux = pcs

disp("switching ocurring")
pcs={pcsaux{1},pcs{4},pcs{2},pcs{3}}

%%

pcs = cleanPCnans(pcs)





virginpcs=pcs
%%
%assign initial pcs

Rcell = {}
tcell = {}
count=1

for str = camnames'
   


  %virginpcs{end+1}=ptCloud
   
  Rcell{end+1}=squeeze(R(count,:,:))
  tcell{end+1}=t(count,:)'
  
  
  count=count+1
  
end
%%

mergeshow(pcs);
%%
auxpcs=virginpcs;
auxpcs = croppc(auxpcs,1.5);

tranfpc = tranformpcs(auxpcs,Rcell,tcell);

figure
mergeshow(tranfpc);

pcs=tranfpc;
%%


 figure
%  
  RR = {R{1},R{2},R{3},R{4}}
  
  tranf1pc = tranformpcs(tranfpc,RR',t)
  mergeshow(tranf1pc)
%      
    
    