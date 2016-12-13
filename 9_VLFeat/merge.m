descriptors_all = [];
font_labels = [];
for i = 1:nName
  name = names(i);
  load(char(strcat('_SIFT_', name, '.mat')))
  descriptors_all = [descriptors_all; descriptors];
  font_labels = [font_labels; ones(size(descriptors, 1), 1)*i];
end
