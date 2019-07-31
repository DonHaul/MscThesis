%rosinit('htttp://metroserver01:11311')

rosinit('metroserver01',11311)
%%
camnames=["diavolo","mista","speedwagon","emperorcrimson"]

rgbtopic='/rgb/image_rect_color'
registeredpctopic= '/depth_registered/points'


topic=strcat(camnames(1),registeredpctopic)
topic=char(topic)
sub = rossubscriber(topic)
%% loop

msg=receive(sub)

xyz = readXYZ(msg);
rgb = readRGB(msg);
%%

scatter3(msg)

%%
rosshutdown