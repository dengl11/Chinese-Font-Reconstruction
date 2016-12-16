nName = numel(names);
dir = './char_img/';
src = {};
for i = 1:nName
  src = vertcat(src, strcat(dir, names(i)));
end

d = 80;
for i = 1:nName
  img2dat(strcat('_TRAIN_',names(i)), string(src(i)), d, 1, N_TRAIN_CHAR+1)
end


for i = 1:nName
  img2dat(strcat('_TEST_', names(i)), string(src(i)), d, N_TRAIN_CHAR+1, N_TRAIN_CHAR+N_TEST_CHAR+1)
end
