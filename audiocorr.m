list = dir('audios/*');
filenames = string({list.name});
disp(filenames)
for i=1:length(filenames)

    [audio1, Fs1] = audioread("audios/handel.wav");
    file = 'audios/' + filenames(i);
    if contains(file, '.wav')
        [audio2, Fs2] = audioread(file);
        
        audio1 = audio1(:, 1);
        audio2 = audio2(:, 1);
        
        l1 = length(audio1);
        l2 = length(audio2);
        lengthof = min(l1,l2);
        
        samples = (1:lengthof)/Fs1;
        audio1 = audio1(1:lengthof);
        audio2 = audio2(1:lengthof);
        
        %subplot(2,1,1);
        %plot(samples, audio1);
        
        %subplot(2,1,2)
        %plot(samples, audio2);
        
        R = corr(audio1, audio2);
        disp(file)
        disp(R)
    end
end