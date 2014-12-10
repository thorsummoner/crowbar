# Fast
rm {path}/{file}.bsp
rm {bspdir}/{file}.bsp
{bsp} -game {gamedir} {path}/{file}
{vis} -fast -game {gamedir} {path}/{file}
{rad} -bounce 2 -noextra -game {gamedir} {path}/{file}
cp {path}/{file}.bsp {bspdir}/{file}.bsp
{game} -allowdebug -game {gamedir} +map {file}
