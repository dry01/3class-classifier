# -*- coding: utf-8 -*-
"""RBF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Yh2rxRCP_KVIyJ2YGgno3RyjEmUFphTi

)
RBFNnet
"""

# Commented out IPython magic to ensure Python compatibility.
import torch
import torchvision
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchvision.utils import make_grid
from torch.utils.data.dataloader import DataLoader
from torch.utils.data import random_split
# %matplotlib inline
from torch.utils.data import Dataset, DataLoader
#import torch_rbf as rbf

from sklearn import datasets
iris = datasets.load_iris()

images = iris.data
labels = iris.target

import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
one_hot_encoder = OneHotEncoder(sparse=False)
X = images

Y = labels
Y = one_hot_encoder.fit_transform(np.array(Y).reshape(-1, 1))
Y[:5]

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10,stratify = Y)

print(len(X_train))

x_train = torch.from_numpy(X_train)
y_train = torch.from_numpy(Y_train)
y_test = torch.from_numpy(Y_test)
x_test = torch.from_numpy(X_test)

from torch.utils.data import TensorDataset
train_ds = TensorDataset(x_train, y_train)
test_ds = TensorDataset(x_test, y_test)

from torch.utils.data import DataLoader
loss_fn = F.mse_loss

batch_size = 5
train_dl = DataLoader(train_ds, batch_size, shuffle=True)
test_dl = DataLoader(train_ds, batch_size, shuffle=True)

import torch.nn.functional as F
loss_fn = F.mse_loss

class Model(nn.Module):
  
    """Feedfoward neural network with 1 hidden layer"""
    def __init__(self, in_size, hidden_size, out_size):
        super().__init__()
        
        self.c = nn.Parameter(torch.ones(in_size ,in_size-1))
        self.beta = nn.Parameter(torch.ones(in_size-1))
        # hidden layer
        self.linear1 = nn.Linear(in_size, hidden_size)
        # output layer
        self.linear2 = nn.Linear(hidden_size, out_size)
        print(self.c.shape)
        print(type(self.c))
        
    def forward(self, xb):


      # Flatten the image tensors
      
      xb = (self.c - xb).pow(2)
      
      xb = torch.exp(-(torch.matmul(xb,self.beta)))
      # Get intermediate outputs using hidden layer
      out = self.linear1(xb)
      # Apply activation function
      out = F.relu(out)
      # Get predictions using output layer
      out = self.linear2(out)
      return out

input_size = 5
hidden_size = 8
num_classes = 3
for xb, yb in train_dl:
    
    break

model = Model(in_size=input_size, hidden_size=8, out_size=num_classes)

opt = torch.optim.SGD(model.parameters(), lr=0.00001)

losses = []
def fit(num_epochs, model, loss_fn, opt, train_dl):
    
    # Repeat for given number of epochs
    for epoch in range(num_epochs):


      
      epoch_loss = 0
        
        # Train with batches of data
      for xb,yb in train_dl:

            
          xb = xb.view(xb.size(0), -1)
          xb = xb.float()
      
          yb = yb.float()

            # 1. Generate predictions
          pred = model(xb)
            
            # 2. Calculate loss
          loss = loss_fn(pred, yb)
          epoch_loss += loss.item()
            
            # 3. Compute gradients
          loss.backward()
            
            # 4. Update parameters using gradients
          opt.step()
            
            # 5. Reset the gradients to zero
          opt.zero_grad()
      epoch_loss /= len(train_dl)
      losses.append(epoch_loss)
        
        # Print the progress
      if (epoch+1) % 1 == 0:
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))



loss = fit(5000,model,loss_fn,opt,train_dl)



losses1 = []
def fit1(num_epochs, model, loss_fn, opt, test_dl):
    
    # Repeat for given number of epochs
    for epoch in range(num_epochs):


      
      epoch_loss = 0
        
        # Train with batches of data
      for xb,yb in test_dl:

            
          xb = xb.view(xb.size(0), -1)
          xb = xb.float()
      
          yb = yb.float()

            # 1. Generate predictions
          pred = model(xb)
            
            # 2. Calculate loss
          loss = loss_fn(pred, yb)
          epoch_loss += loss.item()
            
            # 3. Compute gradients
          loss.backward()
            
            # 4. Update parameters using gradients
          opt.step()
            
            # 5. Reset the gradients to zero
          opt.zero_grad()
      epoch_loss /= len(test_dl)
      losses1.append(epoch_loss)
        
        # Print the progress
      if (epoch+1) % 1 == 0:
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, loss.item()))

loss = fit1(5000,model,loss_fn,opt,test_dl)

losses1

#plot for training and test losses
plt.plot(losses,'r-')

plt.plot(losses1,'b-')

plt.title('Train Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')

