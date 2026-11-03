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
function Draw-Vector([string]$seedText,[int]$rounds,[int]$remove) {
    $stream=New-Stream $seedText 'deck'
    $pack=@(0..77 | Where-Object {$_ -ne $remove})
    $cuts=@()
    for ($round=0;$round -lt $rounds;$round++) {
        for ($i=$pack.Length-1;$i -gt 0;$i--) {
            $j=Below $stream ($i+1)
            $hold=$pack[$i];$pack[$i]=$pack[$j];$pack[$j]=$hold
        }
        if ($rounds -eq 3) {
            $cut=1+(Below $stream ($pack.Length-1));$cuts+=@($cut)
            $pack=@($pack[$cut..($pack.Length-1)])+@($pack[0..($cut-1)])
        }
    }
    $orient=New-Stream $seedText 'orientation'
    $bits=@();for($i=0;$i -lt 10;$i++) {$bits+=@(Below $orient 2)}
    return [ordered]@{seed=$seedText;rounds=$rounds;removed_index=$remove;deck_first_block=$stream.FirstBlock;orientation_first_block=$orient.FirstBlock;cuts=$cuts;permutation=$pack;orientation_bits=$bits}
}
$vectors=@()
foreach($seedText in @('Future-Tarot-v1',"Caf$([char]0x00e9)","Cafe$([char]0x0301)")) {
    $vectors+=@(Draw-Vector $seedText 1 -1)
    $vectors+=@(Draw-Vector $seedText 3 11)
}
$result=[ordered]@{protocol='future-cards-sha256-fy-v1';method='Independent PowerShell/.NET implementation of frozen framing,word extraction,rejection sampling,shuffle,cut and orientation;no production imports';vectors=$vectors}
$json=ConvertTo-Json -InputObject $result -Depth 10
[IO.File]::WriteAllText((Join-Path (Get-Location) 'tests/fixtures/tarot_seed_vectors.json'),$json+"`n",[Text.UTF8Encoding]::new($false))
Write-Output 'Six independent known-answer vectors generated.'
