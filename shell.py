import subprocess

cmd = ['mysql --login-path=local -Ddemo -e "select * from wallet_table where wallet_id = 100"']

f = open('data.csv', 'w')

subprocess.Popen(cmd, stdout = f, stderr = f, shell = True)
