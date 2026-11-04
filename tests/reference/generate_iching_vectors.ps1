# Independent .NET/PowerShell reference. Does not import or execute production Python.
# Re-run from repository root with pwsh -File tests/reference/generate_tarot_vectors.ps1.
$ErrorActionPreference = 'Stop'
function New-Stream([string]$seedText,[string]$domain) {
    return [pscustomobject]@{Seed=$seedText;Domain=$domain;Counter=[uint64]0;Queue=[Collections.Generic.Queue[uint64]]::new();FirstBlock=$null}
}
function Next-Word($stream) {
    if ($stream.Queue.Count -eq 0) {
        $seedBytes=[Text.Encoding]::UTF8.GetBytes($stream.Seed)
        $prefix=[Text.Encoding]::ASCII.GetBytes("FutureIChing`0v1`0"+$stream.Domain+"`0")
        $lengthBytes=[Convert]::FromHexString($seedBytes.Length.ToString('X8'))
        $counterBytes=[Convert]::FromHexString($stream.Counter.ToString('X16'))
        $message=[byte[]]($prefix+$lengthBytes+$seedBytes+$counterBytes)
        $hex=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($message)).ToLowerInvariant()
        if ($null -eq $stream.FirstBlock) {$stream.FirstBlock=$hex}
        for ($i=0;$i -lt 64;$i+=8) {$stream.Queue.Enqueue([Convert]::ToUInt64($hex.Substring($i,8),16))}
        $stream.Counter++
    }
    return $stream.Queue.Dequeue()
}
function Below($stream,[uint64]$n) {
    $size=[uint64]4294967296
    $ceiling=$size-($size % $n)
    do {$word=Next-Word $stream} while ($word -ge $ceiling)
    return [int]($word % $n)
}
function Cast-Vector([string]$seedText,[string]$method) {
    $stream=New-Stream $seedText $method
    $lines=@();$raw=@()
    foreach($position in 1..6) {
        if($method -eq 'three-coin') {
            $bits=@();foreach($coin in 1..3) {$bits+=@(Below $stream 2)}
            $value=6+($bits | Measure-Object -Sum).Sum
            $lines+=@([int]$value);$raw+=,@($bits)
        } else {
            $draw=Below $stream 16
            $raw+=@($draw)
            if($draw -eq 0){$value=6}elseif($draw -le 5){$value=7}elseif($draw -le 12){$value=8}else{$value=9}
            $lines+=@($value)
        }
    }
    return [ordered]@{seed=$seedText;method=$method;first_block=$stream.FirstBlock;lines=$lines;raw=$raw}
}
$vectors=@()
foreach($seedText in @('Future-IChing-v1','0',"Caf$([char]0x00e9)","Cafe$([char]0x0301)",' seed ',('x'*256),([string][char]0x00e9)*128)) {
    foreach($method in @('three-coin','yarrow-marginal')) {$vectors+=@(Cast-Vector $seedText $method)}
}
$result=[ordered]@{protocol='future-iching-sha256-v1';method='Independent PowerShell/.NET framing,SHA256,word/rejection and casts;no production imports';vectors=$vectors}
[IO.File]::WriteAllText((Join-Path (Get-Location) 'tests/fixtures/iching_seed_vectors.json'),(ConvertTo-Json -InputObject $result -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output 'Fourteen independent I Ching cast vectors generated before production casting code.'
