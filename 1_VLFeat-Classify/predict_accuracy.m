function distribution = predict_accuracy(font_index, names, valid_predictors, valid_predictor_labels, N_TEST_CHAR, d, k_classify)
  mat = strcat('_TEST_', string(names(font_index)), '_characters.mat');
  load(char(mat))
  predict_vec = [];
  nName = numel(names);
  distribution = zeros(nName, 1);
  for i = 1:N_TEST_CHAR
    predict_vec(i) = predict(characters,valid_predictors, valid_predictor_labels,  i, d, k_classify);
  end
  for i = 1:nName
    distribution(i) = numel(find(predict_vec==i))/N_TEST_CHAR;
  end
end
