function [pcs] = capturepcs(frames,camnames,interval)


n_cams=size(camnames,1)

%rosinit('htttp://metroserver01:11311')
rosshutdown
rosinit('metroserver01',11311)



rgbtopic='/rgb/image_rect_color'
registeredpctopic= '/depth_registered/points'

for i=1:n_cams
        
    topic=strcat(camnames(i),registeredpctopic);
    topic=char(topic);
    sub(i) = rossubscriber(topic);
    
end


%% loop

xyzccum = zeros(307200,3,frames);
xyzcum = single(xyzccum);

rgbcum = zeros(307200,3,frames);

pcxyz = zeros(307200,3,n_cams);
pcxyz = single(pcxyz);
pcrgb = zeros(307200,3,n_cams);

%%
n_cams
disp("starting")
for j=1:n_cams
    for i=1:frames
        %save all pcs

        msg=receive(sub(j),5);

        xyzcum(:,:,i)=readXYZ(msg);
        
        rgbcum(:,:,i)=readRGB(msg);

        %rgbccum = rgbccum + readRGB(msg);

        pause(interval);
        i
    end
    %%
    pcxyz(:,:,j)=median(xyzcum,3,'omitnan');
    pcrgb(:,:,j)=median(rgbcum,3,'omitnan');
end

rosshutdown

%%
pcs={}

for j=1:n_cams
   pcs{j}=pointCloud(pcxyz(:,:,j),'Color',pcrgb(:,:,j)) 
end

end
