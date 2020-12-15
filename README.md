<div align="center">
<img src="static/img/SmallLogo.png" alt="Order-tron">
</div>
<p align="center">Order-tron helps you view Etsy order information for your shop and export it to many formats.</p>

# Development instructions
To get started, run the following commands:
```bash
# Execute this to make a venv
$ mkdir venv && python3 -m venv venv

# Execute this to activate it
$ source venv/bin/activate

# Execute this to install dependencies
$ pip install -r requirements.txt
```

To run Order-tron locally, you must obtain your own Etsy API key for it. Once you do that, create a file called `env.json` in the root of your copy of Order-tron that looks like the following:
```json
{
  "api_key": "YOUR ETSY API PUBLIC KEY HERE",
  "api_secret": "YOUR ETSY API SECRET HERE"
}
```

Once you've done that, you are ready to run Order-tron! Just run the following (in the venv you set up earlier):
```bash
(venv) $ python main.py
```
If this command doesn't error out, that means you have successfully set up Order-tron. Flask will helpfully point out the URL to type to access your local Order-tron set-up.

# Legal Info & Disclaimers
Order-tron is &copy;2020 Ian Morrill under the [MIT License](/LICSENSE).

The term 'Etsy' is a trademark of Etsy, Inc. This application uses the Etsy API but is not endorsed or certified by Etsy.