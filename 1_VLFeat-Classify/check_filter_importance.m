function is_important = check_filter_importance(descriptors, labels, k, index)
  nDesc = size(descriptors, 1);
  descrip_copys = repmat(descriptors(index,:), nDesc, 1);
  diff = descrip_copys - descriptors;
  distance =  sqrt(sum(diff.^2,2));
  [~,idx] = sort(distance);
  k_min_idx = idx(1:k, :);
  for i = 1:size(k_min_idx, 1)
    if labels(index) ~= labels(k_min_idx(i))
      is_important = 0;
      return
    end
  end
  is_important = 1;
end
