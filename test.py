from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "ACe3c838c6b645a866229e427f88df7cc6" 
AUTH_TOKEN = "af6f39ac0646e837ed396bbc05f90143" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
	to="+919003042465", 
	from_="+12052893566", 
	body="working!", 
)