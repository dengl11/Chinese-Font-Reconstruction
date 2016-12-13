function extract_font_sift(name)
  mat = strcat('_TRAIN_', name, '_characters.mat');
  load(char(mat))
  [nChar, d, d2] = size(characters);
  descriptors = [];
  for i = 1:nChar
    char_arr = single(reshape(characters(i,:,:), [d, d]));
    % f: frame | d: descriptor
    [f, desc] = vl_sift(char_arr);
    desc = desc';
    descriptors = [descriptors; desc];
  end
  save(char(strcat('_SIFT_', name)), 'descriptors')
end
