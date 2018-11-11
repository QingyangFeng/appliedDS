### Configurations for twitter api access:

Feel free to use my api details for playing around with the web app, but please don't make large twitter message requests, 2-10 twitter messages will be fine.

If you feel like you need to make larger requests then I recommend that you replace my api details with your own account, and read the twitter api documentation on limits.

Details of **getting api credentials** can be found [here](https://python-twitter.readthedocs.io/en/latest/getting_started.html), and put them in `usertweets.py` located in `site/twitterapp/Modules/`

User Timeline **limits** can be found [here](https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html)


### Installing dependencies (Python 2.7)

In the *terminal* move into the `site/twitterapp/`

```python
pip install -r requirements.txt
```

### Running Flask

Still in the site/twitterapp/ directory...

```bash
# In terminal 
export FLASK_APP=__init__.py
flask run
```

You should get the output if everything is set up correctly:
```
 * Serving Flask app "twitterapp"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Then enter `http://127.0.0.1:5000/user` to go to the webpage shown in the group meeting (19th Monday March)

### Problems?
Feel free to contact on group chat if there are problems.
