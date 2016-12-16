
% example:

 A=[30,60;
	7,2;
	13,12;
	100,200];

B = [1,0;
     200,30;
     19,10];
G = {'first';'second';'ew'};
F=[1;2;3];
% knnclassify(sample_to_classify, train_X(filtered),  train_y(filtered))
knnclassify(A,B,G,2)
