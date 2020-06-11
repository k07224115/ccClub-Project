import smtplib   
from email.mime.multipart import MIMEMultipart # email內容載體
from email.mime.text import MIMEText # 用於製作文字內文
from email.mime.base import MIMEBase # 用於承載附檔
from email import encoders # 用於附檔編碼     
# 設定要使用的Gmail帳戶資訊
gmail_user = 'k07224115@gmail.com'
gmail_password = 'your_password' 
# 設定寄件資訊
from_address = gmail_user
to_address = ['k07224115@gmail.com']
Subject = f"{now.year}.{now.month}.{now.day - 1}"
attachments = [f"{now.year}.{now.month}.{now.day - 1}.csv"]
# 開始組合信件內容
mail = MIMEMultipart()
mail['From'] = from_address
mail['To'] = ', '.join(to_address)
mail['Subject'] = Subject
# 將信件內文加到email中
content = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(result.to_html())
mail.attach(MIMEText(content, "html"))     
# 將附加檔案們加到email中   
for file in attachments:
    with open(file, 'rb') as fp:
         add_file = MIMEBase('application', "octet-stream")
         add_file.set_payload(fp.read())
    encoders.encode_base64(add_file)
    add_file.add_header('Content-Disposition', 'attachment', filename = file)
    mail.attach(add_file) 
# 設定smtp伺服器並寄發信件    
smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465)
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)
smtpserver.sendmail(from_address, to_address, mail.as_string())
smtpserver.quit()
