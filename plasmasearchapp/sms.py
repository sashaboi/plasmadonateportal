import random
from urllib.request import urlopen, HTTPError
SMS_PROVIDER_USERNAME = 'onkard93'
SMS_PROVIDER_PASSWORD = 'onkard93'
SMS_PROVIDER_URL = "http://www.sms123.in/QuickSend.aspx?username="+SMS_PROVIDER_USERNAME+"&password="+SMS_PROVIDER_PASSWORD+"&sender=VOTEDS"
OTP_SMS = "Here%20is%20your%20verification%20OTP%20%3A%20"
OTP_SMS2 = "%20for%20Plasma%20Connect%20Portal"         
templateid="1207161820660681575"

def send_sms(number,otp):
    
    link = SMS_PROVIDER_URL+"&mob="+str(number)+"&msg="+OTP_SMS+str(otp)+OTP_SMS2+"&templateid="+templateid
    try:
        response = urlopen(link)
        print(response.read().decode("utf-8"))
        print(otp)
       
    except HTTPError as e:
        print(e.msg+str(e.code)+e.url)

    return otp
