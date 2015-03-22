# Captcha Sniper Api Python

# Installation
download and put captchasniper folder next to your python files

## Usage
```python
from captchasniper import CaptchaSniperApi
cs_api = CaptchaSniperApi("http://CAPTCHA_SNIPER_SERVER:PORT")
captcha = cs_api.solve('/path/to/captcha.png')
# captcha is a str representing solved captcha or none if the captcha can't be solved
print(captcha)
```