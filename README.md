# Chainalysis_Take_home

Clone the repository using
```
git clone https://github.com/ArthDh/Chainalysis_Take_home.git
```

Create a python virtual environment
```python
python -m venv env
```
Activate the environment
```
source  env/bin/activate
```

Install dependencies
```
pip install requirements.txt
```

Run the Flask server
```
python webapp.py
```


Questionnaire:

Are there any sub-optimal choices( or short cuts taken due to limited time ) in your implementation?
Yes, I would like to implement unit testing of functions and have documentation for each of them. The backend could also be better handled. Requests should have been cached to Db for faster retrieval  

Is any part of it over-designed? ( It is fine to over-design to showcase your skills as long as you are clear about it)
I implemented a general exchange comparision however some of the exchanges require api keys.
This can be easily extended to multiple coins as well.

If you have to scale your solution to 100 users/second traffic what changes would you make, if any?
A Centralized Database server to along with load balancing could be introduced. 

What are some other enhancements you would have made, if you had more time to do this implementation
I would implement a heurestic based recommendation engine to select exchanges and coins for maximal profit at a given point of time.
