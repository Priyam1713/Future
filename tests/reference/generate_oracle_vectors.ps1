# Independent .NET/PowerShell reference. Does not import or execute production Python.
# Re-run from repository root with pwsh -File tests/reference/generate_tarot_vectors.ps1.
$ErrorActionPreference = 'Stop'
function New-Stream([string]$seedText,[string]$domain) {
    return [pscustomobject]@{Seed=$seedText;Domain=$domain;Counter=[uint64]0;Queue=[Collections.Generic.Queue[uint64]]::new();FirstBlock=$null}
}
function Next-Word($stream) {
    if ($stream.Queue.Count -eq 0) {
        $seedBytes=[Text.Encoding]::UTF8.GetBytes($stream.Seed)
        $prefix=[Text.Encoding]::ASCII.GetBytes("FutureCards`0v1`0"+$stream.Domain+"`0")
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
function Draw-Vector([string]$seedText) {
    $stream=New-Stream $seedText 'deck'
    $pack=@(1..36)
    for ($remaining=36;$remaining -gt 1;$remaining--) {
        $chosen=Below $stream $remaining
        $hold=$pack[$remaining-1];$pack[$remaining-1]=$pack[$chosen];$pack[$chosen]=$hold
    }
    return [ordered]@{seed=$seedText;deck_first_block=$stream.FirstBlock;permutation=$pack}
}
$vectors=@()
foreach($seedText in @('Future-Lenormand-v1','0',"Caf$([char]0x00e9)","Cafe$([char]0x0301)",' leading seed ','replay-36')) {
    $vectors+=@(Draw-Vector $seedText)
}
$result=[ordered]@{protocol='future-cards-sha256-fy-v1';method='Independent PowerShell/.NET reference;canonical numbers1..36;no production imports';vectors=$vectors}
$json=ConvertTo-Json -InputObject $result -Depth 10
[IO.File]::WriteAllText((Join-Path (Get-Location) 'tests/fixtures/oracle_seed_vectors.json'),$json+"`n",[Text.UTF8Encoding]::new($false))
Write-Output 'Six independent Lenormand full-pack vectors generated.'
