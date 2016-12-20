% Loss diagram
clear all
clc
close all
epoch = 1:10;

train_Loss = [1.8918
                0.3905
                0.1023
                0.0509
                0.0334
                0.0253
                0.0164
                0.0133
                0.0097
                0.0082];
Test_Loss = [0.799
                    0.1382
                    0.0686
                    0.0417
                    0.0362
                    0.024
                    0.0233
                    0.0292
                    0.0163
                    0.0168];
figure
lbsz = 24;
w = 6;
plot(epoch,train_Loss, 'LineWidth', w, 'Color',[0,0.7,0.9]);
hold on
plot(epoch,Test_Loss, 'LineWidth', w, 'Color',[1,69/255,0]);
grid on
title('Train & Test Loss ')
xlabel('Epoch', 'FontSize', lbsz)
ylabel('Loss', 'FontSize', lbsz)
legend('Train Loss','Test Loss');
set(gca,'FontSize',lbsz)

train_accuracy = [0.476
                    0.956
                    0.9836
                    0.9932
                    0.9964
                    0.998
                    0.9992
                    0.9996
                    0.9996
                    0.9996];

Test_accuracy = [0.928
                        0.982
                        0.99
                        0.994
                        0.994
                        0.998
                        0.998
                        0.99
                        0.998
                        0.998];

  figure


  plot(epoch,train_accuracy, 'LineWidth', w, 'Color',[0,0.7,0.9]);
  hold on
  plot(epoch,Test_accuracy, 'LineWidth', w, 'Color',[113/255,198/255,113/255]);
  grid on
  title('Train & Test Accuracy ')


  xlabel('Epoch', 'FontSize', lbsz)
  ylabel('Loss', 'FontSize', lbsz)
  legend('Train Accuracy','Test Accuracy');
  set(gca,'FontSize',lbsz)
