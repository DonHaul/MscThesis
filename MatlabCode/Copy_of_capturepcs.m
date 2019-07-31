%rosinit('htttp://metroserver01:11311')

rosinit('metroserver01',11311)
%%
camnames=["diavolo","mista","speedwagon","emperorcrimson"]

rgbtopic='/rgb/image_rect_color'
registeredpctopic= '/depth_registered/points'


topic=strcat(camnames(1),rgbtopic)
topic=char(topic)
sub = rossubscriber(topic)
%%
msg=receive(sub)
%%
 img = readImage(msg)
 
 imshow(img)
%%
rosshutdown