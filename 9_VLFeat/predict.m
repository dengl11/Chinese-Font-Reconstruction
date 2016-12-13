% return prediction of font
function result = predict(characters,valid_descriptors, valid_descriptor_labels, idx, d, k)
  test_char = characters(idx, :, :);
  [f, sift_descriptor] = vl_sift(single(reshape(test_char, [d, d])));
  classfys = knnclassify(sift_descriptor', valid_descriptors, valid_descriptor_labels, k);
  result = mode(classfys);
end
