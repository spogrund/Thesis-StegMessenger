[audio1, Fs1] = audioread("audios/handel.wav");
[audio2, Fs2] = audioread("audios/vkfQkmqgtf.wav");
l1 = length(audio1);
l2 = length(audio2)-1;
samples = (0: l2)/Fs2;
subplot(2,1,1)
stem(audio2(samples), samples);



%R = corrcoef(audio1(samples), audio2(samples));



