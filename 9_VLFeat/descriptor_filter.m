% descriptor_diff_styles
% labels

%load descriptors and labels

[num_disc, length_disc] = size(descriptors_all);
valid_descriptors = [];

valid_descriptor_labels = [];

count = zeros(size(names));

for i = 1: num_disc
  if check_filter_importance(descriptors_all, font_labels, k_filter, i)
    valid_descriptors = [valid_descriptors; descriptors_all(i, :)];
    valid_descriptor_labels = [valid_descriptor_labels; font_labels(i)];
    count(font_labels(i)) = count(font_labels(i)) + 1;
  end
end

min_length = min(count);
cursor = 1;
% all_index = 1:num_disc;
rand_chosen_index = [];
for i = 1 : nName
    next_cursor = cursor + count(i);
    rand_perm = randperm(count(i));
    segment = cursor: (next_cursor - 1);
    rand_chosen_index = [rand_chosen_index, segment(rand_perm(1:min_length))];
    cursor = next_cursor;
end

valid_descriptors = valid_descriptors(rand_chosen_index,:);
valid_descriptor_labels = valid_descriptor_labels(rand_chosen_index);
