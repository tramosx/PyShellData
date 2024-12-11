import subprocess

def execute_bash_script(input_file, mode):
    script = './max-min-size.sh'
    try:
        result = subprocess.run([script, input_file, f"-{mode}"], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if not output:
            return {"error": "No data found in the file"}, None
        return output, None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()
    

def execute_bash_script_sorted(input_file, desc):
    script = './order-by-username.sh'
    try:
        cmd = ['./order-by-username.sh', input_file, '-desc' if desc else '']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return None, result.stderr

        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.strip()



def execute_bash_script_between_msgs(input_file, qtd_min, qtd_max):
    script = './between-msgs.sh'
    try:
        result = subprocess.run([script, input_file, qtd_min, qtd_max], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            return None, result.stderr

        return result.stdout, None
    except subprocess.CalledProcessError as e:
        return {"error": "Error processing file"}, None
