% DEMOJRMPCTOF   Example of using JRMPC in the registration of TOF data.
%    This demo loads M views from ./tofData/ and calls jrmpc to do the reg-
%    istration, then visualizes the result in 2 figures, one depicting the
%    final registration with all the points and another showing the reg-
%    istration with "unreliable points" removed. The color
%    value for each point was acquired by a stereo pair rigidly attached 
%    to the TOF camera. The colors are only needed for
%    the visualization and are not used by the algorithm at any step.
%
%    $ 18 / 12 / 2014 11:00 AM $

clc
close all
clear all

% indices of views to be read from ./tofData 
% filenames: view1.txt, view2.txt ...

M = 10;%the number of views, Nj is the cardinality of view V{j}
idx = transpose(1:M);


% construct file names to read the view*.txt files and make the legends
fname = arrayfun(@(idx) sprintf('./tofData/view%d.txt',idx),idx,'uniformoutput',false);

fprintf('TOF data loading from ''./tofData/''.\n');
% .txt files are organised in 6 columns, [x y z R G B], with the leftmost 3
% containing floating point indices and the rightmost 3 containing the color
% of the points as unsigned integers in the range [0,255], as in 24-bit RGB.
V = cellfun(@(fname) dlmread(fname,' '),fname,'uniformoutput',false);

% V now contains 6 x Nj matrices with coordinates and colors, separated 
% into point coordinates (V) and color info normalized in [0,1] (I).
% I is converted into a M x 1 cell array with 1 x Nj cell arrays with
% 3 x 1 vector-colors each, so we can feed each plot3 with a different color

 
% %%% optionally work with less points, donwnsample the point-sets by a factor df >1
df=1; % df=1 means no downsampling
[V,I] = cellfun(@(V) deal(V(1:df:end,1:3)',double(V(1:df:end,4:6))/255),V,'uniformoutput',false);


% initialize centers, the median cardinality can also be used as K but 
% it will dramatically increase the computational complexity without 
%  substantial gain in performance. Higher K can be combined with point-set
%  downsampling to avoid high complexity
K = 450;

% sample the unit sphere, by randomly selecting azimuth / elevation angles.
az = 2*pi*rand(1,K);
el = 2*pi*rand(1,K);

% (unit) polar to cartesian conversion.
Xin = [cos(az).*cos(el); sin(el); sin(az).*cos(el)];

Xin = Xin*100; % make them have the same order with points (it helps the convergence)


% choose the middle pointset instead to initialize the cluster centers
% Xin = V{5}(:,unique(round(linspace(1,size(V{5},2),K))));


% Number of Iterations.
maxNumIter = 30;
 

% call jrmpc to do the actual compuation, 
fprintf('Joint registration...(it takes a few minutes with full sets).\n');
[R,t,X,S,a,~,T] = jrmpc(V,Xin,'maxNumIter',maxNumIter,'gamma',0.1, 'epsilon', 1e-5);

%%
% visualize the registration process, see documentation of jrmpc for T.

figure(2);

for iter = 1:maxNumIter
    % apply transformation of iteration : iter
    TV = cellfun(@(V,R_iter,t_iter) bsxfun(@plus,R_iter*V,t_iter),V,T(:,1,iter),T(:,2,iter),'uniformoutput',false);
    
    clf(2);
    
    hold on, grid on
    
    title(sprintf('Registration of the sets after %d iteration(s).\n',iter),'fontweight','bold','fontsize',12);
    
    hg2 = cellfun(@(TV,clrmap,marker,markerSize) scatter3(TV(1,:),TV(2,:),TV(3,:),markerSize,clrmap,marker), TV, clrmap, marker, markerSize);
    
    legend(strIdx{:});
    
    set(2,'position',get(1,'position')+[+580 0 0 0]);
    
    % iteration 1 locks the axes of subsequent plots
    if iter == 1
       XLim = get(gca,'XLim');
       
       YLim = get(gca,'YLim');
       
       Zlim = get(gca,'ZLim');
       
       set(gca,'fontweight','bold','children',hg2);
    else
       set(gca,'XLim',XLim,'YLim',YLim,'ZLim',Zlim,'fontweight','bold','children',hg2); 
    end

    view([40 54])
    
    hold off
    
    pause(.12);
end

% detect and remove "bad" centers and "unreliable" points 
[TVrefined,Xrefined,Xrem] = removePointsAndCenters(TV,X,S,a);
    
% visualize TVrefined.
figure(3);
hold on, grid on

    title('Final registration with unreliable points removed','fontweight','bold','fontsize',12);
    
    hg3 = cellfun(@(TVrefined,clrmap,marker,mkSize) scatter3(TVrefined(1,:),TVrefined(2,:),TVrefined(3,:),mkSize,clrmap,marker),TVrefined,clrmap,marker,markerSize);
    
    legend(strIdx{:});
    
    % use the same axes as in the registration process
    set(gca,'XLim',XLim,'YLim',YLim,'ZLim',Zlim,'fontweight','bold','children',hg3);
    
    set(3,'position',get(1,'position')+[0 -510 0 0]);
    
    view([40 54]) 
hold off

% Visualize bad centers (orange) and good centers (blue).
figure(4);
hold on, grid on

    title('Final GMM means.','fontweight','bold','fontsize',12);
    
    scatter3(Xrefined(1,:),Xrefined(2,:),Xrefined(3,:),8,[0 .38 .67],'s');
    
    scatter3(Xrem(1,:),Xrem(2,:),Xrem(3,:),40,[1 .1412 0],'marker','x');
    
    legend('"Good" Centers','"Bad" Centers');
    
    % use the same axes as in the registration process
    set(gca,'XLim',XLim,'YLim',YLim,'ZLim',Zlim,'fontweight','bold');
    
    set(4,'position',get(1,'position')+[+580 -510 0 0]);
    
    view([40 54])
    
hold off

