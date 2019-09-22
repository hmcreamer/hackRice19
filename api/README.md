## How to setup and run:
Run the following command just once (per terminal session):

`$ export FLASK_APP=run.py`

Run the following after every update:

`$ flask run`
or `$ python -m flask run`

 Then the app should be Running on http://127.0.0.1:5000/

 ## Endpoints
 In order to access our simulated environment, go to the route http://127.0.0.1:5000/simulate

 ## Documentation
 -Created an Experiment class that is used to create our simulated environments. This class allows researchers to specify how many nodes they want in the network, what percentage of the nodes will be bots vs. non-bots, and how many simulations they want to run (i.e. how many times the nodes transmit information)
 -The simulated environment assigns every node to be either a non-bot, bot promoting idea A (red in color), or bot promoting idea B (blue in color)
 -The simulated environment decides whether information is spread to neighboring nodes by using edge weights/probabilities
