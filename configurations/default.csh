# Default
rm {path}/{file}.bsp
rm {bspdir}/{file}.bsp
{bsp} -game {gamedir} {path}/{file}
{vis} -game {gamedir} {path}/{file}
{rad} -game {gamedir} {path}/{file}
cp {path}/{file}.bsp {bspdir}/{file}.bsp
{game} -sw -w1024 -h 768 -dev -console -allowdebug -game {gamedir} +map $file
