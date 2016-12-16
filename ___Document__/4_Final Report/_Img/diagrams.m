% loss diagram

epoch = 1:10;

train_loss = [1.8918
                0.3905
                0.1023
                0.0509
                0.0334
                0.0253
                0.0164
                0.0133
                0.0097
                0.0082];
validation_loss = [0.799
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
plot(epoch,train_loss,'-*',epoch,validation_loss,'-*');
title('Train & Validation Loss ')
xlabel('Epoch')
ylabel('Loss')
legend('Train loss','Validation loss');

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
            
validation_accuracy = [0.928
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
plot(epoch,train_loss,'-x',epoch,validation_loss,'-x');
title('Train & Validation Accuracy ')
xlabel('Epoch')
ylabel('Accuracy')
legend('Train accuracy','Validation accuracy');                    
            


