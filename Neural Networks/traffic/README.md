First iteration is just returning a basic TF model with the set sizes, to validate that it is working:
1 convolution with 8 3x3 filters, no pooling layers, no hidden layers: received accuracy of 86% on the testing dataset.

With 1 2X2 pooling added: 88% accuracy, almost the same.

When increasing the number of convolution filters to 32: 95% accuracy. This makes sense as we indeed added complexity to the network.

When added another layer of 32 convolution filters and 2x2 pooling layers: 93% accuracy. The accuracy might have come down since we decreased the network complexity by the pooling.
If we took out the additional convolution and pooling, but instead added a 64 hidden layer, didn't improve the accuracy. In fact, with the relu activation the network was stuck at 5% accuracy.

I tried to increase the size of the hidden layer to 256 but it was overfitted - the test data was 88% accurate while the training data was 92%.

So I reduced the hidden layer size back to 64 and added another 64 hidden layer. The accuracy was 95%.

Finally I increased the number of the convolution filters to 64 or even 256 at each layer, and added yet another 64 hidden layer, with no significant increase in accuracy above 94%.

Then I increased the size of the first hidden layer to 196, to reflect the size of the pool layer. I expected a higher accuracy but received 83% while the training accuracy was 92%. That looked as a result of overfitting, so I added dropout of 0.5. The results then were still 83%, but now the training set results were 88%.

With the first hidden layer only the results were slightly improved to 89%.

Further explorations involved reducing the number of nodes: 2 convolution and pooling layers with less filters, then 2 smaller hidden layers of 36 nodes each. Since we only run few epochs, I eliminated the dropout. The result was both FAST and ACCURATE: 95%.