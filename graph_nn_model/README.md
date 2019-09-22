## Graph Neural Network for Node Prediction - Is each node a bot or not?

![learning problem diagram](https://i.imgur.com/8Yfam57.png)

This model - found in `model.py` - is built on the GraphSAGE (https://arxiv.org/abs/1706.02216) method which is a an inductive learning method on graph which means we will be able to make predictions on new additions to the graph (even after training!).

### How generate data?

Enter the `data/` directory and run: `$ python generate.py`. A file of type `.pth` will be saved within that directory. 
To use this new data, replace the path in the `get_loader` method in `data.py`.

### How to start training?

Ensure there is data in the `data/` directory and that it is linked to in `data.py` then run: `$ python train.py`

#### Citations

*Hamilton, Will, Zhitao Ying, and Jure Leskovec. **"Inductive representation learning on large graphs."** Advances in Neural Information Processing Systems. 2017.*

*Fey, Matthias, and Jan Eric Lenssen. **"Fast graph representation learning with PyTorch Geometric.**" arXiv preprint arXiv:1903.02428 (2019).*
