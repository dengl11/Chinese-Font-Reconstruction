% clear all
% startup
clc
close all
N_TRAIN_CHAR = 2000;
N_TEST_CHAR = 400;
k_classify = 1;
k_filter = 3;

% names = { 'Song',  'Li',  'Kai'};
names = { 'Song',  'Li',  'Kai',  'SoftXing',  'Zhuan'};
% names = { 'Song',  'Li',  'Kai',  'Xing',  'Zhuan'};
% names = { 'Song',  'Li',  'Kai',  'Xing'};

run('preprocess.m')
run('extract_sift.m')
run('merge.m')
run('descriptor_filter.m')
run('test.m')
