# Independent .NET reference;no production Python imports or execution.
$ErrorActionPreference='Stop'
$vectors=@()
foreach($seedText in @('Future-Pendulum-v1','0',"Caf$([char]0x00e9)","Cafe$([char]0x0301)",' seed ',('x'*256))) {
    $seedBytes=[Text.UTF8Encoding]::new($false,$true).GetBytes($seedText)
    if($seedBytes.Length -lt 1 -or $seedBytes.Length -gt 256){throw 'Invalid seed'}
    $prefix=[Text.Encoding]::ASCII.GetBytes("FuturePendulum`0v1`0symbolic-response`0")
    $length=[Convert]::FromHexString($seedBytes.Length.ToString('X8'))
    $indices=@();$categories=@();$first=$null;$counter=[uint64]0;$rejected=0
    while($indices.Count -lt 32) {
        $message=[byte[]]($prefix+$length+$seedBytes+[Convert]::FromHexString($counter.ToString('X16')))
        $hex=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($message)).ToLowerInvariant()
        if($null -eq $first){$first=$hex}
        $counter++
        for($offset=0;$offset -lt 64 -and $indices.Count -lt 32;$offset+=8) {
            $word=[Convert]::ToUInt64($hex.Substring($offset,8),16)
            if($word -ge [uint64]4294967295){$rejected++;continue}
            $index=[int]($word % 5);$indices+=@($index)
            $category=if($index -lt 2){'yes'}elseif($index -lt 4){'no'}else{'unresolved'}
            $categories+=@($category)
        }
    }
    $vectors+=@([ordered]@{seed=$seedText;first_block=$first;indices=$indices;categories=$categories;blocks=$counter;rejected_words=$rejected})
}
$result=[ordered]@{protocol='future-pendulum-sha256-v1';distribution='editorial-2-2-1-v1';method='Independent PowerShell/.NET SHA256,rejection and32 categorical draws per seed;no production imports';vectors=$vectors}
$json=ConvertTo-Json -InputObject $result -Depth 10
[IO.File]::WriteAllText((Join-Path (Get-Location) 'tests/fixtures/pendulum_seed_vectors.json'),$json+"`n",[Text.UTF8Encoding]::new($false))
Write-Output 'Six independent Pendulum32-draw vectors generated before engine implementation.'
