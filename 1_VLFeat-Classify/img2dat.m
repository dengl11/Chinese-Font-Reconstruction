function img2dat(name, src, d, FROM, TO)
  src =   strcat(src, '/');
  contents = dir(char(strcat(src, '*.png'))); % or whatever the filename extension is
  characters = zeros(TO-FROM, d,d);
  k = 1;
  for i = FROM:numel(contents)
    filename = contents(i).name;
    img = imread(char(strcat(src, filename)));
    characters(k,:,:)= img;
    k = k + 1;
    if i >= TO
      break
    end
  end
  % save characters to mat
  save(char(strcat(name, '_characters.mat')), 'characters')
end
