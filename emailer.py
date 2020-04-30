import pdfkit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from secrets import EMAIL_PASS

def send_email(pr):
	"""
	Notifies member that a purchase request has been submitted on their behalf.
	"""
	fromaddr = "anovafinancereimbursements@gmail.com"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = pr['email']
	msg['Subject'] = "[ANova] Purchase Request Submitted on Callink"
	body = "Hi " + pr['first_name'] + ",\n\nA purchase request has been submitted on your behalf on Callink for the following reimbursement:\n" + pr['description'] + ".\n\nPlease look for your check in the mail soon. Feel free to email berkeleyanovaexecutive@gmail.com if you have any questions or concerns. Thanks!\n\nBest,\nANova Finance" 
	msg.attach(MIMEText(body, 'plain'))
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromaddr, EMAIL_PASS)
	text = msg.as_string()
	s.sendmail(fromaddr, pr['email'], text)
	s.quit()


# Send Email with PR as PDF (NOT WORKING)
# def send_email(link, email):
# 	pdfkit.from_url(link, "out.pdf")
# 	fromaddr = "anovafinancereimbursements@gmail.com"
# 	toaddr = email
# 	msg = MIMEMultipart()
# 	msg['From'] = fromaddr
# 	msg['To'] = toaddr
# 	msg['Subject'] = "[Important] Your ANova Reimbursement PDF"
# 	body = "Hi [Name],\nAttached is the PDF confirmation of your reimbursement submission. Please print this out and submit to the LEAD center with your receipt attached. \nEmail [_] if you have any questions.\nThanks, Finance"
# 	msg.attach(MIMEText(body, 'plain'))

# 	# open the file to be sent
# 	filename = "out.pdf"
# 	attachment = open("/Users/maggieluo/documents/cs/personal/anova_finance/out.pdf", "rb")
	
# 	p = MIMEBase('application', 'octet-stream')
# 	p.set_payload((attachment).read())
# 	encoders.encode_base64(p)
# 	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# 	msg.attach(p)
# 	s = smtplib.SMTP('smtp.gmail.com', 587)
# 	s.starttls()
# 	s.login(fromaddr, EMAIL_PASS)
# 	text = msg.as_string()

# 	# Send the email and terminate
# 	s.sendmail(fromaddr, toaddr, text)
# 	s.quit()
