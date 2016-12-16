accuracys = zeros(nName,1);
confusion_matrix = zeros(nName);
for i = 1:nName
  predict_dict = predict_accuracy(i, names, valid_descriptors, valid_descriptor_labels, N_TEST_CHAR, d, k_classify);
  accuracys(i) = predict_dict(i);
  confusion_matrix(:, i) = predict_dict;
end
disp 'Prediction Accuracy: '
accuracys

disp 'Confusion Matrix: '
confusion_matrix

imshow(1-confusion_matrix, 'InitialMagnification', 10000)
colormap(jet)
